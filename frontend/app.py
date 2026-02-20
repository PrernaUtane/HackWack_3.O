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
from components.auth import require_auth, show_user_profile, logout
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

# Check authentication FIRST
user = require_auth()  # This will redirect to login if not authenticated

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state['analysis_results'] = None

# Show user profile in sidebar
show_user_profile()

# Title with user greeting
st.title(f"🏙️ City Lens")
st.markdown(f"### Welcome back, {user.get('name', 'User')}! 👋")

# Role-based welcome message
role_messages = {
    'admin': "You have full access to all features.",
    'planner': "Plan and evaluate urban development projects.",
    'enterprise': "Access advanced analytics and API features.",
    'public': "View public impact assessments."
}
st.caption(role_messages.get(user.get('role', 'public'), ""))

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
    
    # Role-based access control for features
    user_role = user.get('role', 'public')
    
    # Create tabs (different based on role)
    if user_role in ['admin', 'planner', 'enterprise']:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "🗺️ Impact Map", 
            "📈 Detailed Analysis",
            "💡 Recommendations",
            "⚙️ Advanced"
        ])
    else:
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
        
        # Different recommendations based on user role
        if user_role == 'admin':
            recommendations = [
                {
                    'category': '🚦 Traffic',
                    'title': 'Widen Main Street intersection',
                    'description': 'Add dedicated left-turn lane to reduce congestion by 25%',
                    'priority': 'High',
                    'cost': '$2.5M',
                    'impact': 'High',
                    'roi': '3.2x'
                },
                {
                    'category': '🌳 Environment',
                    'title': 'Install green buffer zone',
                    'description': 'Plant 200 trees along boundary to reduce air pollution',
                    'priority': 'Medium',
                    'cost': '$150K',
                    'impact': 'Medium',
                    'roi': '1.8x'
                },
                {
                    'category': '🏘️ Community',
                    'title': 'Affordable housing provision',
                    'description': 'Include 20% affordable units to mitigate displacement',
                    'priority': 'High',
                    'cost': '$5M',
                    'impact': 'High',
                    'roi': '2.5x'
                }
            ]
        elif user_role == 'enterprise':
            recommendations = [
                {
                    'category': '🚦 Traffic',
                    'title': 'Widen Main Street intersection',
                    'description': 'Add dedicated left-turn lane to reduce congestion by 25%',
                    'priority': 'High',
                    'cost': '$2.5M',
                    'impact': 'High',
                    'api_access': True
                },
                {
                    'category': '🌳 Environment',
                    'title': 'Install green buffer zone',
                    'description': 'Plant 200 trees along boundary to reduce air pollution',
                    'priority': 'Medium',
                    'cost': '$150K',
                    'impact': 'Medium',
                    'api_access': True
                }
            ]
        else:  # public or planner
            recommendations = [
                {
                    'category': '🚦 Traffic',
                    'title': 'Improve traffic flow',
                    'description': 'Project will increase traffic by 35% during peak hours',
                    'priority': 'High',
                    'mitigation': 'City is considering road widening'
                },
                {
                    'category': '🌳 Environment',
                    'title': 'Air quality impact',
                    'description': 'AQI expected to increase by 30 points',
                    'priority': 'Medium',
                    'mitigation': 'Tree planting planned'
                }
            ]
        
        for rec in recommendations:
            with st.expander(f"{rec['category']}: {rec['title']}"):
                for key, value in rec.items():
                    if key not in ['category', 'title']:
                        st.write(f"**{key.title()}:** {value}")
                
                # Add implement button for admin/enterprise
                if user_role in ['admin', 'enterprise', 'planner']:
                    if st.button(f"Add to Plan", key=rec['title']):
                        st.success("Added to implementation plan!")
    
    # Advanced tab for admin only
    if user_role in ['admin', 'enterprise'] and 'tab5' in locals():
        with tab5:
            st.subheader("⚙️ Advanced Settings")
            
            st.warning("⚠️ These settings affect all analyses")
            
            col1, col2 = st.columns(2)
            with col1:
                st.slider("Model Sensitivity", 0.0, 1.0, 0.5)
                st.slider("Prediction Confidence", 0.0, 1.0, 0.95)
            with col2:
                st.selectbox("Data Source", ["Live API", "Cached", "Historical"])
                st.checkbox("Enable Real-time Updates")
            
            if st.button("Save Settings"):
                st.success("Settings saved!")

else:
    # Welcome screen for authenticated users
    st.info("👈 Enter project details in the sidebar and click 'Analyze Impact' to begin")
    
    # Show role-specific features
    st.subheader(f"Your {user.get('role', '').title()} Dashboard")
    
    if user.get('role') == 'admin':
        st.markdown("""
        - 📊 **System Overview**: Monitor all projects
        - 👥 **User Management**: Manage team access
        - 📈 **Analytics**: Platform usage metrics
        - 🔧 **Configuration**: System settings
        """)
    elif user.get('role') == 'planner':
        st.markdown("""
        - 📋 **Active Projects**: 3 ongoing analyses
        - 📊 **Recent Reports**: 5 this week
        - 👥 **Team Members**: 8 collaborators
        - 📈 **Usage Stats**: 78% of monthly quota
        """)
    elif user.get('role') == 'enterprise':
        st.markdown("""
        - 🔑 **API Keys**: Manage API access
        - 📊 **Bulk Analysis**: Run multiple projects
        - 📈 **Custom Reports**: Export in multiple formats
        - 🤝 **Team Access**: 5 team members
        """)
    else:  # public
        st.markdown("""
        - 📊 **Public Projects**: 12 available
        - 📈 **Community Feedback**: 45 responses
        - 🗺️ **Local Impacts**: 3 near you
        - 📋 **Public Meetings**: 2 upcoming
        """)

# Footer
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"© 2026 Epoch Elites")
with col2:
    st.markdown(f"City Lens v1.0")
with col3:
    st.markdown(f"Logged in as: {user.get('role', '').title()}")
with col4:
    st.markdown(f"Organization: {user.get('organization', 'N/A')}")