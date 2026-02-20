# backend/app/data/cache.py
import time
from datetime import datetime, timedelta
import hashlib
import json

class DataCache:
    """Simple cache to store API responses"""
    
    def __init__(self, expiry_minutes=60):
        self.cache = {}
        self.expiry_minutes = expiry_minutes
        print(f"✅ Cache initialized (expires after {expiry_minutes} minutes)")
    
    def _generate_key(self, *args, **kwargs):
        """Generate unique cache key"""
        key_string = str(args) + str(sorted(kwargs.items()))
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get(self, key):
        """Get value from cache if not expired"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            age = datetime.now() - timestamp
            
            if age < timedelta(minutes=self.expiry_minutes):
                print(f"📦 Cache HIT: {key}")
                return data
            else:
                print(f"⏰ Cache EXPIRED: {key}")
                del self.cache[key]
        
        print(f"❌ Cache MISS: {key}")
        return None
    
    def set(self, key, value):
        """Store value in cache"""
        self.cache[key] = (value, datetime.now())
        print(f"💾 Cache SET: {key}")
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        print("🗑️ Cache cleared")

# Global cache instance
cache = DataCache(expiry_minutes=30)

def cached(func):
    """Decorator to cache function results"""
    def wrapper(*args, **kwargs):
        cache_key = f"{func.__name__}:{cache._generate_key(*args, **kwargs)}"
        result = cache.get(cache_key)
        if result is not None:
            return result
        result = func(*args, **kwargs)
        cache.set(cache_key, result)
        return result
    return wrapper

if __name__ == "__main__":
    # Test the cache
    cache.set("test", {"message": "Hello Cache"})
    print(cache.get("test"))