# -*- coding: utf-8 -*-
"""
Enhanced map visualization component for City Lens
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
from folium.plugins import HeatMap, Fullscreen, MeasureControl

def create_base_map(lat=40.7128, lon=-74.0060, zoom_start=13):
    """
    Create a base Folium map with dark theme
    """
    # Use dark tile layer
    m = folium.Map(
        location=[lat, lon],
        zoom_start=zoom_start,
        tiles="CartoDB dark_matter",  # Dark theme tiles
        attr="City Lens"
    )
    
    # Add fullscreen button
    Fullscreen().add_to(m)
    
    # Add measurement tool
    MeasureControl(position='topleft').add_to(m)
    
    return m

def add_heatmap_layer(map_obj, data_points, radius=20, blur=15, name="Heatmap"):
    """
    Add a heatmap layer to the map with better styling
    """
    # Convert data to format needed for heatmap
    heat_data = [[point['lat'], point['lon'], point.get('intensity', 0.8)] 
                 for point in data_points]
    
    HeatMap(
        heat_data,
        radius=radius,
        blur=blur,
        max_zoom=1,
        gradient={0.4: 'blue', 0.6: 'lime', 0.8: 'yellow', 1.0: 'red'},
        name=name
    ).add_to(map_obj)
    
    return map_obj

def add_markers(map_obj, locations, popup_text=None):
    """
    Add markers to the map
    """
    for i, loc in enumerate(locations):
        # Color based on type
        color = loc.get('color', 'blue')
        icon = loc.get('icon', 'info-sign')
        
        folium.Marker(
            location=[loc['lat'], loc['lon']],
            popup=popup_text[i] if popup_text else loc.get('name', ''),
            icon=folium.Icon(color=color, icon=icon, prefix='fa'),
            tooltip=loc.get('name', '')
        ).add_to(map_obj)
    
    return map_obj

def add_circle_markers(map_obj, locations, radius=50, name="Points"):
    """
    Add circle markers with popups
    """
    fg = folium.FeatureGroup(name=name)
    
    for loc in locations:
        # Determine color based on value
        if 'value' in loc:
            if loc['value'] > 80:
                color = '#EF4444'  # red
            elif loc['value'] > 60:
                color = '#F59E0B'  # orange
            elif loc['value'] > 40:
                color = '#FBBF24'  # yellow
            else:
                color = '#10B981'  # green
        else:
            color = loc.get('color', '#06B6D4')
        
        folium.CircleMarker(
            location=[loc['lat'], loc['lon']],
            radius=radius,
            color=color,
            fill=True,
            fillOpacity=0.6,
            popup=loc.get('popup', ''),
            tooltip=loc.get('name', '')
        ).add_to(fg)
    
    fg.add_to(map_obj)
    return map_obj

def add_traffic_layer(map_obj, roads_data):
    """
    Create a traffic congestion layer with colored roads
    """
    fg = folium.FeatureGroup(name="Traffic Congestion")
    
    for road in roads_data:
        # Color based on congestion level
        congestion = road.get('congestion', 0.5)
        if congestion > 0.8:
            color = '#EF4444'  # red
            weight = 7
        elif congestion > 0.6:
            color = '#F59E0B'  # orange
            weight = 6
        elif congestion > 0.4:
            color = '#FBBF24'  # yellow
            weight = 5
        else:
            color = '#10B981'  # green
            weight = 4
        
        folium.PolyLine(
            locations=road['coordinates'],
            color=color,
            weight=weight,
            opacity=0.8,
            popup=f"{road.get('name', 'Road')}: {congestion*100:.0f}% congested",
            tooltip=road.get('name', 'Road')
        ).add_to(fg)
    
    fg.add_to(map_obj)
    return map_obj

def add_air_quality_layer(map_obj, stations):
    """
    Add air quality monitoring stations
    """
    fg = folium.FeatureGroup(name="Air Quality")
    
    for station in stations:
        aqi = station.get('aqi', 50)
        
        # Color based on AQI
        if aqi > 200:
            color = '#7F1D1D'  # dark red
            icon = 'exclamation-triangle'
        elif aqi > 150:
            color = '#EF4444'  # red
            icon = 'warning'
        elif aqi > 100:
            color = '#F59E0B'  # orange
            icon = 'exclamation-circle'
        elif aqi > 50:
            color = '#FBBF24'  # yellow
            icon = 'info-circle'
        else:
            color = '#10B981'  # green
            icon = 'check-circle'
        
        folium.Marker(
            location=[station['lat'], station['lon']],
            icon=folium.Icon(color='red' if 'red' in color else 'blue', 
                           icon=icon, prefix='fa'),
            popup=f"""
            <b>{station.get('name', 'Station')}</b><br>
            AQI: {aqi}<br>
            PM2.5: {station.get('pm25', 0)} μg/m³<br>
            PM10: {station.get('pm10', 0)} μg/m³
            """,
            tooltip=f"AQI: {aqi}"
        ).add_to(fg)
    
    fg.add_to(map_obj)
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
    
    # Add different layers based on what's available
    
    # 1. Congestion hotspots (heatmap)
    if 'congestion_hotspots' in analysis_results:
        add_heatmap_layer(
            m, 
            analysis_results['congestion_hotspots'],
            radius=25,
            blur=20,
            name="Traffic Heat"
        )
    
    # 2. Traffic roads
    if 'roads' in analysis_results:
        add_traffic_layer(m, analysis_results['roads'])
    
    # 3. Air quality stations
    if 'air_stations' in analysis_results:
        add_air_quality_layer(m, analysis_results['air_stations'])
    
    # 4. Points of interest
    if 'poi' in analysis_results:
        add_circle_markers(m, analysis_results['poi'], radius=30, name="Points of Interest")
    
    # Add layer control
    folium.LayerControl(position='topright', collapsed=False).add_to(m)
    
    return m

def generate_sample_roads(lat, lon):
    """Generate sample road data for demo"""
    return [
        {
            'name': 'Main Street',
            'coordinates': [[lat, lon], [lat+0.01, lon+0.01]],
            'congestion': 0.85
        },
        {
            'name': 'Broadway',
            'coordinates': [[lat+0.005, lon-0.005], [lat+0.015, lon+0.005]],
            'congestion': 0.72
        },
        {
            'name': 'Park Avenue',
            'coordinates': [[lat-0.01, lon], [lat+0.01, lon]],
            'congestion': 0.45
        }
    ]

def generate_sample_air_stations(lat, lon):
    """Generate sample air quality stations"""
    return [
        {
            'name': 'Downtown Station',
            'lat': lat + 0.005,
            'lon': lon - 0.005,
            'aqi': 145,
            'pm25': 45,
            'pm10': 80
        },
        {
            'name': 'Riverside Station',
            'lat': lat - 0.008,
            'lon': lon + 0.01,
            'aqi': 98,
            'pm25': 25,
            'pm10': 40
        }
    ]

def generate_sample_poi(lat, lon):
    """Generate sample points of interest"""
    return [
        {
            'name': 'City Hall',
            'lat': lat + 0.002,
            'lon': lon - 0.003,
            'value': 90,
            'popup': 'City Hall - Government'
        },
        {
            'name': 'Central Hospital',
            'lat': lat - 0.005,
            'lon': lon + 0.004,
            'value': 75,
            'popup': 'Medical Center'
        },
        {
            'name': 'University',
            'lat': lat + 0.008,
            'lon': lon + 0.006,
            'value': 60,
            'popup': 'State University'
        }
    ]

def display_impact_map(analysis_results):
    """
    Main function to display map in Streamlit
    """
    st.markdown("""
    <div class="chart-container">
        <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
            <h3 style="color: #F1F5F9; margin: 0;">📍 Impact Heatmap</h3>
            <span style="color: #06B6D4;">🔄 Click layers to toggle</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Add sample data if not present
    if 'roads' not in analysis_results:
        analysis_results['roads'] = generate_sample_roads(
            analysis_results.get('latitude', 40.7128),
            analysis_results.get('longitude', -74.0060)
        )
    
    if 'air_stations' not in analysis_results:
        analysis_results['air_stations'] = generate_sample_air_stations(
            analysis_results.get('latitude', 40.7128),
            analysis_results.get('longitude', -74.0060)
        )
    
    if 'poi' not in analysis_results:
        analysis_results['poi'] = generate_sample_poi(
            analysis_results.get('latitude', 40.7128),
            analysis_results.get('longitude', -74.0060)
        )
    
    # Create map
    m = create_impact_map(analysis_results)
    
    # Display map
    map_data = st_folium(
        m,
        width=1200,
        height=500,
        returned_objects=["last_clicked", "bounds", "last_object_clicked"]
    )
    
    # Show clicked location info
    if map_data and map_data.get("last_clicked"):
        st.markdown(f"""
        <div style="background: #0F172A; border-radius: 8px; padding: 1rem; margin-top: 1rem;
                    border-left: 4px solid #06B6D4;">
            <span style="color: #06B6D4;">📍 Selected Location:</span>
            <span style="color: #F1F5F9; margin-left: 1rem;">
                Lat: {map_data['last_clicked']['lat']:.4f}, 
                Lng: {map_data['last_clicked']['lng']:.4f}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    # Legend
    st.markdown("""
    <div style="display: flex; gap: 2rem; margin-top: 1rem; padding: 1rem; 
                background: #1E293B; border-radius: 8px;">
        <div><span style="color: #EF4444;">🔴</span> Critical (80-100)</div>
        <div><span style="color: #F59E0B;">🟠</span> High (60-80)</div>
        <div><span style="color: #FBBF24;">🟡</span> Moderate (40-60)</div>
        <div><span style="color: #10B981;">🟢</span> Low (0-40)</div>
        <div><span style="color: #06B6D4;">🔵</span> Points of Interest</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return map_data