# backend/app/core/environmental.py
from app.models.schemas import ProjectInput
from app.data.fetcher import DataFetcher
from app.data.cache import Cache
import logging

logger = logging.getLogger(__name__)

class EnvironmentalEngine:
    """Derives environmental impacts from congestion score and real data"""
    
    def __init__(self):
        self.fetcher = DataFetcher()
        self.cache = Cache()
    
    def calculate_impacts(self, congestion_score: float, project: ProjectInput) -> dict:
        """
        Calculate environmental impacts using real air quality data
        """
        try:
            # Fetch real air quality data for baseline
            air_data = self.fetcher.fetch_air_quality(project.latitude, project.longitude)
            
            # Air Quality Index
            if air_data and 'aqi' in air_data:
                # Use real AQI as baseline
                base_aqi = air_data['aqi']
                aqi = base_aqi + (congestion_score * 30)  # Add projected increase
                logger.info(f"Using real AQI baseline: {base_aqi}")
            else:
                # Fallback to formula
                aqi = 50 + (congestion_score * 150)
                logger.info("Using formula-based AQI (no real data)")
            
            aqi = min(aqi, 300)
            
            # Air quality level
            if aqi < 50:
                aqi_level = "Good"
            elif aqi < 100:
                aqi_level = "Moderate"
            elif aqi < 150:
                aqi_level = "Unhealthy for Sensitive Groups"
            elif aqi < 200:
                aqi_level = "Unhealthy"
            else:
                aqi_level = "Very Unhealthy"
            
            # Noise pollution - can be adjusted with real data if available
            if air_data and 'noise' in air_data:
                base_noise = air_data['noise']
                noise = base_noise + (congestion_score * 15)
            else:
                noise = 55 + (congestion_score * 30)
            
            noise = min(noise, 85)
            
            # Urban heat island effect
            # Check if we have satellite temp data
            if air_data and 'temperature' in air_data:
                base_temp = air_data['temperature']
                heat = base_temp + (congestion_score * 1.5)
                heat_effect = heat - base_temp
            else:
                heat_effect = congestion_score * 3.0
            
            # Stormwater runoff
            runoff = congestion_score * 50
            if project.green_space_percent:
                runoff *= (1 - project.green_space_percent / 100)
            
            # Add PM2.5 and PM10 if available
            pm25 = air_data.get('pm25', 15.0) if air_data else 15.0
            pm10 = air_data.get('pm10', 25.0) if air_data else 25.0
            
            return {
                "air_quality_index": round(aqi, 1),
                "air_quality_level": aqi_level,
                "pm25": round(pm25, 1),
                "pm10": round(pm10, 1),
                "noise_level_db": round(noise, 1),
                "heat_island_effect_c": round(heat_effect, 1),
                "stormwater_runoff_increase": round(runoff, 1),
                "data_sources": {
                    "real_aqi": bool(air_data and 'aqi' in air_data)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in environmental engine: {str(e)}")
            # Fallback calculation
            aqi = 50 + (congestion_score * 150)
            aqi = min(aqi, 300)
            
            return {
                "air_quality_index": round(aqi, 1),
                "air_quality_level": "Moderate",
                "pm25": 15.0,
                "pm10": 25.0,
                "noise_level_db": round(55 + (congestion_score * 30), 1),
                "heat_island_effect_c": round(congestion_score * 3.0, 1),
                "stormwater_runoff_increase": round(congestion_score * 50, 1),
                "data_sources": {"using_fallback": True}
            }