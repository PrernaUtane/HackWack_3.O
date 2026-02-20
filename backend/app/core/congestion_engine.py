# backend/app/core/congestion_engine.py
from app.models.schemas import ProjectInput, ProjectType, RiskLevel
from app.data.fetcher import DataFetcher
from app.data.geospatial import GeospatialAnalyzer
from app.data.cache import Cache
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class CongestionEngine:
    """Core engine that calculates congestion score using real data"""
    
    def __init__(self):
        self.fetcher = DataFetcher()
        self.geo = GeospatialAnalyzer()
        self.cache = Cache()
    
    def calculate_score(self, project: ProjectInput) -> Dict:
        """
        Calculate congestion score based on project parameters
        Uses real data from APIs via the data module
        """
        try:
            # Step 1: Fetch real-time data for this location
            logger.info(f"Fetching data for location: {project.latitude}, {project.longitude}")
            real_data = self.fetcher.fetch_all(project.latitude, project.longitude)
            
            # Step 2: Get road network data
            road_data = self.geo.get_road_density(project.latitude, project.longitude)
            
            # Step 3: Base score by project type
            base_scores = {
                ProjectType.COMMERCIAL: 0.6,
                ProjectType.RESIDENTIAL: 0.4,
                ProjectType.MIXED_USE: 0.5,
                ProjectType.INDUSTRIAL: 0.7
            }
            
            score = base_scores[project.project_type]
            logger.info(f"Base score: {score}")
            
            # Step 4: Adjust based on real traffic data
            if real_data and 'traffic' in real_data:
                traffic = real_data['traffic']
                traffic_speed = traffic.get('speed', 35)
                congestion_level = traffic.get('congestion_level', 'moderate')
                
                # Lower speed = higher congestion
                if traffic_speed < 20 or congestion_level == 'heavy':
                    score *= 1.3
                elif traffic_speed < 30 or congestion_level == 'moderate':
                    score *= 1.1
                
                logger.info(f"Traffic adjustment: speed={traffic_speed}, new score={score}")
            
            # Step 5: Adjust based on road density
            if road_data and 'density' in road_data:
                density = road_data['density']
                score *= (1 + density * 0.5)  # Higher density = more congestion
                logger.info(f"Road density adjustment: density={density}, new score={score}")
            
            # Step 6: Size factor (per 100,000 sq ft)
            size_factor = min(project.size_sqft / 100000, 2.0)
            score *= size_factor
            logger.info(f"Size factor: {size_factor}, new score={score}")
            
            # Step 7: Location factor from city
            dense_cities = ["New York", "Mumbai", "Tokyo", "London", "Delhi", "Shanghai"]
            if project.city in dense_cities:
                score *= 1.3
                logger.info(f"Dense city adjustment: {project.city}, new score={score}")
            
            # Step 8: Parking impact
            if project.parking_spaces:
                parking_factor = 1.0 + (project.parking_spaces / 1000) * 0.15
                score *= min(parking_factor, 1.5)
                logger.info(f"Parking factor: {parking_factor}, new score={score}")
            
            # Step 9: Green space reduces impact
            if project.green_space_percent:
                green_factor = 1.0 - (project.green_space_percent / 100) * 0.4
                score *= max(green_factor, 0.6)
                logger.info(f"Green space factor: {green_factor}, new score={score}")
            
            # Step 10: Cap the score
            score = min(score, 1.5)
            score = max(score, 0.1)
            
            # Step 11: Determine risk level
            if score < 0.3:
                level = RiskLevel.LOW
            elif score < 0.6:
                level = RiskLevel.MODERATE
            elif score < 0.9:
                level = RiskLevel.HIGH
            else:
                level = RiskLevel.SEVERE
            
            # Step 12: Get peak hours based on project type
            peaks = {
                ProjectType.COMMERCIAL: ["7-9 AM", "12-2 PM", "5-7 PM"],
                ProjectType.RESIDENTIAL: ["6-8 AM", "5-8 PM"],
                ProjectType.MIXED_USE: ["7-9 AM", "12-2 PM", "5-8 PM"],
                ProjectType.INDUSTRIAL: ["5-7 AM", "3-6 PM"]
            }
            peak_hours = peaks.get(project.project_type, ["8-9 AM", "5-6 PM"])
            
            # Step 13: Get affected roads from geospatial data
            affected_roads = []
            if road_data and 'nearby_roads' in road_data:
                for i, road in enumerate(road_data['nearby_roads'][:3]):
                    impact_pct = 30 + (i * 15)
                    affected_roads.append({
                        "name": road.get('name', f'Road {i+1}'),
                        "impact": f"+{impact_pct}%",
                        "distance": f"{road.get('distance', 0.5 + i*0.3):.1f} miles"
                    })
            else:
                # Fallback mock data
                affected_roads = [
                    {"name": "Main Street", "impact": "+45%", "distance": "0.2 miles"},
                    {"name": "Broadway", "impact": "+32%", "distance": "0.4 miles"},
                    {"name": "Park Avenue", "impact": "+28%", "distance": "0.6 miles"}
                ]
            
            # Step 14: Generate recommendation
            if score > 0.8:
                rec = "🚨 CRITICAL: Add bus lanes immediately. Widen Main Street. Increase public transit frequency by 40%."
            elif score > 0.5:
                rec = "⚠️ MODERATE: Optimize traffic signals at key intersections. Consider adding turn lanes. Monitor peak hours."
            else:
                rec = "✅ LOW IMPACT: Standard monitoring post-construction recommended. Add pedestrian crossings."
            
            result = {
                "score": round(score, 2),
                "level": level,
                "peak_hours": peak_hours,
                "affected_roads": affected_roads,
                "recommendation": rec,
                "data_sources": {
                    "traffic_api": bool(real_data and 'traffic' in real_data),
                    "road_network": bool(road_data)
                }
            }
            
            # Cache the result
            cache_key = f"congestion_{project.latitude}_{project.longitude}_{project.project_type}"
            self.cache.set(cache_key, result, ttl=3600)  # Cache for 1 hour
            
            return result
            
        except Exception as e:
            logger.error(f"Error in congestion engine: {str(e)}")
            # Fallback to basic calculation without real data
            return self._fallback_calculation(project)
    
    def _fallback_calculation(self, project: ProjectInput) -> Dict:
        """Fallback calculation when APIs fail"""
        logger.info("Using fallback calculation")
        
        # Basic calculation without real data
        base_scores = {
            ProjectType.COMMERCIAL: 0.6,
            ProjectType.RESIDENTIAL: 0.4,
            ProjectType.MIXED_USE: 0.5,
            ProjectType.INDUSTRIAL: 0.7
        }
        
        score = base_scores[project.project_type]
        score *= min(project.size_sqft / 100000, 2.0)
        
        if project.parking_spaces:
            score *= 1.0 + (project.parking_spaces / 1000) * 0.15
        
        score = min(score, 1.5)
        
        if score < 0.3:
            level = RiskLevel.LOW
        elif score < 0.6:
            level = RiskLevel.MODERATE
        elif score < 0.9:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.SEVERE
        
        return {
            "score": round(score, 2),
            "level": level,
            "peak_hours": ["7-9 AM", "5-7 PM"],
            "affected_roads": [
                {"name": "Main Street", "impact": "+35%", "distance": "0.2 miles"}
            ],
            "recommendation": "Standard monitoring recommended",
            "data_sources": {"using_fallback": True}
        }