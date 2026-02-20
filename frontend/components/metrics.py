# -*- coding: utf-8 -*-
"""
Enhanced metric cards for City Lens
Professional dark theme metrics with badges and trends
"""

import streamlit as st

def metric_card(icon, label, value, change, badge_text, badge_type="warning"):
    """
    Display a professional metric card
    
    Args:
        icon: Emoji or icon string
        label: Metric label
        value: Main value to display
        change: Change indicator (e.g., "+35%")
        badge_text: Text for badge (e.g., "HIGH", "MODERATE")
        badge_type: "critical", "warning", "success", or "neutral"
    """
    
    badge_colors = {
        "critical": "metric-badge-critical",
        "warning": "metric-badge-warning", 
        "success": "metric-badge-success",
        "neutral": "metric-badge-neutral"
    }
    
    badge_class = badge_colors.get(badge_type, "metric-badge-neutral")
    
    # Determine change color and arrow
    if str(change).startswith("+"):
        change_color = "#10B981"  # green
        arrow = "▲"
    elif str(change).startswith("-"):
        change_color = "#EF4444"  # red
        arrow = "▼"
    else:
        change_color = "#94A3B8"  # gray
        arrow = "•"
    
    html = f"""
    <div class="metric-container">
        <div class="metric-header">
            <span class="metric-label">{icon} {label}</span>
            <span class="metric-badge {badge_class}">{badge_text}</span>
        </div>
        <div class="metric-value">{value}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
            <span class="metric-subvalue">
                <span style="color: {change_color};">{arrow} {change}</span>
            </span>
            <span class="metric-subvalue">vs baseline</span>
        </div>
    </div>
    """
    
    return html

def display_metrics_row(metrics_data):
    """
    Display a row of metric cards
    
    metrics_data: List of dicts with keys: 
        icon, label, value, change, badge_text, badge_type
    """
    cols = st.columns(len(metrics_data))
    
    for i, metric in enumerate(metrics_data):
        with cols[i]:
            st.markdown(
                metric_card(
                    icon=metric['icon'],
                    label=metric['label'],
                    value=metric['value'],
                    change=metric['change'],
                    badge_text=metric['badge_text'],
                    badge_type=metric['badge_type']
                ),
                unsafe_allow_html=True
            )

def create_metric_from_analysis(metric_type, value, change=None):
    """
    Create a metric card configuration from analysis data
    
    Args:
        metric_type: 'traffic', 'air', 'property', 'jobs', 'population'
        value: The metric value
        change: Optional change percentage
    """
    
    metrics_config = {
        'traffic': {
            'icon': '🚦',
            'label': 'TRAFFIC IMPACT',
            'badge_map': lambda v: ('CRITICAL', 'critical') if v > 80 else 
                                   ('HIGH', 'warning') if v > 60 else
                                   ('MODERATE', 'neutral') if v > 40 else
                                   ('LOW', 'success')
        },
        'air': {
            'icon': '🌫️',
            'label': 'AIR QUALITY',
            'badge_map': lambda v: ('HAZARDOUS', 'critical') if v > 200 else
                                   ('UNHEALTHY', 'warning') if v > 150 else
                                   ('MODERATE', 'neutral') if v > 100 else
                                   ('GOOD', 'success')
        },
        'property': {
            'icon': '💰',
            'label': 'PROPERTY VALUE',
            'badge_map': lambda v: ('BOOM', 'success') if v > 20 else
                                   ('GROWTH', 'neutral') if v > 10 else
                                   ('STABLE', 'neutral') if v > 0 else
                                   ('DECLINE', 'warning')
        },
        'jobs': {
            'icon': '👷',
            'label': 'JOBS CREATED',
            'badge_map': lambda v: ('MAJOR', 'success') if v > 500 else
                                   ('SIGNIFICANT', 'neutral') if v > 200 else
                                   ('MODERATE', 'neutral') if v > 50 else
                                   ('MINOR', 'warning')
        },
        'population': {
            'icon': '👥',
            'label': 'POPULATION AFFECTED',
            'badge_map': lambda v: ('MAJOR', 'critical') if v > 50000 else
                                   ('HIGH', 'warning') if v > 10000 else
                                   ('MODERATE', 'neutral') if v > 1000 else
                                   ('LOW', 'success')
        }
    }
    
    config = metrics_config.get(metric_type, {
        'icon': '📊',
        'label': 'METRIC',
        'badge_map': lambda v: ('INFO', 'neutral')
    })
    
    badge_text, badge_type = config['badge_map'](value)
    
    # Format value based on metric type
    if metric_type == 'traffic':
        display_value = f"{value}/100"
    elif metric_type == 'air':
        display_value = f"AQI: {value}"
    elif metric_type == 'property':
        display_value = f"{value}%"
    elif metric_type == 'jobs':
        display_value = f"{value:,}"
    elif metric_type == 'population':
        display_value = f"{value:,}"
    else:
        display_value = str(value)
    
    return {
        'icon': config['icon'],
        'label': config['label'],
        'value': display_value,
        'change': change if change else "0%",
        'badge_text': badge_text,
        'badge_type': badge_type
    }

