# -*- coding: utf-8 -*-
"""
City Lens - Urban Impact Forecasting System
Team: Epoch Elites
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Import components
from components.sidebar import render_project_input
from components.map_view import display_impact_map
from components.charts import (
    create_congestion_gauge,
    create_impact_breakdown,
    create_impact_comparison
)

# Page configuration
st.set_page_config(
    page_title="City Lens - Urban Impact Forecasting",
    page_icon="🏙️",
    layout="wide"
)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state['analysis_results'] = None

# Title
st.title("🏙️ City Lens")
st.markdown("### See the future of your city before breaking ground")

# Render sidebar and get project input
analyze_clicked, project_input = render_project_input()

# Main content area
if analyze_clicked or st.session_state['analysis_results']:
    
    if analyze_clicked:
        # Simulate analysis (replace with actual API call)
        with st.spinner("Analyzing impacts..."):
            # Mock analysis results
            st.session_state['analysis_results'] = {
                'latitude': project_input.get('latitude', 40.7128),
                'longitude': project_input.get('longitude', -74.0060),
                'congestion_score': 0.75,
                'traffic_impact': 85,
                'air_quality': 145,
                'property_change': 12,
                'jobs_created': 250,
                'population_affected': 15000,
                'congestion_hotspots': [
                    {'lat': 40.7128, 'lon': -74.0060, 'intensity': 0.9},
                    {'lat': 40.7138, 'lon': -74.0070, 'intensity': 0.8},
                    {'lat': 40.7148, 'lon': -74.0080, 'intensity': 0.7},
                ]
            }
        st.success("Analysis complete!")
    
    results = st.session_state['analysis_results']
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "🗺️ Impact Map", 
        "📈 Detailed Analysis",
        "💡 Recommendations"
    ])
    
    with tab1:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Traffic Impact",
                f"{results['traffic_impact']}/100",
                delta="High Risk",
                delta_color="inverse"
            )
        with col2:
            st.metric(
                "Air Quality",
                f"AQI: {results['air_quality']}",
                delta="Unhealthy",
                delta_color="inverse"
            )
        with col3:
            st.metric(
                "Property Value",
                f"+{results['property_change']}%",
                delta="Increase"
            )
        with col4:
            st.metric(
                "Jobs Created",
                f"{results['jobs_created']:,}",
                delta="Permanent"
            )
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            # Congestion gauge
            fig_gauge = create_congestion_gauge(results['congestion_score'])
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            # Impact breakdown
            impact_scores = {
                'Traffic': 85,
                'Environment': 72,
                'Socioeconomic': 45,
                'Infrastructure': 68,
                'Community': 35
            }
            fig_breakdown = create_impact_breakdown(impact_scores)
            st.plotly_chart(fig_breakdown, use_container_width=True)
        
        # Affected population
        st.metric(
            "Population Affected",
            f"{results['population_affected']:,} people",
            help="Number of people directly impacted"
        )
    
    with tab2:
        # Display impact map
        display_impact_map(results)
    
    with tab3:
        st.subheader("Detailed Impact Analysis")
        
        # Before/After comparison
        before = [45, 65, 55, 70, 30]
        after = [85, 72, 68, 82, 35]
        
        fig_compare = create_impact_comparison(before, after)
        st.plotly_chart(fig_compare, use_container_width=True)
        
        # Detailed metrics table
        st.subheader("Impact Metrics")
        metrics_df = pd.DataFrame({
            'Metric': ['Peak Hour Congestion', 'Average Speed', 'PM2.5 Levels', 'Noise Levels', 'Property Values'],
            'Current': ['35 min', '25 mph', '12 μg/m³', '65 dB', '$500k'],
            'Projected': ['55 min (+57%)', '18 mph (-28%)', '22 μg/m³ (+83%)', '78 dB (+20%)', '$560k (+12%)'],
            'Threshold': ['45 min', '20 mph', '15 μg/m³', '70 dB', 'N/A']
        })
        st.dataframe(metrics_df, use_container_width=True)
    
    with tab4:
        st.subheader("AI-Powered Recommendations")
        
        recommendations = [
            {
                'category': '🚦 Traffic',
                'title': 'Widen Main Street intersection',
                'description': 'Add dedicated left-turn lane to reduce congestion by 25%',
                'priority': 'High',
                'cost': 'Medium',
                'impact': 'High'
            },
            {
                'category': '🌳 Environment',
                'title': 'Install green buffer zone',
                'description': 'Plant 200 trees along boundary to reduce air pollution',
                'priority': 'Medium',
                'cost': 'Low',
                'impact': 'Medium'
            },
            {
                'category': '🏘️ Community',
                'title': 'Affordable housing provision',
                'description': 'Include 20% affordable units to mitigate displacement',
                'priority': 'High',
                'cost': 'High',
                'impact': 'High'
            },
            {
                'category': '🚌 Transit',
                'title': 'Add bus rapid transit lane',
                'description': 'Dedicated BRT lane on Main Street',
                'priority': 'Medium',
                'cost': 'High',
                'impact': 'High'
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"{rec['category']}: {rec['title']}"):
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Priority", rec['priority'])
                col2.metric("Cost", rec['cost'])
                col3.metric("Impact", rec['impact'])
                col4.metric("ROI", "High")
                st.write(rec['description'])
                
                # Add implement button
                if st.button(f"Implement {rec['title']}", key=rec['title']):
                    st.success("Added to implementation plan!")

else:
    # Welcome screen
    st.info("👈 Enter project details in the sidebar and click 'Analyze Impact' to begin")
    
    # Show sample visualization
    st.subheader("How City Lens Works")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **1️⃣ Input**
        - Project location
        - Development type
        - Size and timeline
        """)
        st.image("https://via.placeholder.com/150?text=Input")
    
    with col2:
        st.markdown("""
        **2️⃣ Analyze**
        - AI predicts impacts
        - Real-time data
        - Multi-factor analysis
        """)
        st.image("https://via.placeholder.com/150?text=AI")
    
    with col3:
        st.markdown("""
        **3️⃣ Decide**
        - Visualize impacts
        - Get recommendations
        - Make decisions
        """)
        st.image("https://via.placeholder.com/150?text=Decide")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("© 2026 Epoch Elites")
with col2:
    st.markdown("City Lens v1.0")
with col3:
    st.markdown("Team: Epoch Elites")