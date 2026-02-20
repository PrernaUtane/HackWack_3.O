# -*- coding: utf-8 -*-
"""
Export utilities for City Lens
"""

import streamlit as st
import pandas as pd
import json
from datetime import datetime
import base64

def create_download_link(data, filename, text):
    """Create a download link for data"""
    if isinstance(data, pd.DataFrame):
        data = data.to_csv(index=False)
    elif isinstance(data, dict):
        data = json.dumps(data, indent=2)
    
    b64 = base64.b64encode(data.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{text}</a>'
    return href

def export_to_csv(dataframes, filename_prefix="citylens_export"):
    """
    Export multiple dataframes to CSV
    
    Args:
        dataframes: Dict of name: dataframe
        filename_prefix: Prefix for filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for name, df in dataframes.items():
        csv = df.to_csv(index=False)
        filename = f"{filename_prefix}_{name}_{timestamp}.csv"
        
        st.download_button(
            label=f"📥 Download {name} CSV",
            data=csv,
            file_name=filename,
            mime="text/csv",
            key=f"export_{name}"
        )

def export_to_json(data, filename=None):
    """
    Export data to JSON
    """
    if filename is None:
        filename = f"citylens_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    json_str = json.dumps(data, indent=2, default=str)
    
    st.download_button(
        label="📥 Download JSON",
        data=json_str,
        file_name=filename,
        mime="application/json"
    )

def create_report_html(analysis_results, user, metrics_df):
    """
    Create an HTML report
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>City Lens Impact Report</title>
        <style>
            body {{ font-family: 'Inter', sans-serif; background: #0B1120; color: #F1F5F9; }}
            .container {{ max-width: 1200px; margin: 0 auto; padding: 2rem; }}
            .header {{ text-align: center; margin-bottom: 2rem; }}
            .header h1 {{ color: #06B6D4; }}
            .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 2rem 0; }}
            .metric-card {{ background: #1E293B; padding: 1.5rem; border-radius: 12px; }}
            .metric-value {{ font-size: 2rem; font-weight: bold; color: #F1F5F9; }}
            .metric-label {{ color: #94A3B8; font-size: 0.875rem; }}
            table {{ width: 100%; border-collapse: collapse; margin: 2rem 0; }}
            th {{ background: #1E293B; color: #F1F5F9; padding: 1rem; text-align: left; }}
            td {{ padding: 0.75rem 1rem; border-bottom: 1px solid #334155; color: #94A3B8; }}
            .footer {{ text-align: center; margin-top: 3rem; color: #64748B; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🏙️ City Lens Impact Report</h1>
                <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
                <p>Report for: {user.get('name', 'User')} ({user.get('role', 'public').title()})</p>
            </div>
            
            <div class="metrics">
                <div class="metric-card">
                    <div class="metric-label">Traffic Impact</div>
                    <div class="metric-value">{analysis_results.get('traffic_impact', 0)}/100</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Air Quality</div>
                    <div class="metric-value">AQI: {analysis_results.get('air_quality', 0)}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Property Value</div>
                    <div class="metric-value">+{analysis_results.get('property_change', 0)}%</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Jobs Created</div>
                    <div class="metric-value">{analysis_results.get('jobs_created', 0)}</div>
                </div>
            </div>
            
            <h2>Detailed Metrics</h2>
            {metrics_df.to_html(index=False, classes='table')}
            
            <div class="footer">
                <p>© 2026 Epoch Elites | City Lens v2.0</p>
                <p>This report was automatically generated. For questions, contact support@citylens.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def display_export_options(analysis_results, user, metrics_df):
    """
    Display export options in the UI
    """
    st.markdown("### 📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CSV Export
        csv = metrics_df.to_csv(index=False)
        st.download_button(
            label="📥 CSV",
            data=csv,
            file_name=f"impact_metrics_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        # JSON Export
        json_data = {
            'analysis': analysis_results,
            'user': user,
            'generated_at': datetime.now().isoformat(),
            'version': '2.0'
        }
        json_str = json.dumps(json_data, indent=2, default=str)
        st.download_button(
            label="📥 JSON",
            data=json_str,
            file_name=f"impact_data_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col3:
        # HTML Report
        html = create_report_html(analysis_results, user, metrics_df)
        st.download_button(
            label="📥 HTML Report",
            data=html,
            file_name=f"impact_report_{datetime.now().strftime('%Y%m%d')}.html",
            mime="text/html",
            use_container_width=True
        )