# -*- coding: utf-8 -*-
"""
Site Comparison Tool - Compare multiple development sites
Click to open from main dashboard
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

def render_site_comparison():
    """
    Main function to render the site comparison tool
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                padding: 2rem; border-radius: 16px; border-left: 6px solid #06B6D4;
                margin-bottom: 2rem;">
        <h2 style="color: #F1F5F9; margin: 0;">🔄 Site Comparison Tool</h2>
        <p style="color: #94A3B8;">Compare multiple potential sites for your development project</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for sites
    if 'comparison_sites' not in st.session_state:
        st.session_state.comparison_sites = []
    
    # Site input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🏗️ Add Site for Comparison")
        
        # Site details form
        with st.form("add_site_form"):
            site_name = st.text_input("Site Name", placeholder="e.g., Downtown Location A")
            site_address = st.text_input("Address", placeholder="Enter address or coordinates")
            
            col_a, col_b = st.columns(2)
            with col_a:
                site_type = st.selectbox("Project Type", 
                    ["Commercial", "Residential", "Mixed-Use", "Industrial", "Infrastructure"])
            with col_b:
                site_size = st.number_input("Size (sq ft)", min_value=1000, value=50000, step=1000)
            
            # Impact scores (manual entry for demo - in production would come from API)
            st.markdown("##### 📊 Impact Scores (0-100)")
            col1a, col1b, col1c = st.columns(3)
            with col1a:
                traffic_score = st.slider("Traffic Impact", 0, 100, 50)
                env_score = st.slider("Environmental Impact", 0, 100, 50)
            with col1b:
                socio_score = st.slider("Socioeconomic Impact", 0, 100, 50)
                infra_score = st.slider("Infrastructure Impact", 0, 100, 50)
            with col1c:
                cost_score = st.slider("Cost Factor", 0, 100, 50)
                roi_score = st.slider("ROI Potential", 0, 100, 50)
            
            submitted = st.form_submit_button("➕ Add to Comparison", use_container_width=True)
            
            if submitted and site_name:
                new_site = {
                    'name': site_name,
                    'address': site_address,
                    'type': site_type,
                    'size': site_size,
                    'scores': {
                        'Traffic': traffic_score,
                        'Environmental': env_score,
                        'Socioeconomic': socio_score,
                        'Infrastructure': infra_score,
                        'Cost': cost_score,
                        'ROI': roi_score
                    },
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.comparison_sites.append(new_site)
                st.success(f"✅ Added {site_name} to comparison")
    
    with col2:
        # Show current sites count
        st.markdown("### 📋 Sites to Compare")
        st.markdown(f"""
        <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px; 
                    text-align: center; border: 1px solid #334155;">
            <div style="font-size: 3rem; color: #06B6D4;">{len(st.session_state.comparison_sites)}</div>
            <div style="color: #94A3B8;">Sites Added</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🗑️ Clear All Sites"):
            st.session_state.comparison_sites = []
            st.rerun()
    
    # Display comparison if we have sites
    if st.session_state.comparison_sites:
        st.markdown("---")
        st.markdown("### 📊 Site Comparison Analysis")
        
        # Create tabs for different views
        comp_tab1, comp_tab2, comp_tab3, comp_tab4 = st.tabs([
            "📊 Score Comparison", 
            "📈 Radar Chart", 
            "🏆 Ranking",
            "📋 Detailed Table"
        ])
        
        with comp_tab1:
            # Bar chart comparison
            sites = st.session_state.comparison_sites
            categories = list(sites[0]['scores'].keys())
            
            fig = go.Figure()
            
            for site in sites:
                fig.add_trace(go.Bar(
                    name=site['name'],
                    x=categories,
                    y=[site['scores'][cat] for cat in categories],
                    text=[site['scores'][cat] for cat in categories],
                    textposition='outside'
                ))
            
            fig.update_layout(
                title="Site Comparison - Impact Scores",
                xaxis_title="Impact Categories",
                yaxis_title="Score (0-100)",
                barmode='group',
                plot_bgcolor='#1E293B',
                paper_bgcolor='#1E293B',
                font=dict(color='#F1F5F9'),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Best for each category
            st.markdown("### 🏅 Best Performer by Category")
            cols = st.columns(len(categories))
            for i, cat in enumerate(categories):
                with cols[i]:
                    best_site = max(sites, key=lambda x: x['scores'][cat])
                    st.markdown(f"""
                    <div style="background: #1E293B; padding: 1rem; border-radius: 8px; 
                                text-align: center; border-left: 4px solid #06B6D4;">
                        <div style="color: #94A3B8; font-size: 0.75rem;">{cat}</div>
                        <div style="color: #F1F5F9; font-weight: 600;">{best_site['name']}</div>
                        <div style="color: #06B6D4; font-size: 1.25rem;">{best_site['scores'][cat]}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with comp_tab2:
            # Radar chart comparison
            fig = go.Figure()
            
            for site in sites:
                fig.add_trace(go.Scatterpolar(
                    r=[site['scores'][cat] for cat in categories],
                    theta=categories,
                    fill='toself',
                    name=site['name']
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                plot_bgcolor='#1E293B',
                paper_bgcolor='#1E293B',
                font=dict(color='#F1F5F9'),
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with comp_tab3:
            # Ranking table
            st.markdown("### 🏆 Overall Site Ranking")
            
            # Calculate weighted scores
            weights = {'Traffic': 0.2, 'Environmental': 0.2, 'Socioeconomic': 0.2, 
                      'Infrastructure': 0.15, 'Cost': 0.1, 'ROI': 0.15}
            
            ranked_sites = []
            for site in sites:
                weighted_score = sum(site['scores'][cat] * weights[cat] for cat in categories)
                ranked_sites.append({
                    'Site': site['name'],
                    'Type': site['type'],
                    'Size': f"{site['size']:,} sq ft",
                    **site['scores'],
                    'Weighted Score': round(weighted_score, 1)
                })
            
            df = pd.DataFrame(ranked_sites)
            df = df.sort_values('Weighted Score', ascending=False)
            
            # Display as styled dataframe
            st.dataframe(df, use_container_width=True)
            
            # Recommendation
            best_site = df.iloc[0]['Site']
            best_score = df.iloc[0]['Weighted Score']
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #065986, #0F172A); 
                        padding: 2rem; border-radius: 16px; margin-top: 1rem;
                        border: 1px solid #06B6D4;">
                <h3 style="color: #F1F5F9; margin: 0;">🎯 RECOMMENDATION</h3>
                <p style="color: #94A3B8; font-size: 1.1rem; margin-top: 0.5rem;">
                    Based on weighted analysis, <span style="color: #06B6D4; font-weight: 600;">{best_site}</span>
                    is the optimal location with a score of <span style="color: #06B6D4;">{best_score}</span>/100.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with comp_tab4:
            st.markdown("### 📋 Detailed Site Information")
            
            for site in sites:
                with st.expander(f"📍 {site['name']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Address:** {site['address']}")
                        st.markdown(f"**Type:** {site['type']}")
                        st.markdown(f"**Size:** {site['size']:,} sq ft")
                    with col2:
                        st.markdown(f"**Added:** {site['timestamp']}")
                    
                    # Mini radar for each site
                    fig = go.Figure(data=go.Scatterpolar(
                        r=[site['scores'][cat] for cat in categories],
                        theta=categories,
                        fill='toself',
                        name=site['name']
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=False,
                        height=300,
                        margin=dict(l=80, r=80, t=20, b=20)
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    else:
        # Empty state
        st.markdown("""
        <div style="text-align: center; padding: 4rem; background: #1E293B; 
                    border-radius: 16px; border: 2px dashed #334155;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🏗️</div>
            <h3 style="color: #F1F5F9;">No Sites Added Yet</h3>
            <p style="color: #94A3B8;">Use the form to add sites for comparison</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Export options
    if st.session_state.comparison_sites:
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("📥 Export Comparison Report", use_container_width=True):
                st.success("Report generated! (Demo - would download CSV/PDF)")
        with col2:
            if st.button("🔄 Share Results", use_container_width=True):
                st.info("Sharing link copied to clipboard!")
        with col3:
            if st.button("🔍 Detailed Analysis", use_container_width=True):
                st.session_state.show_detailed = True