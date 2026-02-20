# backend/tests/test_integration.py
"""
Test script for Harshita to verify data module integration
Run with: python -m backend.tests.test_integration
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data.integration_helper import ImpactDataHelper
import json

def test_different_locations():
    """Test the helper with various locations"""
    print("\n" + "="*50)
    print("TESTING DIFFERENT LOCATIONS")
    print("="*50)
    
    helper = ImpactDataHelper()
    
    # Test locations
    test_cases = [
        {"lat": 40.7128, "lon": -74.0060, "city": "New York", "name": "NYC Downtown"},
        {"lat": 34.0522, "lon": -118.2437, "city": "Los Angeles", "name": "LA Downtown"},
        {"lat": 41.8781, "lon": -87.6298, "city": "Chicago", "name": "Chicago Loop"},
        {"lat": 29.7604, "lon": -95.3698, "city": "Houston", "name": "Houston"},
        {"lat": 51.5074, "lon": -0.1278, "city": "London", "name": "London"}  # Tests default city factor
    ]
    
    for test in test_cases:
        print(f"\n📍 Testing: {test['name']}")
        data = helper.get_all_impact_data(test['lat'], test['lon'], test['city'])
        
        print(f"   Congestion Score: {data['congestion_data']['base_congestion']}")
        print(f"   Traffic Speed: {data['congestion_data']['traffic_speed']} km/h")
        print(f"   Road Density: {data['congestion_data']['road_density']}")
        print(f"   City Factor: {data['congestion_data']['city_factor']}")
        print(f"   AQI: {data['environmental_data']['baseline_aqi']} ({data['environmental_data']['air_quality_level']})")

def test_caching():
    """Test that caching is working"""
    print("\n" + "="*50)
    print("TESTING CACHE SYSTEM")
    print("="*50)
    
    helper = ImpactDataHelper()
    lat, lon = 40.7128, -74.0060
    
    print("\n🔄 First call (should cache miss):")
    data1 = helper.get_all_impact_data(lat, lon, "New York")
    
    print("\n🔄 Second call (should cache hit):")
    data2 = helper.get_all_impact_data(lat, lon, "New York")
    
    # Check if same data (cached)
    if data1['congestion_data']['timestamp'] == data2['congestion_data']['timestamp']:
        print("✅ Cache is working! Same timestamp returned")
    else:
        print("❌ Cache not working - timestamps differ")

def test_edge_cases():
    """Test edge cases"""
    print("\n" + "="*50)
    print("TESTING EDGE CASES")
    print("="*50)
    
    helper = ImpactDataHelper()
    
    # Test with no city (should use default)
    print("\n📍 No city provided:")
    data = helper.get_all_impact_data(40.7128, -74.0060)
    print(f"   City Factor (default): {data['congestion_data']['city_factor']}")
    
    # Test with extreme coordinates
    print("\n📍 Extreme coordinates:")
    data = helper.get_all_impact_data(0, 0)
    print(f"   Still works: {data['congestion_data']['base_congestion']}")

if __name__ == "__main__":
    print("\n🔧 INTEGRATION TESTS FOR HARSHITA")
    print("Run these to verify everything works!\n")
    
    test_different_locations()
    test_caching()
    test_edge_cases()
    
    print("\n" + "="*50)
    print("✅ ALL TESTS COMPLETE")
    print("="*50)