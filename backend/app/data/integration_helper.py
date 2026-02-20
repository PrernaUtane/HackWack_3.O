from .fetcher import DataFetcher 
 
class ImpactDataHelper: 
    def __init__(self): 
        self.fetcher = DataFetcher() 
        print("Helper ready") 
 
    def get_all_impact_data(self, lat, lon, city=None): 
        return self.fetcher.fetch_all(lat, lon) 
