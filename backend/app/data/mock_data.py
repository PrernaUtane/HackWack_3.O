# backend/app/data/mock_data.py
import random
from datetime import datetime

class MockDataProvider:
    """Provides mock data for testing"""
    
    @staticmethod
    def get_mock_traffic(lat=None, lon=None):
        return {
            "speed": random.randint(20, 50),
            "free_flow_speed": random.randint(50, 70),
            "current_travel_time": random.randint(60, 180),
            "free_flow_travel_time": random.randint(40, 100),
            "confidence": round(random.uniform(0.6, 0.95), 2),
            "road_density": round(random.uniform(0.3, 0.8), 2),
            "source": "mock",
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def get_mock_air_quality(lat=None, lon=None):
        aqi = random.randint(30, 150)
        return {
            "aqi": aqi,
            "pm25": round(aqi * 0.3, 1),
            "pm10": round(aqi * 0.5, 1),
            "level": "Moderate" if aqi < 100 else "Unhealthy",
            "source": "mock"
        }
    
    @staticmethod
    def get_mock_all(lat=None, lon=None):
        return {
            "traffic": MockDataProvider.get_mock_traffic(lat, lon),
            "air_quality": MockDataProvider.get_mock_air_quality(lat, lon),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    data = MockDataProvider.get_mock_all(40.7128, -74.0060)
    print(data)