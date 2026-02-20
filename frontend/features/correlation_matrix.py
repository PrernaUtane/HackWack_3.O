# -*- coding: utf-8 -*-
"""
Correlation Matrix - Show relationships between different impacts
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def render_correlation_matrix():
    """
    Main function to render correlation analysis
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                padding: 2rem; border-radius: 16px; border-left: 6px solid #F59E0B;
                margin-bottom: 2rem;">
        <h2 style="color: #F1F5F9; margin: 0;">📈 Impact Correlation Matrix</h2>
        <p style="color: #94A3B8;">Understand relationships between different impact factors</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate sample correlation data
    np.random.seed(42)
    n_samples = 100
    
    # Create synthetic data showing relationships
    traffic = np.random.normal(50, 15, n_samples)
    air_quality = traffic * 0.7 + np.random.normal(20, 10, n_samples)  # Strong correlation
    noise = traffic * 0.6 + np.random.normal(25, 12, n_samples)        # Strong correlation
    property_value = -traffic * 0.4 + np.random.normal(70, 15, n_samples)  # Negative correlation
    jobs = traffic * 0.3 + np.random.normal(40, 20, n_samples)         # Weak correlation
    population = traffic * 0.5 + np.random.normal(30, 15, n_samples)    # Medium correlation
    
    df = pd.DataFrame({
        'Traffic': traffic,
        'Air Quality': air_quality,
        'Noise': noise,
        'Property Value': property_value,
        'Jobs': jobs,
        'Population': population
    })
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["🔷 Correlation Heatmap", "📊 Scatter Matrix", "📈 Insights"])
    
    with tab1:
        st.markdown("### 🔷 Impact Correlation Heatmap")
        st.markdown("*Shows how strongly different factors influence each other*")
        
        # Calculate correlation matrix
        corr_matrix = df.corr()
        
        # Create heatmap using plotly
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu_r',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10, "color": "white"},
            hoverongaps=False
        ))
        
        fig.update_layout(
            title="Correlation Matrix (1 = perfect positive, -1 = perfect negative)",
            plot_bgcolor='#1E293B',
            paper_bgcolor='#1E293B',
            font=dict(color='#F1F5F9'),
            height=600,
            width=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Interpretation
        st.markdown("### 📌 Key Correlations")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background: #1E293B; padding: 1rem; border-radius: 8px; 
                        border-left: 4px solid #EF4444;">
                <h4 style="color: #F1F5F9;">🔴 Strong Positive (0.7 - 1.0)</h4>
                <p style="color: #94A3B8;">• Traffic ↔ Air Quality: 0.85<br>
                • Traffic ↔ Noise: 0.78<br>
                • Air Quality ↔ Noise: 0.82</p>
                <small>When traffic increases, air pollution and noise increase proportionally</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #1E293B; padding: 1rem; border-radius: 8px; 
                        border-left: 4px solid #10B981;">
                <h4 style="color: #F1F5F9;">🟢 Strong Negative (-0.7 - -1.0)</h4>
                <p style="color: #94A3B8;">• Traffic ↔ Property Value: -0.72<br>
                • Noise ↔ Property Value: -0.68</p>
                <small>Higher traffic and noise decrease property values</small>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 📊 Scatter Plot Matrix")
        st.markdown("*Explore relationships between any two factors*")
        
        # Select variables to compare
        col1, col2 = st.columns(2)
        with col1:
            x_var = st.selectbox("X-axis variable", df.columns, index=0)
        with col2:
            y_var = st.selectbox("Y-axis variable", df.columns, index=1)
        
        # Create scatter plot
        fig = px.scatter(
            df, x=x_var, y=y_var,
            trendline="ols",
            title=f"{x_var} vs {y_var}",
            labels={x_var: x_var, y_var: y_var}
        )
        
        fig.update_layout(
            plot_bgcolor='#1E293B',
            paper_bgcolor='#1E293B',
            font=dict(color='#F1F5F9'),
            height=500
        )
        
        fig.update_xaxes(gridcolor='#334155')
        fig.update_yaxes(gridcolor='#334155')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calculate correlation
        correlation = df[x_var].corr(df[y_var])
        
        st.markdown(f"""
        <div style="background: #0F172A; padding: 1rem; border-radius: 8px; 
                    text-align: center; border: 1px solid #334155;">
            <span style="color: #94A3B8;">Correlation Coefficient: </span>
            <span style="color: {'#EF4444' if abs(correlation) > 0.7 else '#F59E0B' if abs(correlation) > 0.4 else '#10B981'}; 
                        font-size: 1.5rem; font-weight: 600;">
                {correlation:.3f}
            </span>
            <span style="color: #94A3B8; margin-left: 1rem;">
                ({'Strong' if abs(correlation) > 0.7 else 'Moderate' if abs(correlation) > 0.4 else 'Weak'} 
                {'positive' if correlation > 0 else 'negative'} correlation)
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 💡 Insights & Recommendations")
        
        insights = [
            {
                'title': 'Traffic-Air Quality Nexus',
                'description': 'Strong correlation (0.85) suggests any traffic mitigation will significantly improve air quality.',
                'action': 'Prioritize traffic flow improvements to address air quality concerns',
                'impact': 'High',
                'icon': '🌫️'
            },
            {
                'title': 'Property Value Protection',
                'description': 'Negative correlation (-0.72) indicates need for buffer zones near high-traffic areas.',
                'action': 'Implement green buffers and sound barriers to protect property values',
                'impact': 'High',
                'icon': '💰'
            },
            {
                'title': 'Jobs-Housing Balance',
                'description': 'Moderate correlation (0.45) suggests job growth drives population increase.',
                'action': 'Plan additional housing near job centers to prevent commute strain',
                'impact': 'Medium',
                'icon': '👷'
            }
        ]
        
        for insight in insights:
            impact_color = '#EF4444' if insight['impact'] == 'High' else '#F59E0B'
            
            st.markdown(f"""
            <div style="background: #1E293B; padding: 1.5rem; border-radius: 12px; 
                        margin-bottom: 1rem; border-left: 4px solid {impact_color};">
                <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 0.5rem;">
                    <span style="font-size: 2rem;">{insight['icon']}</span>
                    <h4 style="color: #F1F5F9; margin: 0;">{insight['title']}</h4>
                    <span style="background: {impact_color}; padding: 0.25rem 0.75rem; 
                                border-radius: 999px; font-size: 0.75rem; color: white;">
                        {insight['impact']} Impact
                    </span>
                </div>
                <p style="color: #94A3B8; margin-bottom: 0.5rem;">{insight['description']}</p>
                <p style="color: #06B6D4; font-weight: 500;">🎯 Action: {insight['action']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Export option
    if st.button("📥 Export Correlation Analysis", use_container_width=True):
        st.success("Analysis exported! (Demo)")