# -*- coding: utf-8 -*-
"""
Authentication component for City Lens
Uses bcrypt for password hashing and JSON file for user storage
"""

import streamlit as st
import bcrypt
import json
import os
from datetime import datetime
import re

# File paths
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')

# Ensure data directory exists
os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def create_user(email, password, name, role="public", organization=""):
    """Create a new user"""
    users = load_users()
    
    # Check if user exists
    if email in users:
        return False, "Email already registered"
    
    # Validate email
    if not validate_email(email):
        return False, "Invalid email format"
    
    # Validate password
    valid, msg = validate_password(password)
    if not valid:
        return False, msg
    
    # Create user
    users[email] = {
        "password_hash": hash_password(password),
        "name": name,
        "role": role,
        "organization": organization,
        "created_at": datetime.now().isoformat(),
        "last_login": None,
        "preferences": {
            "theme": "light",
            "notifications": True
        }
    }
    
    save_users(users)
    return True, "User created successfully"

def authenticate_user(email, password):
    """Authenticate user"""
    users = load_users()
    
    if email not in users:
        return False, None, "Email not found"
    
    user = users[email]
    if verify_password(password, user["password_hash"]):
        # Update last login
        users[email]["last_login"] = datetime.now().isoformat()
        save_users(users)
        return True, user, "Login successful"
    
    return False, None, "Invalid password"

