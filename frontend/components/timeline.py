# -*- coding: utf-8 -*-
"""
Timeline slider and forecast component for City Lens
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

def create_timeline_slider(years=5, start_year=2024):
    """
    Create an interactive timeline slider
    
    Returns:
        selected_year: The year selected by user
    """
    years = list(range(start_year, start_year + years + 1))
    
    st.markdown("""
    <div style="background: #1E293B; border-radius: 16px; padding: 1.5rem; 
                border: 1px solid #334155; margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
            <span style="color: #F1F5F9; font-weight: 600;">📅 Impact Timeline</span>
            <span style="color: #06B6D4;">Drag slider to see future impacts</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Create columns for slider and year display
    col1, col2 = st.columns([4, 1])
    
    with col1:
        selected_year = st.select_slider(
            "Select Year",
            options=years,
            value=years[1],  # Default to second year
            key="timeline_slider"
        )
    
    with col2:
        st.markdown(f"""
        <div style="background: #0F172A; padding: 0.5rem; border-radius: 8px; 
                    text-align: center; border: 1px solid #06B6D4;">
            <span style="color: #06B6D4; font-size: 1.5rem; font-weight: 700;">
                {selected_year}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return selected_year

def generate_forecast_data(base_value, year, start_year=2024, volatility=0.1):
    """
    Generate forecast data for a given year
    
    Args:
        base_value: Value at start year
        year: Target year
        start_year: Base year
        volatility: How much values fluctuate
    
    Returns:
        Projected value for the year
    """
    years_diff = year - start_year
    
    if years_diff == 0:
        return base_value
    
    # Different patterns for different metrics
    if 'traffic' in str(base_value).lower() or isinstance(base_value, (int, float)):
        # Traffic increases then decreases after construction
        if years_diff <= 2:  # Construction phase
            growth = 1 + (years_diff * 0.2)  # 20% increase per year
        else:  # Post-construction
            growth = 1.4 - ((years_diff - 2) * 0.1)  # Gradual decrease
    
    return base_value * growth

def display_forecast_chart(metric_name, historical_values, forecast_years):
    """
    Display a forecast chart with historical and projected values
    """
    # Create dataframe
    df = pd.DataFrame({
        'Year': list(historical_values.keys()) + forecast_years,
        'Value': list(historical_values.values()) + [None] * len(forecast_years),
        'Type': ['Historical'] * len(historical_values) + ['Forecast'] * len(forecast_years)
    })
    
    fig = go.Figure()
    
    # Historical line
    fig.add_trace(go.Scatter(
        x=list(historical_values.keys()),
        y=list(historical_values.values()),
        mode='lines+markers',
        name='Historical',
        line=dict(color='#06B6D4', width=3),
        marker=dict(size=8, color='#06B6D4')
    ))
    
    # Forecast line (dashed)
    if forecast_years:
        fig.add_trace(go.Scatter(
            x=forecast_years,
            y=[generate_forecast_data(list(historical_values.values())[-1], y) 
               for y in forecast_years],
            mode='lines+markers',
            name='Forecast',
            line=dict(color='#F59E0B', width=3, dash='dash'),
            marker=dict(size=8, color='#F59E0B')
        ))
    
    fig.update_layout(
        title=f"{metric_name} - Historical & Forecast",
        xaxis_title="Year",
        yaxis_title="Value",
        plot_bgcolor='#1E293B',
        paper_bgcolor='#1E293B',
        font=dict(color='#F1F5F9'),
        xaxis=dict(gridcolor='#334155'),
        yaxis=dict(gridcolor='#334155'),
        hovermode='x unified',
        height=400
    )
    
    return fig

def impact_timeline_dashboard(analysis_results):
    """
    Complete timeline dashboard with slider and charts
    """
    st.markdown("""
    <div class="chart-container">
        <h3 style="color: #F1F5F9; margin-bottom: 1rem;">📅 Impact Forecast (2024-2028)</h3>
    """, unsafe_allow_html=True)
    
    # Timeline slider
    selected_year = create_timeline_slider(years=5, start_year=2024)
    
    # Show impacts for selected year
    st.markdown(f"""
    <div style="background: #0F172A; border-radius: 12px; padding: 1rem; 
                margin: 1rem 0; border-left: 4px solid #06B6D4;">
        <div style="color: #06B6D4; font-weight: 600;">📊 PROJECTED IMPACTS FOR {selected_year}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate projected values based on selected year
    base_year = 2024
    years_diff = selected_year - base_year
    
    # Different phases
    if years_diff <= 2:  # Construction phase (2024-2026)
        phase = "🏗️ Construction Phase"
        phase_color = "#F59E0B"
        traffic_mult = 1 + (years_diff * 0.2)
        aqi_mult = 1 + (years_diff * 0.15)
        jobs = 250 + (years_diff * 100)
    else:  # Post-construction (2027-2028)
        phase = "✅ Post-Construction"
        phase_color = "#10B981"
        post_years = years_diff - 2
        traffic_mult = 1.4 - (post_years * 0.1)
        aqi_mult = 1.3 - (post_years * 0.1)
        jobs = 450 - (post_years * 50)
    
    # Display metrics for selected year
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: #1E293B; padding: 1rem; border-radius: 8px;">
            <div style="color: #94A3B8; font-size: 0.75rem;">TRAFFIC CONGESTION</div>
            <div style="color: #F1F5F9; font-size: 1.5rem; font-weight: 600;">
                {int(45 * traffic_mult)} min
            </div>
            <div style="color: {phase_color}; font-size: 0.75rem;">{phase}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #1E293B; padding: 1rem; border-radius: 8px;">
            <div style="color: #94A3B8; font-size: 0.75rem;">AIR QUALITY (AQI)</div>
            <div style="color: #F1F5F9; font-size: 1.5rem; font-weight: 600;">
                {int(85 * aqi_mult)}
            </div>
            <div style="color: {phase_color}; font-size: 0.75rem;">{phase}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="background: #1E293B; padding: 1rem; border-radius: 8px;">
            <div style="color: #94A3B8; font-size: 0.75rem;">JOBS</div>
            <div style="color: #F1F5F9; font-size: 1.5rem; font-weight: 600;">
                {jobs}
            </div>
            <div style="color: {phase_color}; font-size: 0.75rem;">{phase}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div style="background: #1E293B; padding: 1rem; border-radius: 8px;">
            <div style="color: #94A3B8; font-size: 0.75rem;">PROPERTY VALUE</div>
            <div style="color: #F1F5F9; font-size: 1.5rem; font-weight: 600;">
                {500 + (years_diff * 15)}k
            </div>
            <div style="color: {phase_color}; font-size: 0.75rem;">{phase}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Create forecast chart
    historical = {2022: 35, 2023: 40, 2024: 45}
    forecast = [2025, 2026, 2027, 2028]
    
    fig = display_forecast_chart("Traffic Congestion (minutes)", historical, forecast)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    return selected_year