def kpi_card(title, value, subtitle=None, trend=None, trend_direction="up"):
    """
    Simple KPI card for dashboard
    
    Args:
        title: KPI title
        value: Main value
        subtitle: Optional subtitle
        trend: Optional trend percentage
        trend_direction: "up" or "down"
    """
    
    trend_color = "#10B981" if trend_direction == "up" else "#EF4444"
    trend_arrow = "▲" if trend_direction == "up" else "▼"
    
    html = f"""
    <div style="background: #1E293B; padding: 1rem; border-radius: 8px; 
                border: 1px solid #334155; margin-bottom: 0.5rem;">
        <div style="color: #94A3B8; font-size: 0.75rem; text-transform: uppercase; 
                    letter-spacing: 0.05em; margin-bottom: 0.25rem;">
            {title}
        </div>
        <div style="display: flex; align-items: baseline; justify-content: space-between;">
            <span style="color: #F1F5F9; font-size: 1.5rem; font-weight: 600;">
                {value}
            </span>
            {f'<span style="color: {trend_color}; font-size: 0.875rem;">{trend_arrow} {trend}</span>' if trend else ''}
        </div>
        {f'<div style="color: #64748B; font-size: 0.75rem; margin-top: 0.25rem;">{subtitle}</div>' if subtitle else ''}
    </div>
    """
    
    return html

def impact_gauge(score, title="Impact Score", height=200):
    """
    Create a custom gauge chart using HTML/CSS
    
    Args:
        score: Value between 0-100
        title: Gauge title
        height: Chart height in pixels
    """
    
    # Determine color based on score
    if score > 80:
        color = "#EF4444"  # red
        level = "Critical"
    elif score > 60:
        color = "#F59E0B"  # orange
        level = "High"
    elif score > 40:
        color = "#FBBF24"  # yellow
        level = "Moderate"
    else:
        color = "#10B981"  # green
        level = "Low"
    
    # Calculate rotation for gauge needle (0-180 degrees)
    rotation = (score / 100) * 180
    
    html = f"""
    <div style="background: #1E293B; border-radius: 16px; padding: 1.5rem; 
                border: 1px solid #334155; margin-bottom: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <span style="color: #F1F5F9; font-weight: 600;">{title}</span>
            <span style="color: {color}; font-weight: 600;">{level}</span>
        </div>
        
        <!-- Simple gauge visualization -->
        <div style="position: relative; height: 100px; margin: 1rem 0;">
            <div style="position: absolute; bottom: 0; left: 0; right: 0; 
                        height: 20px; background: linear-gradient(90deg, 
                        #10B981 0%, #FBBF24 40%, #F59E0B 60%, #EF4444 100%); 
                        border-radius: 10px;"></div>
            
            <!-- Needle -->
            <div style="position: absolute; bottom: 20px; left: {score}%; 
                        transform: translateX(-50%);">
                <div style="width: 4px; height: 40px; background: {color}; 
                            border-radius: 2px;"></div>
                <div style="width: 12px; height: 12px; background: {color}; 
                            border-radius: 50%; margin-top: -4px; margin-left: -4px;"></div>
            </div>
        </div>
        
        <div style="display: flex; justify-content: space-between; color: #94A3B8; 
                    font-size: 0.75rem; margin-top: 0.5rem;">
            <span>0</span>
            <span>25</span>
            <span>50</span>
            <span>75</span>
            <span>100</span>
        </div>
        
        <div style="text-align: center; margin-top: 1rem;">
            <span style="color: #F1F5F9; font-size: 2rem; font-weight: 700;">
                {score}
            </span>
            <span style="color: #94A3B8;">/100</span>
        </div>
    </div>
    """
    
    return html