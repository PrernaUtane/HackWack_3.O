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
from features.multi_site import render_multi_site

# ===== PAGE CONFIG MUST BE FIRST =====
st.set_page_config(
    page_title="City Lens - Urban Impact Forecasting",
    page_icon="🏙️",
    layout="wide"
)

# ===== NOW add debug info in sidebar (after config) =====
st.sidebar.markdown("### 🔍 DEBUG INFO")
st.sidebar.write("Features loaded:")
st.sidebar.success("✅ Site Comparison")
st.sidebar.success("✅ Correlation Matrix")
st.sidebar.success("✅ Baseline Analysis")
st.sidebar.success("✅ Multi-Site")

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Check authentication FIRST
user = require_auth()

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

# Render sidebar and get project input
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
            # ... (keep your existing quick analysis code here)
            pass

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