# -*- coding: utf-8 -*-
"""
Sidebar component for City Lens
"""

import streamlit as st
from datetime import date

def render_project_input():
    """
    Render the project input form in sidebar
    """
    with st.sidebar:
        st.header("🏗️ Project Details")
        
        # Project name
        project_name = st.text_input(
            "Project Name",
            value="New Development Project",
            help="Give your project a name"
        )
        
        # Project type with icons
        project_type = st.selectbox(
            "Project Type",
            options=[
                "🏢 Commercial",
                "🏘️ Residential", 
                "🏬 Mixed-Use",
                "🏭 Industrial",
                "🚉 Infrastructure"
            ],
            help="Select the type of development"
        )
        
        # Clean the project type (remove emoji)
        clean_project_type = project_type.split(" ")[1] if " " in project_type else project_type
        
        # Location input
        st.subheader("📍 Location")
        
        # Two options: address or coordinates
        location_method = st.radio(
            "Location input method",
            ["Enter address", "Click on map", "Enter coordinates"],
            horizontal=True
        )
        
        if location_method == "Enter address":
            address = st.text_input(
                "Address",
                value="Downtown, City",
                help="Enter the project address"
            )
            lat, lon = None, None
        elif location_method == "Enter coordinates":
            col1, col2 = st.columns(2)
            with col1:
                lat = st.number_input("Latitude", value=40.7128, format="%.6f")
            with col2:
                lon = st.number_input("Longitude", value=-74.0060, format="%.6f")
            address = f"{lat}, {lon}"
        else:
            st.info("Click on map in main area")
            lat, lon = None, None
            address = None
        
        # Project size
        st.subheader("📏 Project Size")
        col1, col2 = st.columns(2)
        with col1:
            size_value = st.number_input(
                "Size",
                min_value=100,
                value=50000,
                step=1000,
                help="Enter the project size"
            )
        with col2:
            size_unit = st.selectbox(
                "Unit",
                ["sq ft", "acres", "hectares"],
                help="Select unit of measurement"
            )
        
        # Timeline
        st.subheader("📅 Timeline")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=date.today()
            )
        with col2:
            duration = st.number_input(
                "Duration (months)",
                min_value=1,
                value=18,
                step=1
            )
        
        # Additional parameters
        with st.expander("⚙️ Advanced Parameters"):
            st.slider(
                "Population Density Factor",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Adjust for local density"
            )
            
            st.slider(
                "Environmental Sensitivity",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Adjust for environmental concerns"
            )
        
        # Analyze button
        analyze_clicked = st.button(
            "🔮 Analyze Impact",
            type="primary",
            use_container_width=True
        )
        
        # Store in session state
        if analyze_clicked:
            st.session_state['project_input'] = {
                'name': project_name,
                'type': clean_project_type,
                'address': address,
                'latitude': lat,
                'longitude': lon,
                'size': size_value,
                'size_unit': size_unit,
                'start_date': start_date,
                'duration': duration,
                'analyze': True
            }
        
        # Show recent analyses
        with st.expander("📋 Recent Analyses"):
            st.write("• Downtown Mall (2 hours ago)")
            st.write("• Riverside Apartments (yesterday)")
            st.write("• Tech Park (3 days ago)")
        
        # Help section
        with st.expander("❓ Help & Tips"):
            st.markdown("""
            **How to use:**
            1. Enter project details
            2. Click 'Analyze Impact'
            3. View results on map
            4. Get recommendations
            
            **Need help?** Contact support
            """)
        
        return analyze_clicked, st.session_state.get('project_input', {})