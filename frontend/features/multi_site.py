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
from components.metrics import display_metrics_row, create_metric_from_analysis, impact_gauge, kpi_card
from components.timeline import impact_timeline_dashboard
from utils.export import display_export_options

# Import feature modules
from features.site_comparison import render_site_comparison
from features.correlation_matrix import render_correlation_matrix
from features.baseline_analysis import render_baseline_analysis

# Page configuration - THIS MUST BE FIRST
st.set_page_config(
    page_title="City Lens - Urban Impact Forecasting",
    page_icon="🏙️",
    layout="wide"
)

# Load custom CSS - AFTER set_page_config
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Check authentication FIRST
user = require_auth()  # This will redirect to login if not authenticated

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state['analysis_results'] = None
    
# Initialize feature visibility states
if 'show_quick' not in st.session_state:
    st.session_state.show_quick = False
if 'show_site_comparison' not in st.session_state:
    st.session_state.show_site_comparison = False
if 'show_correlation' not in st.session_state:
    st.session_state.show_correlation = False
if 'show_baseline' not in st.session_state:
    st.session_state.show_baseline = False
if 'show_multi' not in st.session_state:
    st.session_state.show_multi = False

# Show user profile in sidebar
show_user_profile()

# Title with user greeting
st.markdown('<h1 class="main-header">🏙️ City Lens</h1>', unsafe_allow_html=True)
st.markdown(f"### Welcome back, {user.get('name', 'User')}! 👋")

# Role-based welcome message
role_messages = {
    'admin': "You have full access to all features.",
    'planner': "Plan and evaluate urban development projects.",
    'enterprise': "Access advanced analytics and API features.",
    'public': "View public impact assessments."
}
st.caption(role_messages.get(user.get('role', 'public'), ""))

# Render sidebar and get project input (only for quick analysis)
analyze_clicked, project_input = render_project_input()

# ============================================
# FEATURE NAVIGATION LOGIC
# ============================================

# Check if any feature is active
active_feature = None
if st.session_state.show_site_comparison:
    active_feature = "site_comparison"
elif st.session_state.show_correlation:
    active_feature = "correlation"
elif st.session_state.show_baseline:
    active_feature = "baseline"
elif st.session_state.show_multi:
    active_feature = "multi"
elif st.session_state.show_quick:
    active_feature = "quick"

