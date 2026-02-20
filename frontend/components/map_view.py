# -*- coding: utf-8 -*-
"""
Simplified map visualization component for City Lens
"""

import streamlit as st
import folium
from streamlit_folium import st_folium

def display_impact_map(analysis_results):
    """
    Main function to display map in Streamlit
    """
    st.markdown("""
    <div style="background: #1E293B; border-radius: 16px; padding: 1.5rem; 
                border: 1px solid #334155; margin-bottom: 1rem;">
        <h3 style="color: #F1F5F9; margin-bottom: 1rem;">📍 Impact Location Map</h3>
    """, unsafe_allow_html=True)
    
    # Get location from results or use default
    lat = analysis_results.get('latitude', 40.7128)
    lon = analysis_results.get('longitude', -74.0060)
    
    # Create a simple map
    m = folium.Map(
        location=[lat, lon],
        zoom_start=14,
        tiles="OpenStreetMap"
    )
    
    # Add a marker for the project location
    folium.Marker(
        [lat, lon],
        popup="Project Location",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Add a circle for impact area
    folium.Circle(
        radius=500,
        location=[lat, lon],
        color='#06B6D4',
        fill=True,
        fillOpacity=0.2,
        popup="Impact Area (500m radius)"
    ).add_to(m)
    
    # Display the map
    st_data = st_folium(m, width=700, height=400)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return st_data
