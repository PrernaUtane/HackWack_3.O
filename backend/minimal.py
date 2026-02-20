from fastapi import FastAPI, APIRouter
from datetime import datetime
import random
import uvicorn

# Create router
router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "City Lens API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@router.post("/simulate")
async def simulate(project: dict):
    # Generate random but realistic data
    congestion = round(random.uniform(0.4, 0.9), 2)
    
    return {
        "traffic": {
            "congestion_score": congestion,
            "congestion_level": "High" if congestion > 0.7 else "Moderate",
            "peak_hours": ["7-9 AM", "5-7 PM"],
            "affected_roads": [
                {"name": "Main Street", "impact": f"+{int(congestion*50)}%", "distance": "0.2 miles"}
            ],
            "recommendation": "Add bus lanes and optimize signals"
        },
        "environmental": {
            "air_quality_index": int(50 + congestion * 150),
            "air_quality_level": "Unhealthy" if congestion > 0.6 else "Moderate",
            "pm25": round(15 + congestion * 30, 1),
            "pm10": round(25 + congestion * 50, 1),
            "noise_level_db": round(55 + congestion * 30, 1),
            "heat_island_effect_c": round(congestion * 3, 1),
            "stormwater_runoff_increase": round(congestion * 50, 1)
        },
        "socioeconomic": {
            "property_value_change_percent": round(15 - congestion * 20, 1),
            "jobs_created_construction": int(50 + project.get('size_sqft', 50000) / 1000),
            "jobs_created_permanent": int(100 + project.get('size_sqft', 50000) / 500),
            "population_change": int(5000 + project.get('size_sqft', 50000) / 10),
            "gentrification_risk": "High" if congestion > 0.7 else "Moderate"
        },
        "infrastructure": {
            "road_capacity_utilization": round(65 + congestion * 35, 1),
            "transit_demand_increase": round(congestion * 40, 1),
            "recommendations": [
                "Road widening needed" if congestion > 0.7 else "Monitor road capacity"
            ],
            "stress_level": "High" if congestion > 0.7 else "Moderate"
        },
        "unified_impact_score": int(congestion * 100),
        "recommendations": [
            "Add dedicated left-turn lanes",
            "Install green buffer zone",
            "Include affordable housing"
        ],
        "simulation_id": f"sim_{random.randint(1000, 9999)}",
        "timestamp": datetime.now().isoformat()
    }

# Create main app
app = FastAPI(title="City Lens API", version="1.0.0")
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "City Lens API", "status": "running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
