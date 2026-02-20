# -*- coding: utf-8 -*-
"""
Multi-Site Analytics Feature for City Lens
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

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
    
    # Tabs for different analytics
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Site Portfolio",
        "📈 Performance Matrix",
        "🎯 Optimal Selection",
        "📋 Comparative Analysis"
    ])
    
    with tab1:
        st.markdown("### 📊 Site Portfolio Overview")
        
        # Metrics selector
        metrics = ['Traffic Impact', 'Environmental Impact', 'Socioeconomic Impact', 
                  'Infrastructure Strain', 'Cost Efficiency', 'ROI Potential']
        
        selected_metrics = st.multiselect(
            "Select metrics to display",
            metrics,
            default=metrics[:3]
        )
        
        if selected_metrics:
            # Create parallel coordinates plot
            dimensions = []
            for metric in selected_metrics:
                dimensions.append(
                    dict(
                        range=[df[metric].min(), df[metric].max()],
                        label=metric,
                        values=df[metric].tolist()
                    )
                )
            
            fig = go.Figure(data=go.Parcoords(
                line=dict(color=df.index, colorscale='Viridis'),
                dimensions=dimensions
            ))
            
            fig.update_layout(
                title="Multi-Dimensional Site Comparison",
                plot_bgcolor='#1E293B',
                paper_bgcolor='#1E293B',
                font=dict(color='#F1F5F9'),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Calculate overall score
        df['Overall Score'] = df[metrics].mean(axis=1)
        filtered_df = df.sort_values('Overall Score', ascending=False)
        
        # Display as cards
        for _, site in filtered_df.head(5).iterrows():
            cols = st.columns([1, 3, 1, 1])
            
            with cols[0]:
                st.markdown(f"### 🏢")
            
            with cols[1]:
                st.markdown(f"**{site['Site']}**")
                st.markdown(f"<small>Budget: ${site['Budget ($M)']}M | Timeline: {site['Timeline (months)']} months</small>", unsafe_allow_html=True)
            
            with cols[2]:
                score_color = '#10B981' if site['Overall Score'] > 70 else '#F59E0B' if site['Overall Score'] > 50 else '#EF4444'
                st.markdown(f"<div style='text-align: center;'><span style='color: {score_color}; font-size: 1.5rem; font-weight: 600;'>{site['Overall Score']:.0f}</span><br><span style='color: #94A3B8;'>Score</span></div>", unsafe_allow_html=True)
            
            with cols[3]:
                st.markdown(f"<div style='text-align: center;'><span style='color: #06B6D4;'>{site['ROI Potential']:.0f}%</span><br><span style='color: #94A3B8;'>ROI</span></div>", unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 0.5rem 0; border-color: #334155;'>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📈 Performance Matrix")
        
        # Bubble chart
        x_axis = st.selectbox("X-Axis", metrics, index=0, key="multi_x")
        y_axis = st.selectbox("Y-Axis", metrics, index=1, key="multi_y")
        size_metric = st.selectbox("Bubble Size", metrics, index=2, key="multi_size")
        
        fig = px.scatter(
            df, 
            x=x_axis, 
            y=y_axis,
            size=size_metric,
            color='Overall Score',
            hover_name='Site',
            text='Site',
            title=f"{x_axis} vs {y_axis}",
            color_continuous_scale='Viridis'
        )
        
        fig.update_traces(textposition='top center')
        fig.update_layout(
            plot_bgcolor='#1E293B',
            paper_bgcolor='#1E293B',
            font=dict(color='#F1F5F9'),
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("### 🎯 Optimal Site Selection")
        
        st.markdown("#### ⚖️ Define Your Priorities")
        
        weights = {}
        cols = st.columns(len(metrics))
        
        for i, metric in enumerate(metrics):
            with cols[i]:
                weights[metric] = st.slider(
                    metric[:10],
                    min_value=0.0,
                    max_value=1.0,
                    value=0.5,
                    step=0.1,
                    key=f"weight_{i}"
                )
        
        # Normalize weights
        total = sum(weights.values())
        if total > 0:
            for metric in weights:
                weights[metric] /= total
        
        # Calculate weighted scores
        df['Weighted Score'] = 0
        for metric in metrics:
            df['Weighted Score'] += df[metric] * weights.get(metric, 0)
        
        # Sort and display
        top_sites = df.nlargest(5, 'Weighted Score')[['Site', 'Weighted Score'] + metrics]
        
        st.markdown("#### 🏆 Top 5 Sites Based on Your Priorities")
        st.dataframe(top_sites, use_container_width=True)
        
        # Recommendation
        best_site = top_sites.iloc[0]['Site']
        best_score = top_sites.iloc[0]['Weighted Score']
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #065986, #0F172A); 
                    padding: 2rem; border-radius: 16px; margin-top: 1rem;
                    border: 1px solid #06B6D4;">
            <h3 style="color: #F1F5F9;">🎯 OPTIMAL CHOICE</h3>
            <p style="color: #94A3B8; font-size: 1.2rem;">
                <span style="color: #06B6D4; font-weight: 600;">{best_site}</span>
                best matches your priorities with a score of 
                <span style="color: #06B6D4;">{best_score:.1f}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### 📋 Comparative Analysis")
        
        # Select sites to compare
        selected_sites = st.multiselect(
            "Select sites to compare",
            sites,
            default=sites[:3]
        )
        
        if selected_sites:
            comparison_df = df[df['Site'].isin(selected_sites)]
            
            # Radar chart
            fig = go.Figure()
            
            for _, site in comparison_df.iterrows():
                fig.add_trace(go.Scatterpolar(
                    r=[site[metric] for metric in metrics[:5]],
                    theta=metrics[:5],
                    fill='toself',
                    name=site['Site']
                ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=True,
                plot_bgcolor='#1E293B',
                paper_bgcolor='#1E293B',
                font=dict(color='#F1F5F9'),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed comparison table
            st.markdown("#### 📊 Side-by-Side Comparison")
            
            # Transpose for better display
            display_df = comparison_df.set_index('Site')[metrics + ['Budget ($M)', 'Timeline (months)']].T
            st.dataframe(display_df, use_container_width=True)