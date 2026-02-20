# -*- coding: utf-8 -*-
"""
Map visualization component for City Lens
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np

def create_base_map(lat=40.7128, lon=-74.0060, zoom_start=12):
    """
    Create a base Folium map
    """
    m = folium.Map(
        location=[lat, lon],
        zoom_start=zoom_start,
        tiles="CartoDB positron"
    )
    return m

def add_heatmap_layer(map_obj, data_points, radius=15, blur=10):
    """
    Add a heatmap layer to the map
    """
    from folium.plugins import HeatMap
    
    # Convert data to format needed for heatmap
    heat_data = [[point['lat'], point['lon'], point['intensity']] 
                 for point in data_points]
    
    HeatMap(
        heat_data,
        radius=radius,
        blur=blur,
        max_zoom=1
    ).add_to(map_obj)
    
    return map_obj

def add_markers(map_obj, locations, popup_text=None):
    """
    Add markers to the map
    """
    for i, loc in enumerate(locations):
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=popup_text[i] if popup_text else loc.get('name', ''),
            icon=folium.Icon(color=loc.get('color', 'blue'), 
                           icon=loc.get('icon', 'info-sign'))
        ).add_to(map_obj)
    
    return map_obj

def create_impact_map(analysis_results):
    """
    Create a complete impact map based on analysis results
    """
    # Default to NYC if no location
    lat = analysis_results.get('latitude', 40.7128)
    lon = analysis_results.get('longitude', -74.0060)
    
    # Create base map
    m = create_base_map(lat, lon)
    
    # Add different layers based on impact type
    if 'congestion_hotspots' in analysis_results:
        add_heatmap_layer(
            m, 
            analysis_results['congestion_hotspots'],
            radius=20,
            blur=15
        )
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def display_impact_map(analysis_results):
    """
    Main function to display map in Streamlit
    """
    st.subheader("📍 Impact Heatmap")
    
    # Create map
    m = create_impact_map(analysis_results)
    
    # Display map
    map_data = st_folium(
        m,
        width=1200,
        height=500,
        returned_objects=["last_clicked", "bounds"]
    )
    
    # Show clicked location info
    if map_data and map_data["last_clicked"]:
        st.write("Selected location:", map_data["last_clicked"])
    
    return map_data

def create_traffic_layer(roads_data):
    """
    Create a traffic congestion layer
    """
    traffic_map = folium.Map()
    
    for road in roads_data:
        # Color based on congestion level
        if road['congestion'] > 0.8:
            color = 'red'
        elif road['congestion'] > 0.6:
            color = 'orange'
        elif road['congestion'] > 0.4:
            color = 'yellow'
        else:
            color = 'green'
        
        folium.PolyLine(
            locations=road['coordinates'],
            color=color,
            weight=5,
            opacity=0.7,
            popup=f"{road['name']}: {road['congestion']*100:.0f}% congested"
        ).add_to(traffic_map)
    
    return traffic_map

def create_environmental_layer(env_data):
    """
    Create environmental impact layer
    """
    env_map = folium.Map()
    
    # Add air quality markers
    for station in env_data.get('air_quality_stations', []):
        color = 'green' if station['aqi'] < 50 else 'yellow' if station['aqi'] < 100 else 'orange' if station['aqi'] < 150 else 'red'
        
        folium.CircleMarker(
            location=[station['lat'], station['lon']],
            radius=10,
            color=color,
            fill=True,
            fillOpacity=0.6,
            popup=f"AQI: {station['aqi']}"
        ).add_to(env_map)
    
    return env_map