# -*- coding: utf-8 -*-
"""
City Lens - Professional Urban Impact Forecasting System
Version 3.0 - Enterprise Grade
Team: Epoch Elites
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Import components
from components.auth import require_auth
from components.sidebar import render_project_input
from components.map_view import display_impact_map
from components.charts import (
    create_congestion_gauge,
    create_impact_breakdown,
    create_impact_comparison
)
from components.metrics import display_metrics_row, create_metric_from_analysis, impact_gauge, kpi_card
from components.timeline import impact_timeline_dashboard
from components.navigation import render_navigation, render_header, render_footer
from utils.export import display_export_options

# Import feature modules
from features.site_comparison import render_site_comparison
from features.correlation_matrix import render_correlation_matrix
from features.baseline_analysis import render_baseline_analysis
from features.multi_site import render_multi_site

# Import API client
from utils.api_clients import get_api_client

# Page configuration
st.set_page_config(
    page_title="City Lens - Urban Impact Platform",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Check authentication (standalone - uses local JSON)
user = require_auth()

# Initialize session states
if 'analysis_results' not in st.session_state:
    st.session_state['analysis_results'] = None

# Feature visibility states
feature_keys = ['show_quick', 'show_site_comparison', 'show_correlation', 
                'show_baseline', 'show_multi', 'show_reports']
for key in feature_keys:
    if key not in st.session_state:
        st.session_state[key] = False

# Initialize user projects if not exists
if 'user_projects' not in st.session_state:
    st.session_state.user_projects = []

# Render navigation sidebar
render_navigation()

# Main content area
with st.container():
    # Header
    render_header()
    
    # Determine active feature
    active_feature = None
    for key in feature_keys:
        if st.session_state[key]:
            active_feature = key.replace('show_', '')
            break
    
    # Show active feature or dashboard
    if active_feature:
        # Back button
        col1, col2 = st.columns([1, 11])
        with col1:
            if st.button("← Back", key="back_to_dashboard_btn", use_container_width=True):
                for key in feature_keys:
                    st.session_state[key] = False
                st.rerun()
        
        with col2:
            feature_name = active_feature.replace('_', ' ').title()
            st.markdown(f"### {feature_name}")
        
        st.markdown("---")
        
        # Render feature
        if active_feature == 'quick':
            # Quick Analysis
            analyze_clicked, project_input = render_project_input()
            
            if analyze_clicked or st.session_state['analysis_results']:
                if analyze_clicked:
                    with st.spinner("🔮 Analyzing impacts with backend..."):
                        # Get API client
                        api = get_api_client()
                        
                        # Prepare project data for API
                        project_data = {
                            "project_type": project_input.get('type', 'commercial').lower().replace(' ', '_'),
                            "size_sqft": project_input.get('size', 50000),
                            "latitude": project_input.get('latitude', 40.7128),
                            "longitude": project_input.get('longitude', -74.0060),
                            "city": project_input.get('city', 'New York'),
                            "height": project_input.get('height', 50),
                            "parking_spaces": project_input.get('parking', 100),
                            "green_space_percent": project_input.get('green_space', 15)
                        }
                        
                        # Call API
                        results = api.simulate(project_data)
                        
                        if results:
                            # Transform API response to frontend format
                            st.session_state['analysis_results'] = {
                                'latitude': project_input.get('latitude', 40.7128),
                                'longitude': project_input.get('longitude', -74.0060),
                                'project_name': project_input.get('name', 'New Project'),
                                'project_type': project_input.get('type', 'Commercial'),
                                'congestion_score': results['traffic']['congestion_score'],
                                'traffic_impact': results['traffic']['congestion_score'] * 100,
                                'air_quality': results['environmental']['air_quality_index'],
                                'property_change': results['socioeconomic']['property_value_change_percent'],
                                'jobs_created': results['socioeconomic']['jobs_created_permanent'],
                                'population_affected': results['socioeconomic']['population_change'],
                                'recommendations': results['recommendations'],
                                'unified_score': results['unified_impact_score'],
                                'simulation_id': results.get('simulation_id'),
                                'timestamp': results.get('timestamp'),
                                'congestion_hotspots': [
                                    {'lat': project_input.get('latitude', 40.7128), 
                                     'lon': project_input.get('longitude', -74.0060), 
                                     'intensity': results['traffic']['congestion_score']}
                                ]
                            }
                            st.success(f"✅ Analysis complete! Unified Score: {results['unified_impact_score']}")
                        else:
                            st.error("❌ Analysis failed. Using fallback data.")
                            # Fallback to mock data
                            st.session_state['analysis_results'] = {
                                'latitude': project_input.get('latitude', 40.7128),
                                'longitude': project_input.get('longitude', -74.0060),
                                'project_name': project_input.get('name', 'New Project'),
                                'project_type': project_input.get('type', 'Commercial'),
                                'congestion_score': 0.75,
                                'traffic_impact': 85,
                                'air_quality': 145,
                                'property_change': 12,
                                'jobs_created': 250,
                                'population_affected': 15000,
                                'recommendations': ["Standard monitoring recommended", 
                                                   "Consider traffic calming measures"],
                                'unified_score': 75,
                                'congestion_hotspots': [
                                    {'lat': 40.7128, 'lon': -74.0060, 'intensity': 0.9},
                                    {'lat': 40.7138, 'lon': -74.0070, 'intensity': 0.8},
                                ]
                            }
                
                results = st.session_state['analysis_results']
                user_role = user.get('role', 'public')
                
                # Tabs
                tabs = ["📊 Overview", "🗺️ Map", "📈 Analysis", "💡 Recommendations"]
                if user_role in ['admin', 'enterprise']:
                    tabs.append("⚙️ Settings")
                
                tab1, tab2, tab3, tab4, *rest = st.tabs(tabs)
                
                with tab1:
                    # Metrics row
                    metrics_data = [
                        create_metric_from_analysis('traffic', results.get('traffic_impact', 85), "+35%"),
                        create_metric_from_analysis('air', results.get('air_quality', 145), "+30"),
                        create_metric_from_analysis('property', results.get('property_change', 12), "+2.3%"),
                        create_metric_from_analysis('jobs', results.get('jobs_created', 250), "+250")
                    ]
                    display_metrics_row(metrics_data)
                    
                    # Charts
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(impact_gauge(results.get('congestion_score', 0.75) * 100, "Traffic Congestion"),
                                  unsafe_allow_html=True)
                    with col2:
                        impact_scores = {
                            'Traffic': results.get('traffic_impact', 85),
                            'Environment': 72,
                            'Socioeconomic': 45,
                            'Infrastructure': 68,
                            'Community': 35
                        }
                        fig_breakdown = create_impact_breakdown(impact_scores)
                        st.plotly_chart(fig_breakdown, use_container_width=True)
                    
                    st.markdown(kpi_card("Population Affected", f"{results.get('population_affected', 15000):,}",
                                        "residents within 2-mile radius", "+15%", "up"),
                              unsafe_allow_html=True)
                
                with tab2:
                    display_impact_map(results)
                
                with tab3:
                    st.subheader("Detailed Analysis")
                    selected_year = impact_timeline_dashboard(results)
                    
                    # Comparison chart
                    before = [45, 65, 55, 70, 30]
                    after = [85, 72, 68, 82, 35]
                    fig_compare = create_impact_comparison(before, after)
                    st.plotly_chart(fig_compare, use_container_width=True)
                    
                    # Metrics table
                    metrics_df = pd.DataFrame({
                        'Metric': ['Peak Congestion', 'Avg Speed', 'PM2.5', 'Noise', 'Property'],
                        'Current': ['35 min', '25 mph', '12 µg/m³', '65 dB', '$500k'],
                        'Projected': ['55 min (+57%)', '18 mph (-28%)', '22 µg/m³ (+83%)', 
                                     '78 dB (+20%)', '$560k (+12%)'],
                        'Threshold': ['45 min', '20 mph', '15 µg/m³', '70 dB', 'N/A']
                    })
                    st.dataframe(metrics_df, use_container_width=True)
                    display_export_options(results, user, metrics_df)
                
                with tab4:
                    st.subheader("AI Recommendations")
                    
                    # Get recommendations from API or use defaults
                    recommendations = results.get('recommendations', [
                        "Monitor traffic patterns post-construction",
                        "Consider adding green buffer zones",
                        "Evaluate public transit options"
                    ])
                    
                    for i, rec in enumerate(recommendations[:3]):
                        st.markdown(f"""
                        <div style="background: #1E1E2D; padding: 1.5rem; 
                                    border-radius: 12px; border: 1px solid #2A2A3A; margin-bottom: 1rem;
                                    border-left: 4px solid #059669;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span style="color: #F1F5F9; font-weight: 600;">💡 Recommendation {i+1}</span>
                                <span class="metric-badge metric-badge-success">AI Generated</span>
                            </div>
                            <p style="color: #94A3B8;">{rec}</p>
                        </div>
                        """, unsafe_allow_html=True)
            
            else:
                st.info("👈 Enter project details in the sidebar or select a project from My Projects")
        
        elif active_feature == 'site_comparison':
            render_site_comparison()
        elif active_feature == 'correlation':
            render_correlation_matrix()
        elif active_feature == 'baseline':
            render_baseline_analysis()
        elif active_feature == 'multi':
            render_multi_site()
        elif active_feature == 'reports':
            st.info("📋 Reports feature coming soon!")
    
    else:
        # DASHBOARD WITH FEATURE CARDS
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0 3rem 0;">
            <h2 style="color: #F1F5F9; font-size: 2rem;">What would you like to analyze today?</h2>
            <p style="color: #94A3B8;">Select a feature to get started</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature cards grid
        col1, col2 = st.columns(2)
        
        with col1:
            # Quick Analysis Card
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem; border-left: 4px solid #6366F1;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">⚡</div>
                <h3 style="color: #F1F5F9; margin: 0;">Quick Analysis</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Single site impact assessment with real-time predictions</p>
                <span style="background: #2A2A3A; padding: 0.25rem 0.75rem; border-radius: 999px; color: #6366F1; font-size: 0.75rem;">Popular</span>
            </div>
            """, unsafe_allow_html=True)
            if st.button("⚡ Start Quick Analysis", key="quick_btn", use_container_width=True):
                st.session_state.show_quick = True
                st.rerun()
        
        with col2:
            # Site Comparison Card
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔄</div>
                <h3 style="color: #F1F5F9; margin: 0;">Site Comparison</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Compare multiple development sites side-by-side</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 Compare Sites", key="site_btn", use_container_width=True):
                st.session_state.show_site_comparison = True
                st.rerun()
        
        # Second row
        col1, col2 = st.columns(2)
        
        with col1:
            # Correlation Matrix Card
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
                <h3 style="color: #F1F5F9; margin: 0;">Correlation Matrix</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Understand relationships between impact factors</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📊 View Correlations", key="corr_btn", use_container_width=True):
                st.session_state.show_correlation = True
                st.rerun()
        
        with col2:
            # Baseline Analysis Card
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📉</div>
                <h3 style="color: #F1F5F9; margin: 0;">Baseline Analysis</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Compare with vs without development scenarios</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📉 Analyze Baseline", key="base_btn", use_container_width=True):
                st.session_state.show_baseline = True
                st.rerun()
        
        # Third row
        col1, col2 = st.columns(2)
        
        with col1:
            # Multi-Site Analytics Card
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📈</div>
                <h3 style="color: #F1F5F9; margin: 0;">Multi-Site Analytics</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Portfolio-level insights and optimal site selection</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📈 Explore Portfolio", key="multi_btn", use_container_width=True):
                st.session_state.show_multi = True
                st.rerun()
        
        with col2:
            # Reports Card
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem; opacity: 0.7;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📋</div>
                <h3 style="color: #F1F5F9; margin: 0;">Reports & Export</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Generate comprehensive reports</p>
                <span style="background: #2A2A3A; padding: 0.25rem 0.75rem; border-radius: 999px; color: #94A3B8; font-size: 0.75rem;">Coming Soon</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Stats section
        st.markdown("---")
        st.markdown("### Platform Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px;">
                <div style="color: #6366F1; font-size: 2rem; font-weight: 600;">156</div>
                <div style="color: #94A3B8;">Analyses This Week</div>
                <div style="color: #10B981; font-size: 0.875rem;">↑ +12%</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px;">
                <div style="color: #F59E0B; font-size: 2rem; font-weight: 600;">24</div>
                <div style="color: #94A3B8;">Active Projects</div>
                <div style="color: #10B981; font-size: 0.875rem;">↑ +3</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px;">
                <div style="color: #10B981; font-size: 2rem; font-weight: 600;">12</div>
                <div style="color: #94A3B8;">Cities Covered</div>
                <div style="color: #10B981; font-size: 0.875rem;">↑ +2</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px;">
                <div style="color: #EF4444; font-size: 2rem; font-weight: 600;">89%</div>
                <div style="color: #94A3B8;">Accuracy Rate</div>
                <div style="color: #10B981; font-size: 0.875rem;">↑ +5%</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    render_footer()