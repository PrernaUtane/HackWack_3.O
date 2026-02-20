# fetcher.py
print("Hello World - It works!")

class DataFetcher:
    def __init__(self):
        print("✅ DataFetcher initialized")
    
    def fetch_traffic_data(self, lat, lon):
        print(f"🌐 Fetching traffic data for {lat}, {lon}")
        return {
            "speed": 35,
            "source": "mock"
        }
    
    def fetch_all(self, lat, lon):
        print("🚀 Fetching ALL data")
        traffic = self.fetch_traffic_data(lat, lon)
        return {
            "traffic": traffic,
            "location": {"lat": lat, "lon": lon}
        }

if __name__ == "__main__":
    fetcher = DataFetcher()
    data = fetcher.fetch_all(40.7128, -74.0060)
    print(data)