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

# Import components - USING YOUR NEW AUTH
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

# Page configuration - MUST BE FIRST
st.set_page_config(
    page_title="City Lens - Urban Impact Platform",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Check authentication - THIS WILL SHOW YOUR NEW LOGIN PAGE
user = require_auth()

# Initialize session states
if 'analysis_results' not in st.session_state:
    st.session_state['analysis_results'] = None

# Feature visibility states - ONLY 6 FEATURES
feature_keys = ['show_quick', 'show_site_comparison', 'show_correlation', 
                'show_baseline', 'show_multi', 'show_reports']
for key in feature_keys:
    if key not in st.session_state:
        st.session_state[key] = False

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
                    with st.spinner("Analyzing impacts..."):
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
                user_role = user.get('role', 'public')
                
                # Tabs
                tabs = ["📊 Overview", "🗺️ Map", "📈 Analysis", "💡 Recommendations"]
                if user_role in ['admin', 'enterprise']:
                    tabs.append("⚙️ Settings")
                
                tab1, tab2, tab3, tab4, *rest = st.tabs(tabs)
                
                with tab1:
                    # Metrics row
                    metrics_data = [
                        create_metric_from_analysis('traffic', results['traffic_impact'], "+35%"),
                        create_metric_from_analysis('air', results['air_quality'], "+30"),
                        create_metric_from_analysis('property', results['property_change'], "+2.3%"),
                        create_metric_from_analysis('jobs', results['jobs_created'], "+250")
                    ]
                    display_metrics_row(metrics_data)
                    
                    # Charts
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(impact_gauge(results['congestion_score'] * 100, "Traffic Congestion"),
                                  unsafe_allow_html=True)
                    with col2:
                        impact_scores = {
                            'Traffic': 85, 'Environment': 72, 'Socioeconomic': 45,
                            'Infrastructure': 68, 'Community': 35
                        }
                        fig_breakdown = create_impact_breakdown(impact_scores)
                        st.plotly_chart(fig_breakdown, use_container_width=True)
                    
                    st.markdown(kpi_card("Population Affected", f"{results['population_affected']:,}",
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
                        priority_class = "metric-badge-critical" if rec['priority'] == 'High' else \
                                       "metric-badge-warning" if rec['priority'] == 'Medium' else \
                                       "metric-badge-success"
                        
                        st.markdown(f"""
                        <div style="background: var(--bg-card); padding: 1.5rem; 
                                    border-radius: var(--radius-lg); border: 1px solid var(--border); margin-bottom: 1rem;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                                <span style="color: var(--text-primary); font-weight: 600;">{rec['category']} {rec['title']}</span>
                                <span class="metric-badge {priority_class}">{rec['priority']} Priority</span>
                            </div>
                            <p style="color: var(--text-secondary); margin-bottom: 1rem;">{rec['description']}</p>
                        """, unsafe_allow_html=True)
                        
                        if user_role in ['admin', 'enterprise', 'planner']:
                            st.markdown(f"""
                            <div style="display: flex; gap: 2rem; margin-bottom: 1rem;">
                                <span style="color: var(--text-muted);">💰 Cost: {rec.get('cost', 'N/A')}</span>
                                <span style="color: var(--text-muted);">📊 Impact: {rec.get('impact', 'N/A')}</span>
                                <span style="color: var(--text-muted);">📈 ROI: {rec.get('roi', 'N/A')}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns([1, 1, 8])
                        with col1:
                            if st.button(f"✅ Implement", key=f"impl_quick_{i}", use_container_width=True):
                                st.success("Added to implementation plan!")
                        with col2:
                            if st.button(f"📅 Schedule", key=f"sch_quick_{i}", use_container_width=True):
                                st.info("Schedule feature coming soon")
            
            else:
                st.info("👈 Enter project details in the sidebar")
        
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
        # DASHBOARD WITH EXACTLY 6 FEATURE CARDS
        st.markdown("""
        <div style="text-align: center; margin: 2rem 0 3rem 0;">
            <h2 style="color: #F1F5F9; font-size: 2rem;">What would you like to analyze today?</h2>
            <p style="color: #94A3B8;">Select a feature to get started</p>
        </div>
        """, unsafe_allow_html=True)
        
        # FIRST ROW - 2 cards
        col1, col2 = st.columns(2)
        
        with col1:
            # Card 1: Quick Analysis
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
            
            # Button
            if st.button("⚡ Start Quick Analysis", key="quick_btn", use_container_width=True):
                st.session_state.show_quick = True
                st.rerun()
        
        with col2:
            # Card 2: Site Comparison
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">🔄</div>
                <h3 style="color: #F1F5F9; margin: 0;">Site Comparison</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Compare multiple development sites side-by-side</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Button
            if st.button("🔄 Compare Sites", key="site_btn", use_container_width=True):
                st.session_state.show_site_comparison = True
                st.rerun()
        
        # SECOND ROW - 2 cards
        col1, col2 = st.columns(2)
        
        with col1:
            # Card 3: Correlation Matrix
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
                <h3 style="color: #F1F5F9; margin: 0;">Correlation Matrix</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Understand relationships between impact factors</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Button
            if st.button("📊 View Correlations", key="corr_btn", use_container_width=True):
                st.session_state.show_correlation = True
                st.rerun()
        
        with col2:
            # Card 4: Baseline Analysis
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📉</div>
                <h3 style="color: #F1F5F9; margin: 0;">Baseline Analysis</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Compare with vs without development scenarios</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Button
            if st.button("📉 Analyze Baseline", key="base_btn", use_container_width=True):
                st.session_state.show_baseline = True
                st.rerun()
        
        # THIRD ROW - 2 cards
        col1, col2 = st.columns(2)
        
        with col1:
            # Card 5: Multi-Site Analytics
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📈</div>
                <h3 style="color: #F1F5F9; margin: 0;">Multi-Site Analytics</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Portfolio-level insights and optimal site selection</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Button
            if st.button("📈 Explore Portfolio", key="multi_btn", use_container_width=True):
                st.session_state.show_multi = True
                st.rerun()
        
        with col2:
            # Card 6: Reports & Export
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 2rem; border-radius: 16px; border: 1px solid #334155;
                        margin-bottom: 1rem; opacity: 0.7;">
                <div style="font-size: 2.5rem; margin-bottom: 1rem;">📋</div>
                <h3 style="color: #F1F5F9; margin: 0;">Reports & Export</h3>
                <p style="color: #94A3B8; margin: 0.5rem 0 1rem 0;">Generate comprehensive reports and export data</p>
                <span style="background: #2A2A3A; padding: 0.25rem 0.75rem; border-radius: 999px; color: #94A3B8; font-size: 0.75rem;">Coming Soon</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Button (disabled for now)
            if st.button("📋 Coming Soon", key="reports_btn", disabled=True, use_container_width=True):
                pass
        
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