# If a feature is active, show it with back button
if active_feature:
    
    # Show back button
    col1, col2 = st.columns([1, 11])
    with col1:
        if st.button("← Back", use_container_width=True):
            # Reset all feature states
            st.session_state.show_quick = False
            st.session_state.show_site_comparison = False
            st.session_state.show_correlation = False
            st.session_state.show_baseline = False
            st.session_state.show_multi = False
            st.rerun()
    
    with col2:
        st.markdown(f"### {active_feature.replace('_', ' ').title()}")
    
    st.markdown("---")
    
    # Render the active feature
    if active_feature == "site_comparison":
        render_site_comparison()
    elif active_feature == "correlation":
        render_correlation_matrix()
    elif active_feature == "baseline":
        render_baseline_analysis()
    elif active_feature == "multi":
        render_multi_site()
    elif active_feature == "quick":
        # Quick analysis (existing functionality)
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
                # Create enhanced metric cards
                metrics_data = [
                    create_metric_from_analysis('traffic', results['traffic_impact'], "+35%"),
                    create_metric_from_analysis('air', results['air_quality'], "+30"),
                    create_metric_from_analysis('property', results['property_change'], "+2.3%"),
                    create_metric_from_analysis('jobs', results['jobs_created'], "+250")
                ]
                
                # Display the metrics row
                display_metrics_row(metrics_data)
                
                # Charts row
                col1, col2 = st.columns(2)
                
                with col1:
                    # Use our custom gauge instead of Plotly
                    st.markdown(
                        impact_gauge(results['congestion_score'] * 100, "Traffic Congestion"),
                        unsafe_allow_html=True
                    )
                
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
                
                # Affected population as KPI card
                st.markdown(
                    kpi_card(
                        "POPULATION AFFECTED",
                        f"{results['population_affected']:,}",
                        "residents within 2-mile radius",
                        "+15%",
                        "up"
                    ),
                    unsafe_allow_html=True
                )
            
            with tab2:
                # Display impact map
                display_impact_map(results)
            
            with tab3:
                st.subheader("📈 Detailed Impact Analysis")
                
                # Add timeline dashboard
                selected_year = impact_timeline_dashboard(results)
                
                # Before/After comparison
                st.markdown("### 📊 Impact Comparison")
                before = [45, 65, 55, 70, 30]
                after = [85, 72, 68, 82, 35]
                
                fig_compare = create_impact_comparison(before, after)
                st.plotly_chart(fig_compare, use_container_width=True)
                
                # Detailed metrics table
                st.markdown("### 📋 Impact Metrics Table")
                metrics_df = pd.DataFrame({
                    'Metric': ['Peak Hour Congestion', 'Average Speed', 'PM2.5 Levels', 'Noise Levels', 'Property Values'],
                    'Current': ['35 min', '25 mph', '12 μg/m³', '65 dB', '$500k'],
                    'Projected': ['55 min (+57%)', '18 mph (-28%)', '22 μg/m³ (+83%)', '78 dB (+20%)', '$560k (+12%)'],
                    'Threshold': ['45 min', '20 mph', '15 μg/m³', '70 dB', 'N/A']
                })
                st.dataframe(metrics_df, use_container_width=True)
                
                # Export options
                display_export_options(results, user, metrics_df)
            
            with tab4:
                st.subheader("💡 AI-Powered Recommendations")
                
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
                
                for i, rec in enumerate(recommendations):
                    # Determine priority class
                    priority_class = "recommendation-priority-high" if rec['priority'] == 'High' else \
                                   "recommendation-priority-medium" if rec['priority'] == 'Medium' else \
                                   "recommendation-priority-low"
                    
                    # Create recommendation card
                    html = f"""
                    <div class="recommendation-card {priority_class}">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                            <span style="color: #F1F5F9; font-weight: 600;">{rec['category']} {rec['title']}</span>
                            <span class="metric-badge metric-badge-{rec['priority'].lower()}">{rec['priority']} Priority</span>
                        </div>
                        <p style="color: #94A3B8; margin-bottom: 1rem;">{rec['description']}</p>
                    """
                    
                    # Add details based on role
                    if user_role in ['admin', 'enterprise', 'planner']:
                        html += f"""
                        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
                            <span style="color: #64748B;">💰 Cost: {rec.get('cost', 'N/A')}</span>
                            <span style="color: #64748B;">📊 Impact: {rec.get('impact', 'N/A')}</span>
                            <span style="color: #64748B;">📈 ROI: {rec.get('roi', 'N/A')}</span>
                        </div>
                        """
                    
                    html += "</div>"
                    
                    st.markdown(html, unsafe_allow_html=True)
                    
                    # Add implement button for admin/enterprise
                    if user_role in ['admin', 'enterprise', 'planner']:
                        col1, col2, col3 = st.columns([1, 1, 5])
                        with col1:
                            if st.button(f"✅ Implement", key=f"impl_{i}"):
                                st.success("Added to implementation plan!")
                        with col2:
                            if st.button(f"📅 Schedule", key=f"sch_{i}"):
                                st.info("Schedule feature coming soon")
            
            # Advanced tab for admin/enterprise only
            if user_role in ['admin', 'enterprise'] and 'tab5' in locals():
                with tab5:
                    st.subheader("⚙️ Advanced Settings")
                    
                    st.warning("⚠️ These settings affect all analyses")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        sensitivity = st.slider("Model Sensitivity", 0.0, 1.0, 0.5, 0.1)
                        confidence = st.slider("Prediction Confidence", 0.0, 1.0, 0.95, 0.05)
                    with col2:
                        data_source = st.selectbox("Data Source", ["Live API", "Cached", "Historical"])
                        realtime = st.checkbox("Enable Real-time Updates", value=True)
                    
                    # API Key management for enterprise
                    if user_role == 'enterprise':
                        st.subheader("🔑 API Access")
                        st.code("YOUR_API_KEY: city_lens_ent_2026_xyz789", language="text")
                        if st.button("Regenerate API Key"):
                            st.warning("This would generate a new key in production")
                    
                    if st.button("💾 Save Settings", type="primary"):
                        st.success("Settings saved successfully!")
        
        else:
            # Quick analysis input screen
            st.info("👈 Enter project details in the sidebar and click 'Analyze Impact' to begin")

