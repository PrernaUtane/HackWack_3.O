# -*- coding: utf-8 -*-
"""
Charts and visualization components for City Lens
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_congestion_gauge(score):
    """
    Create a gauge chart for congestion score
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Congestion Score"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgreen"},
                {'range': [40, 60], 'color': "yellow"},
                {'range': [60, 80], 'color': "orange"},
                {'range': [80, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 80
            }
        }
    ))
    
    fig.update_layout(height=250)
    return fig

def create_impact_comparison(before_data, after_data):
    """
    Create before/after comparison chart
    """
    categories = ['Traffic', 'Air Quality', 'Noise', 'Property Value', 'Jobs']
    
    fig = go.Figure()
    
    # Before data
    fig.add_trace(go.Scatterpolar(
        r=before_data,
        theta=categories,
        fill='toself',
        name='Before Project',
        line_color='blue'
    ))
    
    # After data
    fig.add_trace(go.Scatterpolar(
        r=after_data,
        theta=categories,
        fill='toself',
        name='After Project',
        line_color='red'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        height=400
    )
    
    return fig

def create_timeline_forecast(dates, values, title):
    """
    Create a timeline forecast chart
    """
    df = pd.DataFrame({
        'Date': dates,
        'Impact': values
    })
    
    fig = px.line(
        df, 
        x='Date', 
        y='Impact',
        title=title,
        markers=True
    )
    
    # Add confidence interval
    fig.add_band(
        name="Confidence",
        x0=dates[0],
        x1=dates[-1],
        y0=min(values) * 0.9,
        y1=max(values) * 1.1,
        fillcolor="rgba(0,100,80,0.2)",
        line={"width": 0},
    )
    
    fig.update_layout(height=300)
    return fig

def create_impact_breakdown(impact_scores):
    """
    Create a bar chart showing impact breakdown
    """
    categories = list(impact_scores.keys())
    scores = list(impact_scores.values())
    colors = ['red' if s > 80 else 'orange' if s > 60 else 'yellow' if s > 40 else 'green' for s in scores]
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=scores,
            marker_color=colors,
            text=[f"{s:.0f}" for s in scores],
            textposition='outside'
        )
    ])
    
    fig.update_layout(
        title="Impact Breakdown by Category",
        yaxis_title="Impact Score",
        yaxis_range=[0, 100],
        height=400,
        showlegend=False
    )
    
    return fig

def create_comparison_heatmap(matrix_data, row_labels, col_labels):
    """
    Create a correlation heatmap
    """
    fig = go.Figure(data=go.Heatmap(
        z=matrix_data,
        x=col_labels,
        y=row_labels,
        colorscale='RdBu_r',
        zmid=0,
        text=matrix_data,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        hoverongaps=False
    ))
    
    fig.update_layout(
        title="Impact Correlations",
        height=400,
        xaxis_title="Factors",
        yaxis_title="Impacts"
    )
    
    return fig