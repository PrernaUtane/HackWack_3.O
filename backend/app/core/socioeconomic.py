# backend/app/core/socioeconomic.py
from app.models.schemas import ProjectInput, ProjectType, RiskLevel
import logging

logger = logging.getLogger(__name__)

class SocioeconomicEngine:
    """Derives socioeconomic impacts from congestion and project type"""
    
    @staticmethod
    def calculate_impacts(congestion_score: float, project: ProjectInput) -> dict:
        """Calculate socioeconomic impacts using rule-based approach"""
        
        # Property value change
        if project.project_type == ProjectType.COMMERCIAL:
            if congestion_score < 0.5:
                prop_change = 15
            elif congestion_score < 0.8:
                prop_change = 5
            else:
                prop_change = -10
        elif project.project_type == ProjectType.RESIDENTIAL:
            if congestion_score < 0.4:
                prop_change = 8
            elif congestion_score < 0.7:
                prop_change = 0
            else:
                prop_change = -15
        elif project.project_type == ProjectType.MIXED_USE:
            if congestion_score < 0.5:
                prop_change = 12
            elif congestion_score < 0.75:
                prop_change = 3
            else:
                prop_change = -8
        else:  # industrial
            if congestion_score < 0.6:
                prop_change = 5
            else:
                prop_change = -5
        
        # Jobs created
        jobs_per_sqft = {
            ProjectType.COMMERCIAL: 0.005,   # 5 jobs per 1000 sq ft
            ProjectType.RESIDENTIAL: 0.001,   # 1 job per 1000 sq ft
            ProjectType.MIXED_USE: 0.003,
            ProjectType.INDUSTRIAL: 0.004
        }
        
        total_jobs = int(project.size_sqft * jobs_per_sqft[project.project_type])
        const_jobs = int(total_jobs * 0.3)  # 30% construction
        perm_jobs = total_jobs - const_jobs
        
        # Population change
        if project.project_type == ProjectType.RESIDENTIAL:
            people_per_sqft = 0.002  # 2 people per 1000 sq ft
            pop_change = int(project.size_sqft * people_per_sqft)
        else:
            pop_change = int(perm_jobs * 0.4)  # 40% of jobs bring families
        
        # Gentrification risk
        if congestion_score > 0.7 and project.project_type == ProjectType.COMMERCIAL:
            gent_risk = RiskLevel.HIGH
        elif congestion_score > 0.5 or project.project_type == ProjectType.MIXED_USE:
            gent_risk = RiskLevel.MODERATE
        else:
            gent_risk = RiskLevel.LOW
        
        # Demographic shift
        if project.project_type == ProjectType.COMMERCIAL:
            demographic = {
                "young_adults_18_34": round(15 + (congestion_score * 15), 1),
                "families_35_54": round(10 - (congestion_score * 5), 1),
                "seniors_65plus": round(5 - (congestion_score * 3), 1)
            }
        elif project.project_type == ProjectType.RESIDENTIAL:
            demographic = {
                "young_adults_18_34": round(5 + (congestion_score * 5), 1),
                "families_35_54": round(20 - (congestion_score * 5), 1),
                "seniors_65plus": round(8 + (congestion_score * 2), 1)
            }
        else:
            demographic = {
                "young_adults_18_34": round(10 + (congestion_score * 10), 1),
                "families_35_54": round(15 - (congestion_score * 5), 1),
                "seniors_65plus": round(6 - (congestion_score * 1), 1)
            }
        
        logger.info(f"Socioeconomic calc: prop_change={prop_change}%, jobs={total_jobs}")
        
        return {
            "property_value_change_percent": round(prop_change, 1),
            "jobs_created_construction": const_jobs,
            "jobs_created_permanent": perm_jobs,
            "population_change": pop_change,
            "gentrification_risk": gent_risk,
            "demographic_shift": demographic
        }