# ============================================
# DASHBOARD WITH FEATURE CARDS
# ============================================
else:
    # Welcome screen with feature cards
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0 3rem 0;">
        <h2 style="color: #F1F5F9; font-size: 2rem;">Welcome to City Lens</h2>
        <p style="color: #94A3B8; font-size: 1.1rem;">Select a feature to begin your analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create feature cards in a grid
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        # Quick Analysis Card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                    padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                    margin-bottom: 1.5rem; cursor: pointer; transition: all 0.3s;
                    border-left: 4px solid #06B6D4; height: 220px;
                    display: flex; flex-direction: column;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">⚡</div>
            <h3 style="color: #F1F5F9; margin: 0; font-size: 1.5rem;">Quick Analysis</h3>
            <p style="color: #94A3B8; flex: 1;">Single site impact assessment with real-time predictions</p>
            <div style="color: #06B6D4; font-size: 0.9rem; font-weight: 500;">Click to start →</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ Start Quick Analysis", key="quick_btn", use_container_width=True):
            st.session_state.show_quick = True
            st.rerun()
    
    with row1_col2:
        # Site Comparison Card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                    padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                    margin-bottom: 1.5rem; cursor: pointer; transition: all 0.3s;
                    border-left: 4px solid #F59E0B; height: 220px;
                    display: flex; flex-direction: column;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔄</div>
            <h3 style="color: #F1F5F9; margin: 0; font-size: 1.5rem;">Site Comparison</h3>
            <p style="color: #94A3B8; flex: 1;">Compare multiple development sites side-by-side</p>
            <div style="color: #F59E0B; font-size: 0.9rem; font-weight: 500;">Click to open →</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 Open Site Comparison", key="site_btn", use_container_width=True):
            st.session_state.show_site_comparison = True
            st.rerun()
    
    # Second row
    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        # Correlation Matrix Card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                    padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                    margin-bottom: 1.5rem; cursor: pointer; transition: all 0.3s;
                    border-left: 4px solid #10B981; height: 220px;
                    display: flex; flex-direction: column;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📈</div>
            <h3 style="color: #F1F5F9; margin: 0; font-size: 1.5rem;">Correlation Matrix</h3>
            <p style="color: #94A3B8; flex: 1;">Understand relationships between traffic, environment & socioeconomics</p>
            <div style="color: #10B981; font-size: 0.9rem; font-weight: 500;">Click to open →</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📈 Open Correlation Matrix", key="corr_btn", use_container_width=True):
            st.session_state.show_correlation = True
            st.rerun()
    
    with row2_col2:
        # Baseline Analysis Card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                    padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                    margin-bottom: 1.5rem; cursor: pointer; transition: all 0.3s;
                    border-left: 4px solid #EF4444; height: 220px;
                    display: flex; flex-direction: column;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📉</div>
            <h3 style="color: #F1F5F9; margin: 0; font-size: 1.5rem;">Baseline Analysis</h3>
            <p style="color: #94A3B8; flex: 1;">Compare with vs without development scenarios</p>
            <div style="color: #EF4444; font-size: 0.9rem; font-weight: 500;">Click to open →</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📉 Open Baseline Analysis", key="base_btn", use_container_width=True):
            st.session_state.show_baseline = True
            st.rerun()
    
    # Third row
    row3_col1, row3_col2 = st.columns(2)
    
    with row3_col1:
        # Multi-Site Analytics Card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                    padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                    margin-bottom: 1.5rem; cursor: pointer; transition: all 0.3s;
                    border-left: 4px solid #8B5CF6; height: 220px;
                    display: flex; flex-direction: column;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h3 style="color: #F1F5F9; margin: 0; font-size: 1.5rem;">Multi-Site Analytics</h3>
            <p style="color: #94A3B8; flex: 1;">Portfolio-level insights and optimal site selection</p>
            <div style="color: #8B5CF6; font-size: 0.9rem; font-weight: 500;">Click to open →</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📊 Open Multi-Site Analytics", key="multi_btn", use_container_width=True):
            st.session_state.show_multi = True
            st.rerun()
    
    with row3_col2:
        # Reports & Export Card
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                    padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                    margin-bottom: 1.5rem; opacity: 0.7;
                    border-left: 4px solid #94A3B8; height: 220px;
                    display: flex; flex-direction: column;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
            <h3 style="color: #F1F5F9; margin: 0; font-size: 1.5rem;">Reports & Export</h3>
            <p style="color: #94A3B8; flex: 1;">Generate comprehensive reports and export data</p>
            <div style="color: #94A3B8; font-size: 0.9rem;">Coming Soon</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats row
    st.markdown("---")
    st.markdown("### 📊 Platform Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="color: #06B6D4; font-size: 2rem; font-weight: 600;">156</div>
            <div style="color: #94A3B8;">Analyses This Week</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="color: #F59E0B; font-size: 2rem; font-weight: 600;">24</div>
            <div style="color: #94A3B8;">Active Projects</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="color: #10B981; font-size: 2rem; font-weight: 600;">12</div>
            <div style="color: #94A3B8;">Cities Covered</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px; text-align: center;">
            <div style="color: #EF4444; font-size: 2rem; font-weight: 600;">89%</div>
            <div style="color: #94A3B8;">Accuracy Rate</div>
        </div>
        """, unsafe_allow_html=True)
def render_multi_site():
    """
    Main function to render multi-site analytics
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                padding: 2rem; border-radius: 16px; border-left: 6px solid #8B5CF6;
                margin-bottom: 2rem;">
        <h2 style="color: #F1F5F9; margin: 0;">📊 Multi-Site Analytics</h2>
        <p style="color: #94A3B8;">Compare performance across multiple development sites</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample site data
    np.random.seed(42)
    
    sites = [
        "Downtown Tower", "Riverside Complex", "Suburban Heights", 
        "Tech Park", "Harbor View", "Central Plaza", "Green Meadows",
        "Innovation Hub", "Heritage Square", "Metro Center"
    ]
    
    site_data = []
    for i, site in enumerate(sites):
        site_data.append({
            'Site': site,
            'Traffic Impact': np.random.randint(30, 90),
            'Environmental Impact': np.random.randint(20, 85),
            'Socioeconomic Impact': np.random.randint(40, 95),
            'Infrastructure Strain': np.random.randint(25, 80),
            'Cost Efficiency': np.random.randint(50, 95),
            'Community Support': np.random.randint(30, 90),
            'ROI Potential': np.random.randint(40, 98),
            'Timeline (months)': np.random.randint(12, 48),
            'Budget ($M)': np.random.randint(10, 200)
        })
    
    df = pd.DataFrame(site_data)
    
    # Simple display
    st.dataframe(df)
    
    st.info("Multi-site analytics dashboard coming soon! This is a placeholder.")
# Footer
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("© 2026 Epoch Elites")
with col2:
    st.markdown("City Lens v3.0 - Feature Dashboard")
with col3:
    st.markdown(f"Logged in as: {user.get('role', '').title()}")
with col4:
    st.markdown(f"Organization: {user.get('organization', 'N/A')}")