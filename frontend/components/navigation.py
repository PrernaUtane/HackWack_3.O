# -*- coding: utf-8 -*-
"""
Professional Navigation Component for City Lens
Clean sidebar with Add Project feature and backend status
"""

import streamlit as st
from datetime import datetime
from utils.api_clients import get_api_client

def render_navigation():
    """
    Render the professional sidebar navigation
    """
    with st.sidebar:
        # Logo and brand
        st.markdown("""
        <div style="padding: 1.5rem 1rem 1rem 1rem; border-bottom: 1px solid #2A2A3A; margin-bottom: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.8rem;">🏙️</span>
                <span style="font-size: 1.2rem; font-weight: 600; color: #F1F5F9;">City Lens</span>
            </div>
            <div style="font-size: 0.7rem; color: #6B6B7F; margin-top: 0.25rem;">Urban Impact Platform</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Backend status indicator
        try:
            api = get_api_client()
            health = api.health_check()
            
            if health:
                st.markdown("""
                <div style="padding: 0 1rem 1rem 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; background: #1E1E2D; padding: 0.5rem; border-radius: 8px;">
                        <div style="width: 8px; height: 8px; background: #10B981; border-radius: 50%;"></div>
                        <span style="color: #6B6B7F; font-size: 0.7rem;">Backend Connected</span>
                        <span style="color: #6B6B7F; font-size: 0.6rem; margin-left: auto;">v1.0</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="padding: 0 1rem 1rem 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; background: #1E1E2D; padding: 0.5rem; border-radius: 8px;">
                        <div style="width: 8px; height: 8px; background: #EF4444; border-radius: 50%;"></div>
                        <span style="color: #6B6B7F; font-size: 0.7rem;">Backend Offline</span>
                        <span style="color: #6B6B7F; font-size: 0.6rem; margin-left: auto;">Using Mock</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.markdown("""
            <div style="padding: 0 1rem 1rem 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; background: #1E1E2D; padding: 0.5rem; border-radius: 8px;">
                    <div style="width: 8px; height: 8px; background: #F59E0B; border-radius: 50%;"></div>
                    <span style="color: #6B6B7F; font-size: 0.7rem;">Checking Backend...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # ===== ADD NEW PROJECT SECTION =====
        st.markdown("""
        <div style="padding: 1rem 1rem 0.5rem 1rem;">
            <div style="font-size: 0.7rem; color: #6B6B7F; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;">
                ADD NEW PROJECT
            </div>
        """, unsafe_allow_html=True)
        
        # Project Type Selection
        project_type = st.selectbox(
            "Project Type",
            ["Commercial", "Residential", "Mixed-Use", "Industrial", "Infrastructure"],
            key="sidebar_project_type",
            label_visibility="collapsed",
            placeholder="Select project type"
        )
        
        # Project Name
        project_name = st.text_input(
            "Project Name",
            placeholder="e.g., Downtown Tower",
            key="sidebar_project_name",
            label_visibility="collapsed"
        )
        
        # Site Location
        site_location = st.text_input(
            "Site Location",
            placeholder="Address or coordinates",
            key="sidebar_site_location",
            label_visibility="collapsed"
        )
        
        # Add Project Button
        if st.button("+ Add Development Project", key="add_project_btn", use_container_width=True):
            if project_name and site_location:
                # Initialize projects list if not exists
                if 'user_projects' not in st.session_state:
                    st.session_state.user_projects = []
                
                # Add new project
                new_project = {
                    'name': project_name,
                    'type': project_type,
                    'location': site_location,
                    'date_added': datetime.now().strftime("%Y-%m-%d"),
                    'status': 'Draft'
                }
                st.session_state.user_projects.append(new_project)
                st.success(f"✅ Added {project_name}")
                st.rerun()
            else:
                st.warning("Please enter project name and location")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # ===== MY PROJECTS SECTION =====
        if 'user_projects' in st.session_state and st.session_state.user_projects:
            st.markdown("""
            <div style="padding: 1rem 1rem 0.5rem 1rem;">
                <div style="font-size: 0.7rem; color: #6B6B7F; text-transform: uppercase; letter-spacing: 0.5px;">
                    MY PROJECTS
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            for i, project in enumerate(st.session_state.user_projects):
                # Project card
                st.markdown(f"""
                <div style="background: #1E1E2D; margin: 0.5rem 1rem; padding: 0.75rem; border-radius: 8px; 
                            border: 1px solid #2A2A3A; transition: all 0.2s;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #F1F5F9; font-weight: 500; font-size: 0.9rem;">{project['name']}</div>
                            <div style="color: #6B6B7F; font-size: 0.7rem;">{project['type']} • {project['location'][:20]}...</div>
                        </div>
                        <div style="background: #2A2A3A; padding: 0.2rem 0.5rem; border-radius: 4px; 
                                    color: #6366F1; font-size: 0.6rem;">{project['status']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Analyze button for each project
                if st.button(f"🔍 Analyze", key=f"analyze_project_{i}"):
                    st.session_state.show_quick = True
                    st.session_state['analysis_results'] = {
                        'latitude': 40.7128,
                        'longitude': -74.0060,
                        'project_name': project['name'],
                        'project_type': project['type']
                    }
                    st.rerun()
        
        # ===== NAVIGATION MENU =====
        st.markdown("""
        <div style="padding: 1rem 1rem 0.5rem 1rem; margin-top: 1rem;">
            <div style="font-size: 0.7rem; color: #6B6B7F; text-transform: uppercase; letter-spacing: 0.5px;">
                MENU
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation items as buttons
        nav_items = [
            ("🏠", "Dashboard", "nav_dashboard"),
            ("⚡", "Quick Analysis", "nav_quick"),
            ("🔄", "Site Comparison", "nav_site"),
            ("📊", "Correlation Matrix", "nav_corr"),
            ("📉", "Baseline Analysis", "nav_base"),
            ("📈", "Multi-Site Analytics", "nav_multi"),
        ]
        
        for icon, label, key in nav_items:
            cols = st.columns([1, 8])
            with cols[0]:
                st.markdown(f"<div style='text-align: right; color: #6B6B7F;'>{icon}</div>", unsafe_allow_html=True)
            with cols[1]:
                if st.button(label, key=key, use_container_width=True):
                    if key == "nav_dashboard":
                        for k in ['show_quick', 'show_site_comparison', 'show_correlation', 
                                 'show_baseline', 'show_multi']:
                            st.session_state[k] = False
                    elif key == "nav_quick":
                        st.session_state.show_quick = True
                    elif key == "nav_site":
                        st.session_state.show_site_comparison = True
                    elif key == "nav_corr":
                        st.session_state.show_correlation = True
                    elif key == "nav_base":
                        st.session_state.show_baseline = True
                    elif key == "nav_multi":
                        st.session_state.show_multi = True
                    st.rerun()
        
        # ===== USER PROFILE AT BOTTOM =====
        if 'user' in st.session_state:
            user = st.session_state['user']
            
            st.markdown("""
            <div style="position: fixed; bottom: 1rem; left: 1rem; right: 1rem; width: calc(100% - 2rem);">
            """, unsafe_allow_html=True)
            
            # Profile card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1E293B, #0F172A); 
                        padding: 1rem; border-radius: 12px; border: 1px solid #2A2A3A;
                        margin-top: 2rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="width: 40px; height: 40px; background: #6366F1; 
                                border-radius: 50%; display: flex; align-items: center; 
                                justify-content: center; color: white; font-weight: 600;">
                        {user.get('name', 'U')[0].upper()}
                    </div>
                    <div>
                        <div style="color: #F1F5F9; font-weight: 500; font-size: 0.9rem;">
                            {user.get('name', 'User')}
                        </div>
                        <div style="color: #6B6B7F; font-size: 0.7rem;">
                            {user.get('role', 'public').title()} • {user.get('organization', 'N/A')[:10]}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Logout button
            from components.auth import logout
            if st.button("🚪 Sign Out", key="logout_sidebar", use_container_width=True):
                logout()
            
            st.markdown("</div>", unsafe_allow_html=True)

def render_header():
    """
    Render the professional header section
    """
    if 'user' in st.session_state:
        user = st.session_state['user']
        
        st.markdown(f"""
        <div style="margin-bottom: 2rem;">
            <h1 style="color: #F1F5F9; font-size: 2rem; font-weight: 600; margin-bottom: 0.25rem;">
                Welcome back, {user.get('name', 'User')}
            </h1>
            <p style="color: #6B6B7F; font-size: 0.9rem;">
                {user.get('role', 'public').title()} • {user.get('organization', 'City Lens')}
            </p>
        </div>
        """, unsafe_allow_html=True)

def render_footer():
    """
    Render the professional footer
    """
    st.markdown("""
    <div style="margin-top: 3rem; padding: 1.5rem 0; border-top: 1px solid #2A2A3A;">
        <div style="display: flex; justify-content: space-between; align-items: center; color: #6B6B7F; font-size: 0.75rem;">
            <div>© 2026 Epoch Elites · City Lens v3.0</div>
            <div style="display: flex; gap: 1.5rem;">
                <a href="#" style="color: #6B6B7F; text-decoration: none;">Docs</a>
                <a href="#" style="color: #6B6B7F; text-decoration: none;">Support</a>
                <a href="#" style="color: #6B6B7F; text-decoration: none;">Privacy</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)