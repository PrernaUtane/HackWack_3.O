# -*- coding: utf-8 -*-
"""
Baseline Analysis - Compare with/without development scenarios
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

def render_baseline_analysis():
    """
    Main function to render baseline vs development comparison
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                padding: 2rem; border-radius: 16px; border-left: 6px solid #10B981;
                margin-bottom: 2rem;">
        <h2 style="color: #F1F5F9; margin: 0;">📉 Baseline vs Development Analysis</h2>
        <p style="color: #94A3B8;">Compare current conditions with and without development</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📍 Site Selection")
        
        # Site selector
        site_option = st.selectbox(
            "Choose site",
            ["Downtown Location A", "Riverside Location B", "Suburban Location C", "Industrial Park D"],
            index=0
        )
        
        # Development scenario
        dev_type = st.selectbox(
            "Development Type",
            ["Commercial Tower", "Residential Complex", "Mixed-Use Development", "Industrial Park"]
        )
        
        dev_size = st.slider("Development Size (sq ft)", 10000, 500000, 100000, 10000)
    
    with col2:
        st.markdown("### ⚙️ Analysis Parameters")
        
        analysis_year = st.selectbox("Analysis Year", [2024, 2025, 2026, 2027, 2028])
        include_construction = st.checkbox("Include Construction Phase Impacts", value=True)
        show_sensitivity = st.checkbox("Show Sensitivity Analysis", value=False)
    
    # Generate baseline data
    np.random.seed(hash(site_option) % 100)
    
    # Baseline (without development)
    baseline = {
        'Traffic': np.random.normal(45, 5),
        'Air Quality': np.random.normal(85, 10),
        'Noise': np.random.normal(55, 5),
        'Property Value': np.random.normal(500, 50),
        'Jobs': np.random.normal(1000, 100),
        'Population': np.random.normal(5000, 500)
    }
    
    # With development (impacted)
    development = {
        'Traffic': baseline['Traffic'] * (1 + np.random.uniform(0.3, 0.7)),
        'Air Quality': baseline['Air Quality'] * (1 + np.random.uniform(0.2, 0.5)),
        'Noise': baseline['Noise'] * (1 + np.random.uniform(0.2, 0.4)),
        'Property Value': baseline['Property Value'] * (1 + np.random.uniform(-0.1, 0.3)),
        'Jobs': baseline['Jobs'] * (1 + np.random.uniform(0.1, 0.4)),
        'Population': baseline['Population'] * (1 + np.random.uniform(0.05, 0.2))
    }
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Comparison Dashboard",
        "📈 Impact Delta",
        "🔍 Detailed Breakdown",
        "📋 Report"
    ])
    
    with tab1:
        st.markdown("### 📊 With vs Without Development")
        
        # Metrics in columns
        metrics = list(baseline.keys())
        cols = st.columns(len(metrics))
        
        for i, metric in enumerate(metrics):
            baseline_val = baseline[metric]
            dev_val = development[metric]
            change = ((dev_val - baseline_val) / baseline_val) * 100
            
            # Determine color based on metric type
            if metric in ['Traffic', 'Air Quality', 'Noise']:
                is_positive = change < 0  # Lower is better for these
                color = '#10B981' if is_positive else '#EF4444'
                arrow = '▼' if is_positive else '▲'
            else:
                is_positive = change > 0  # Higher is better for these
                color = '#10B981' if is_positive else '#EF4444'
                arrow = '▲' if is_positive else '▼'
            
            with cols[i]:
                st.markdown(f"""
                <div style="background: #1E293B; padding: 1rem; border-radius: 8px;">
                    <div style="color: #94A3B8; font-size: 0.75rem;">{metric.upper()}</div>
                    <div style="display: flex; justify-content: space-between; align-items: baseline;">
                        <div>
                            <span style="color: #94A3B8; font-size: 0.875rem;">Base:</span>
                            <span style="color: #F1F5F9;"> {baseline_val:.0f}</span>
                        </div>
                        <div>
                            <span style="color: #94A3B8; font-size: 0.875rem;">Dev:</span>
                            <span style="color: #F1F5F9;"> {dev_val:.0f}</span>
                        </div>
                    </div>
                    <div style="margin-top: 0.5rem; color: {color};">
                        {arrow} {abs(change):.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Comparison chart
        fig = go.Figure()
        
        categories = list(baseline.keys())
        
        fig.add_trace(go.Bar(
            name='Without Development (Baseline)',
            x=categories,
            y=[baseline[cat] for cat in categories],
            marker_color='#94A3B8',
            text=[f"{baseline[cat]:.0f}" for cat in categories],
            textposition='outside'
        ))
        
        fig.add_trace(go.Bar(
            name='With Development',
            x=categories,
            y=[development[cat] for cat in categories],
            marker_color='#06B6D4',
            text=[f"{development[cat]:.0f}" for cat in categories],
            textposition='outside'
        ))
        
        fig.update_layout(
            title=f"Baseline vs Development - {site_option}",
            barmode='group',
            plot_bgcolor='#1E293B',
            paper_bgcolor='#1E293B',
            font=dict(color='#F1F5F9'),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 📈 Net Impact Analysis")
        
        # Calculate deltas
        deltas = {}
        for key in baseline:
            deltas[key] = ((development[key] - baseline[key]) / baseline[key]) * 100
        
        # Create impact gauge for each metric
        cols = st.columns(3)
        metric_items = list(deltas.items())
        
        for i in range(0, len(metric_items), 3):
            row_metrics = metric_items[i:i+3]
            row_cols = st.columns(3)
            
            for j, (metric, delta) in enumerate(row_metrics):
                with row_cols[j]:
                    # Determine color
                    if metric in ['Traffic', 'Air Quality', 'Noise']:
                        color = '#10B981' if delta < 0 else '#EF4444'
                        impact = "Beneficial" if delta < 0 else "Harmful"
                    else:
                        color = '#10B981' if delta > 0 else '#EF4444'
                        impact = "Beneficial" if delta > 0 else "Harmful"
                    
                    # Create gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=abs(delta),
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': metric, 'font': {'color': '#F1F5F9'}},
                        gauge={
                            'axis': {'range': [None, 100], 'tickcolor': '#F1F5F9'},
                            'bar': {'color': color},
                            'steps': [
                                {'range': [0, 33], 'color': '#10B981'},
                                {'range': [33, 66], 'color': '#F59E0B'},
                                {'range': [66, 100], 'color': '#EF4444'}
                            ],
                            'threshold': {
                                'line': {'color': 'white', 'width': 4},
                                'thickness': 0.75,
                                'value': abs(delta)
                            }
                        }
                    ))
                    
                    fig.update_layout(
                        height=200,
                        margin=dict(l=10, r=10, t=50, b=10),
                        paper_bgcolor='#1E293B',
                        font={'color': '#F1F5F9'}
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(f"""
                    <div style="text-align: center; color: {color}; font-weight: 600; margin-top: -1rem;">
                        {delta:+.1f}% ({impact})
                    </div>
                    """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🔍 Detailed Factor Analysis")
        
        # Create detailed breakdown table
        detailed_data = []
        for metric in baseline.keys():
            detailed_data.append({
                'Metric': metric,
                'Baseline': f"{baseline[metric]:.1f}",
                'With Development': f"{development[metric]:.1f}",
                'Absolute Change': f"{development[metric] - baseline[metric]:+.1f}",
                'Percent Change': f"{((development[metric] - baseline[metric])/baseline[metric]*100):+.1f}%",
                'Impact Direction': '📈 Increase' if development[metric] > baseline[metric] else '📉 Decrease'
            })
        
        df = pd.DataFrame(detailed_data)
        st.dataframe(df, use_container_width=True)
        
        # Sensitivity analysis
        if show_sensitivity:
            st.markdown("### 📊 Sensitivity Analysis")
            
            # Create sensitivity ranges
            sensitivity_factors = np.linspace(0.5, 1.5, 10)
            
            fig = go.Figure()
            
            for metric in ['Traffic', 'Air Quality', 'Property Value']:
                values = [baseline[metric] * factor for factor in sensitivity_factors]
                fig.add_trace(go.Scatter(
                    x=sensitivity_factors,
                    y=values,
                    mode='lines+markers',
                    name=metric
                ))
            
            fig.update_layout(
                title="Sensitivity to Development Scale",
                xaxis_title="Scale Factor",
                yaxis_title="Impact Value",
                plot_bgcolor='#1E293B',
                paper_bgcolor='#1E293B',
                font=dict(color='#F1F5F9')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 📋 Executive Summary")
        
        # Calculate overall impact score
        impact_scores = []
        for metric in baseline.keys():
            change = ((development[metric] - baseline[metric]) / baseline[metric]) * 100
            if metric in ['Traffic', 'Air Quality', 'Noise']:
                impact_scores.append(-change)  # Negative change is good
            else:
                impact_scores.append(change)   # Positive change is good
        
        overall_score = np.mean(impact_scores)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                    padding: 2rem; border-radius: 16px; border: 1px solid #334155;">
            <h3 style="color: #F1F5F9;">Project: {dev_type} at {site_option}</h3>
            <p style="color: #94A3B8;">Analysis Year: {analysis_year} | Size: {dev_size:,} sq ft</p>
            
            <div style="display: flex; gap: 2rem; margin: 2rem 0;">
                <div style="text-align: center;">
                    <div style="color: #94A3B8;">Overall Impact Score</div>
                    <div style="font-size: 3rem; color: {'#10B981' if overall_score > 0 else '#EF4444'};">
                        {overall_score:+.1f}
                    </div>
                    <div style="color: #94A3B8;">/100</div>
                </div>
                
                <div style="flex: 1;">
                    <div style="color: #F1F5F9; margin-bottom: 1rem;">Key Findings:</div>
                    <ul style="color: #94A3B8;">
                        <li>Traffic expected to increase by {((development['Traffic'] - baseline['Traffic'])/baseline['Traffic']*100):+.1f}%</li>
                        <li>Property values {'increase' if development['Property Value'] > baseline['Property Value'] else 'decrease'} by {abs(((development['Property Value'] - baseline['Property Value'])/baseline['Property Value']*100)):.1f}%</li>
                        <li>{development['Jobs'] - baseline['Jobs']:.0f} new jobs created</li>
                    </ul>
                </div>
            </div>
            
            <div style="background: #0F172A; padding: 1rem; border-radius: 8px;">
                <span style="color: #06B6D4;">🎯 Recommendation:</span>
                <span style="color: #94A3B8;"> 
                    {'Proceed with mitigation measures' if overall_score < -20 else 'Proceed with caution' if overall_score < 0 else 'Recommended for approval'}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Export buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Download Full Report", use_container_width=True):
                st.success("Report downloaded!")
        with col2:
            if st.button("📧 Email Analysis", use_container_width=True):
                st.info("Email sent!")