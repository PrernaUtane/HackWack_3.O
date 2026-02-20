# -*- coding: utf-8 -*-
"""
API Client for City Lens Backend
Handles simulation endpoints only (auth kept separate)
"""

import streamlit as st
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class APIClient:
    """API client for backend simulation endpoints"""
    
    def __init__(self, base_url=None):
        self.base_url = base_url or os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")
        self.timeout = int(os.getenv("API_TIMEOUT", 30))
        print(f"✅ API Client initialized with backend: {self.base_url}")
    
    def _handle_response(self, response):
        """Handle API response with proper error messages"""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                st.error("🔐 Authentication required. Please login.")
            elif response.status_code == 403:
                st.error("⛔ You don't have permission for this action")
            elif response.status_code == 404:
                st.error("🔍 Resource not found")
            elif response.status_code == 422:
                errors = response.json().get('detail', 'Validation error')
                st.error(f"❌ Invalid data: {errors}")
            elif response.status_code >= 500:
                st.error("🔧 Backend server error. Please try again later.")
            else:
                st.error(f"❌ Error {response.status_code}")
            return None
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to backend. Is the server running?")
            return None
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
            return None
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            return None
    
    # ===== SIMULATION ENDPOINTS =====
    
    def simulate(self, project_data):
        """
        Run impact simulation
        
        project_data: {
            project_type: "commercial"|"residential"|"mixed_use"|"industrial"
            size_sqft: int
            latitude: float
            longitude: float
            city: str
            height: optional int
            parking_spaces: optional int
            green_space_percent: optional float
        }
        """
        url = f"{self.base_url}/simulate"
        
        try:
            with st.spinner("🔄 Analyzing impacts with backend..."):
                response = requests.post(
                    url,
                    json=project_data,
                    timeout=self.timeout * 2
                )
                
                result = self._handle_response(response)
                
                if result:
                    # Cache the result
                    st.session_state['last_simulation'] = result
                    st.session_state['last_simulation_time'] = datetime.now().isoformat()
                    
                return result
                
        except Exception as e:
            st.error(f"❌ Simulation failed: {str(e)}")
            return None
    
    def health_check(self):
        """Check if backend is healthy"""
        url = f"{self.base_url}/health"
        
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

# Global API client instance
def get_api_client():
    """Get or create API client instance"""
    if 'api_client' not in st.session_state:
        backend_url = os.getenv("BACKEND_URL", "http://localhost:8000/api/v1")
        st.session_state['api_client'] = APIClient(backend_url)
    return st.session_state['api_client']