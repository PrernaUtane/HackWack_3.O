# backend/app/core/infrastructure.py
from app.models.schemas import ProjectInput, RiskLevel
import logging

logger = logging.getLogger(__name__)

class InfrastructureEngine:
    """Calculates infrastructure stress and recommendations"""
    
    @staticmethod
    def calculate_impacts(congestion_score: float, project: ProjectInput) -> dict:
        """
        Calculate infrastructure impacts
        """
        
        # Road capacity utilization
        road_utilization = 65 + (congestion_score * 35)  # 65-100%
        road_utilization = min(road_utilization, 100)
        
        # Transit impact
        transit_demand = congestion_score * 40  # % increase
        
        # Water demand increase
        water_demand = (project.size_sqft / 100000) * 15  # gallons per day
        water_demand = min(water_demand, 100)
        
        # Electricity demand
        electricity_demand = (project.size_sqft / 100000) * 25  # kWh
        electricity_demand = min(electricity_demand, 150)
        
        # Recommendations
        recommendations = []
        
        if road_utilization > 85:
            recommendations.append("Road widening needed within 2 years")
        if transit_demand > 25:
            recommendations.append("Increase bus frequency on nearby routes")
        if water_demand > 50:
            recommendations.append("Upgrade water mains in this sector")
        if electricity_demand > 80:
            recommendations.append("Substation upgrade required")
        
        if len(recommendations) == 0:
            recommendations.append("Current infrastructure adequate")
        
        return {
            "road_capacity_utilization": round(road_utilization, 1),
            "transit_demand_increase": round(transit_demand, 1),
            "water_demand_increase": round(water_demand, 1),
            "electricity_demand_increase": round(electricity_demand, 1),
            "recommendations": recommendations,
            "stress_level": RiskLevel.HIGH if road_utilization > 85 else 
                           RiskLevel.MODERATE if road_utilization > 70 else 
                           RiskLevel.LOW
        }