def login_form():
    """Display login form with signup option"""
    st.markdown("""
    <style>
    .auth-container {
        max-width: 450px;
        margin: 0 auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .auth-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .auth-header h1 {
        color: #1E3A8A;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .auth-header p {
        color: #6B7280;
    }
    .auth-tabs {
        display: flex;
        margin-bottom: 2rem;
        border-bottom: 2px solid #E5E7EB;
    }
    .auth-tab {
        flex: 1;
        text-align: center;
        padding: 0.75rem;
        cursor: pointer;
        font-weight: 600;
        color: #6B7280;
        transition: all 0.3s;
    }
    .auth-tab.active {
        color: #1E3A8A;
        border-bottom: 3px solid #1E3A8A;
        margin-bottom: -2px;
    }
    .password-requirements {
        background: #F3F4F6;
        padding: 1rem;
        border-radius: 8px;
        font-size: 0.85rem;
        margin-top: 0.5rem;
    }
    .password-requirements ul {
        margin: 0.5rem 0 0 1rem;
        padding: 0;
    }
    .password-requirements li {
        color: #6B7280;
        margin: 0.2rem 0;
    }
    .password-requirements li.valid {
        color: #10B981;
    }
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        color: #9CA3AF;
        margin: 1.5rem 0;
    }
    .divider::before,
    .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #E5E7EB;
    }
    .divider span {
        padding: 0 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the auth form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        st.markdown('<div class="auth-header">', unsafe_allow_html=True)
        st.image("https://via.placeholder.com/100x100.png?text=🏙️", width=100)
        st.markdown("<h1>Welcome to City Lens</h1>", unsafe_allow_html=True)
        st.markdown("<p>Urban impact forecasting platform</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabs for Login/Signup
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input(
                    "Email",
                    placeholder="Enter your email",
                    key="login_email"
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Enter your password",
                    key="login_password"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    remember = st.checkbox("Remember me")
                
                submitted = st.form_submit_button(
                    "Sign In",
                    type="primary",
                    use_container_width=True
                )
                
                if submitted:
                    if not email or not password:
                        st.error("Please fill in all fields")
                    else:
                        success, user_data, message = authenticate_user(email, password)
                        if success:
                            # Set session state
                            st.session_state['authenticated'] = True
                            st.session_state['user'] = user_data
                            st.session_state['user']['email'] = email
                            st.session_state['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            st.rerun()
                        else:
                            st.error(message)
        
        with tab2:
            with st.form("signup_form"):
                name = st.text_input(
                    "Full Name",
                    placeholder="Enter your full name",
                    key="signup_name"
                )
                
                email = st.text_input(
                    "Email",
                    placeholder="Enter your email",
                    key="signup_email"
                )
                
                organization = st.text_input(
                    "Organization (Optional)",
                    placeholder="Enter your organization",
                    key="signup_org"
                )
                
                role = st.selectbox(
                    "Account Type",
                    options=[
                        "public",
                        "planner",
                        "enterprise"
                    ],
                    format_func=lambda x: {
                        "public": "👤 Public User",
                        "planner": "🏛️ City Planner",
                        "enterprise": "🏢 Enterprise"
                    }.get(x, x),
                    key="signup_role"
                )
                
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a password",
                    key="signup_password",
                    help="Password must be at least 8 characters with uppercase, lowercase, and number"
                )
                
                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Confirm your password",
                    key="signup_confirm"
                )
                
                # Password requirements
                with st.expander("Password Requirements"):
                    if password:
                        requirements = [
                            ("✓" if len(password) >= 8 else "✗", "At least 8 characters"),
                            ("✓" if re.search(r'[A-Z]', password) else "✗", "One uppercase letter"),
                            ("✓" if re.search(r'[a-z]', password) else "✗", "One lowercase letter"),
                            ("✓" if re.search(r'[0-9]', password) else "✗", "One number")
                        ]
                        for status, req in requirements:
                            st.markdown(f"<span style='color: {'green' if '✓' in status else 'red'}'>{status} {req}</span>", unsafe_allow_html=True)
                
                terms = st.checkbox("I agree to the Terms of Service and Privacy Policy")
                
                submitted = st.form_submit_button(
                    "Create Account",
                    type="primary",
                    use_container_width=True
                )
                
                if submitted:
                    # Validation
                    if not all([name, email, password, confirm_password]):
                        st.error("Please fill in all required fields")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif not terms:
                        st.error("Please accept the Terms of Service")
                    else:
                        success, message = create_user(
                            email=email,
                            password=password,
                            name=name,
                            role=role,
                            organization=organization
                        )
                        if success:
                            st.success("✅ Account created successfully! Please log in.")
                            # Auto-fill login form
                            st.session_state['login_email'] = email
                        else:
                            st.error(f"❌ {message}")
        
        # Demo credentials
        st.markdown('<div class="divider"><span>Demo Accounts</span></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👤 Public User", use_container_width=True):
                st.session_state['login_email'] = "public@demo.com"
                # Create demo user if doesn't exist
                create_user(
                    email="public@demo.com",
                    password="Demo1234",
                    name="Demo User",
                    role="public"
                )
                st.rerun()
        
        with col2:
            if st.button("🏛️ City Planner", use_container_width=True):
                st.session_state['login_email'] = "planner@demo.com"
                # Create demo user if doesn't exist
                create_user(
                    email="planner@demo.com",
                    password="Planner123",
                    name="Demo Planner",
                    role="planner",
                    organization="City Planning Dept"
                )
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

def logout():
    """Logout user"""
    for key in ['authenticated', 'user', 'login_time']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def show_user_profile():
    """Display user profile in sidebar"""
    if 'user' in st.session_state:
        user = st.session_state['user']
        
        # User avatar based on role
        avatar = {
            'admin': '👑',
            'planner': '🏛️',
            'enterprise': '🏢',
            'public': '👤'
        }.get(user.get('role', 'public'), '👤')
        
        st.sidebar.markdown("---")
        
        # Profile card
        with st.sidebar.container():
            col1, col2 = st.sidebar.columns([1, 3])
            with col1:
                st.markdown(f"<h1 style='font-size: 2.5rem; margin: 0;'>{avatar}</h1>", unsafe_allow_html=True)
            with col2:
                st.markdown(f"**{user.get('name', 'User')}**")
                st.markdown(f"<small style='color: #6B7280;'>{user.get('role', '').title()}</small>", unsafe_allow_html=True)
                st.markdown(f"<small style='color: #9CA3AF;'>{user.get('organization', 'No Organization')}</small>", unsafe_allow_html=True)
            
            # Account settings expander
            with st.sidebar.expander("⚙️ Account Settings"):
                if st.button("📊 My Projects"):
                    st.info("Your saved projects will appear here")
                if st.button("🔑 Change Password"):
                    st.info("Password change feature coming soon")
                if st.button("🎨 Preferences"):
                    st.info("Preferences coming soon")
            
            # Logout button
            if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
                logout()

def require_auth():
    """
    Require authentication for pages
    """
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    
    if not st.session_state['authenticated']:
        # Show login page with centered layout
        st.set_page_config(
            page_title="City Lens - Authentication",
            page_icon="🏙️",
            layout="centered"
        )
        login_form()
        st.stop()
    
    return st.session_state['user']

def get_current_user():
    """Get current authenticated user"""
    if 'user' in st.session_state:
        return st.session_state['user']
    return None

def has_role(required_roles):
    """Check if user has required role"""
    user = get_current_user()
    if not user:
        return False
    return user.get('role') in required_roles