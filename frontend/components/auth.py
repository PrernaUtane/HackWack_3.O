# -*- coding: utf-8 -*-
"""
Authentication component for City Lens
Exact match with provided image + password reset + logo
"""

import streamlit as st
import bcrypt
import json
import os
from datetime import datetime
import re
import random
import base64
from pathlib import Path

# File paths
USER_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'users.json')
RESET_CODES_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'reset_codes.json')
os.makedirs(os.path.dirname(USER_DATA_FILE), exist_ok=True)


# ======================
# DATA HANDLING
# ======================

def load_users():
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_reset_codes():
    if os.path.exists(RESET_CODES_FILE):
        try:
            with open(RESET_CODES_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_reset_codes(codes):
    with open(RESET_CODES_FILE, 'w') as f:
        json.dump(codes, f, indent=2)

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
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
    users = load_users()

    if email in users:
        return False, "Email already registered"

    if not validate_email(email):
        return False, "Invalid email format"

    valid, msg = validate_password(password)
    if not valid:
        return False, msg

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
    users = load_users()

    if email not in users:
        return False, None, "Email not found"

    user = users[email]
    if verify_password(password, user["password_hash"]):
        users[email]["last_login"] = datetime.now().isoformat()
        save_users(users)
        return True, user, "Login successful"

    return False, None, "Invalid password"

def generate_reset_code(email):
    """Generate a 6-digit reset code"""
    code = str(random.randint(100000, 999999))
    reset_codes = load_reset_codes()
    reset_codes[email] = {
        "code": code,
        "expires": (datetime.now().timestamp() + 3600),  # 1 hour expiry
        "used": False
    }
    save_reset_codes(reset_codes)
    return code

def verify_reset_code(email, code):
    """Verify reset code"""
    reset_codes = load_reset_codes()
    if email in reset_codes:
        data = reset_codes[email]
        if not data["used"] and data["expires"] > datetime.now().timestamp() and data["code"] == code:
            return True
    return False

def reset_password(email, new_password):
    """Reset user password"""
    users = load_users()
    if email in users:
        users[email]["password_hash"] = hash_password(new_password)
        save_users(users)
        
        # Invalidate reset code
        reset_codes = load_reset_codes()
        if email in reset_codes:
            reset_codes[email]["used"] = True
            save_reset_codes(reset_codes)
        return True
    return False

def send_reset_email(email, code):
    """Simulate sending reset email (in production, use actual SMTP)"""
    # For demo, just show the code
    st.session_state['reset_code_demo'] = code
    return True

def get_image_base64(image_path):
    """Convert image to base64 for embedding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None


# ======================
# UI - EXACT MATCH WITH IMAGE + LOGO
# ======================

def login_form():
    st.set_page_config(
        page_title="City Lens - Login",
        page_icon="🏙️",
        layout="centered"
    )

    # Try to load logo from Downloads folder
    logo_path = r"C:\Users\ASUS\Downloads\logo.png"  # Adjust filename as needed
    logo_base64 = get_image_base64(logo_path)

    # Initialize session state for password reset flow
    if 'reset_step' not in st.session_state:
        st.session_state.reset_step = None
    if 'reset_email' not in st.session_state:
        st.session_state.reset_email = None

    st.markdown("""
    <style>
    /* Main container */
    .main {
        background: white;
    }
    
    .block-container {
        max-width: 450px !important;
        padding: 2rem !important;
        margin: 0 auto !important;
    }
    
    /* Logo/Brand */
    .brand {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin-bottom: 0.5rem;
    }
    
    .brand h1 {
        font-size: 2rem;
        font-weight: 600;
        color: #1E3A8A;
        margin: 0;
        display: inline;
    }
    
    .brand-logo {
        width: 40px;
        height: 40px;
        object-fit: contain;
    }
    
    .brand p {
        color: #6B7280;
        font-size: 0.875rem;
        margin-top: 0.5rem;
    }
    
    /* Form title - NEW COLOR */
    .form-title {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .form-title h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #059669;  /* Changed to green */
    }
    
    /* Create Account title - NEW COLOR */
    .create-account-title h2 {
        color: #7C3AED;  /* Purple color for Create Account */
    }
    
    /* Form labels */
    .stTextInput label {
        color: #374151 !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        margin-bottom: 0.25rem !important;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        background: white !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 6px !important;
        color: #111827 !important;
        padding: 0.625rem 0.875rem !important;
        font-size: 0.875rem !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.05) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #059669 !important;  /* Changed to green */
        box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1) !important;
    }
    
    /* Remember me and Forgot Password row */
    .row-flex {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0;
    }
    
    .stCheckbox > div > label {
        color: #4B5563 !important;
        font-size: 0.875rem !important;
    }
    
    .forgot-link {
        color: #059669;  /* Changed to green */
        font-size: 0.875rem;
        text-decoration: none;
        cursor: pointer;
        background: none;
        border: none;
        padding: 0;
    }
    
    .forgot-link:hover {
        text-decoration: underline;
        color: #047857;
    }
    
    /* Login button - NEW COLOR */
    .stButton > button[kind="primary"] {
        background: #059669 !important;  /* Changed to green */
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.625rem 1rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        width: 100%;
        margin: 1rem 0;
        transition: background 0.2s;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: #047857 !important;  /* Darker green on hover */
    }
    
    /* Divider */
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        color: #9CA3AF;
        font-size: 0.875rem;
        margin: 1rem 0;
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
    
    /* Register button - NEW COLOR */
    .register-btn > button {
        background: white !important;
        color: #7C3AED !important;  /* Purple color */
        border: 2px solid #7C3AED !important;  /* Purple border */
        border-radius: 6px !important;
        padding: 0.625rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        width: 100%;
        transition: all 0.2s;
    }
    
    .register-btn > button:hover {
        background: #7C3AED !important;
        color: white !important;
    }
    
    /* Back button */
    .back-btn > button {
        background: transparent !important;
        color: #6B7280 !important;
        border: none !important;
        font-size: 0.875rem !important;
        padding: 0 !important;
        margin-bottom: 1rem !important;
    }
    
    .back-btn > button:hover {
        color: #111827 !important;
        background: transparent !important;
    }
    
    /* Create Account button in register form */
    .create-account-btn > button {
        background: #7C3AED !important;  /* Purple */
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.625rem 1rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        width: 100%;
        margin: 1rem 0;
    }
    
    .create-account-btn > button:hover {
        background: #6D28D9 !important;  /* Darker purple */
    }
    
    /* Reset password specific */
    .reset-info {
        background: #F3F4F6;
        border-radius: 6px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        color: #4B5563;
        font-size: 0.875rem;
        border: 1px solid #E5E7EB;
    }
    
    .reset-code {
        font-size: 2rem;
        font-weight: 700;
        color: #059669;  /* Changed to green */
        letter-spacing: 4px;
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 6px;
        border: 1px dashed #059669;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Brand header with logo
    logo_html = ""
    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="brand-logo" alt="City Lens Logo">'
    else:
        logo_html = '<span style="font-size: 2rem;">🏙️</span>'

    st.markdown(f"""
    <div class="brand">
        <div class="logo-container">
            {logo_html}
            <h1>City Lens</h1>
        </div>
        <p>Urban Impact Forecasting Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Password Reset Flow
    if st.session_state.reset_step == "forgot":
        st.markdown('<div class="form-title"><h2 style="color: #059669;">Reset Password</h2></div>', unsafe_allow_html=True)
        
        # Back button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Back", key="back_from_forgot"):
                st.session_state.reset_step = None
                st.session_state.reset_email = None
                st.rerun()
        
        # Step 1: Enter Email
        if st.session_state.reset_step == "forgot" and not st.session_state.get('code_sent'):
            with st.form("forgot_form"):
                email = st.text_input("Email ID", placeholder="Enter your email", key="reset_email_input")
                
                submitted = st.form_submit_button("Send Reset Code", use_container_width=True)
                
                if submitted:
                    if not email:
                        st.error("Please enter your email")
                    else:
                        users = load_users()
                        if email in users:
                            # Generate and send code
                            code = generate_reset_code(email)
                            send_reset_email(email, code)
                            st.session_state.reset_email = email
                            st.session_state.code_sent = True
                            st.session_state.reset_step = "verify_code"
                            st.rerun()
                        else:
                            st.error("Email not found")
        
        # Step 2: Verify Code
        elif st.session_state.get('code_sent') and st.session_state.reset_step == "verify_code":
            st.markdown(f"""
            <div class="reset-info">
                A verification code has been sent to<br>
                <strong>{st.session_state.reset_email}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            # Demo code display (remove in production)
            if 'reset_code_demo' in st.session_state:
                st.markdown(f"""
                <div class="reset-code">
                    {st.session_state.reset_code_demo}
                </div>
                <p style="text-align: center; color: #6B7280; font-size: 0.75rem; margin-top: -0.5rem;">
                    (Demo code - shown for testing)
                </p>
                """, unsafe_allow_html=True)
            
            with st.form("verify_form"):
                code = st.text_input("Verification Code", placeholder="Enter 6-digit code", key="verify_code_input")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.form_submit_button("Back"):
                        st.session_state.code_sent = False
                        st.session_state.reset_step = "forgot"
                        st.rerun()
                with col2:
                    submitted = st.form_submit_button("Verify Code", use_container_width=True)
                
                if submitted:
                    if not code:
                        st.error("Please enter verification code")
                    else:
                        if verify_reset_code(st.session_state.reset_email, code):
                            st.session_state.reset_step = "new_password"
                            st.rerun()
                        else:
                            st.error("Invalid or expired code")
        
        # Step 3: New Password
        elif st.session_state.reset_step == "new_password":
            with st.form("new_password_form"):
                new_password = st.text_input("New Password", type="password", placeholder="Enter new password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm new password")
                
                submitted = st.form_submit_button("Reset Password", use_container_width=True)
                
                if submitted:
                    if not new_password or not confirm_password:
                        st.error("Please fill in all fields")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        valid, msg = validate_password(new_password)
                        if valid:
                            if reset_password(st.session_state.reset_email, new_password):
                                st.success("✅ Password reset successful! Please login.")
                                st.session_state.reset_step = None
                                st.session_state.reset_email = None
                                st.session_state.code_sent = False
                                if 'reset_code_demo' in st.session_state:
                                    del st.session_state['reset_code_demo']
                                st.rerun()
                            else:
                                st.error("Failed to reset password")
                        else:
                            st.error(msg)

    # Registration Form
    elif st.session_state.get('show_register'):
        st.markdown('<div class="form-title create-account-title"><h2>Create Account</h2></div>', unsafe_allow_html=True)
        
        # Back button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("← Back", key="back_from_register"):
                st.session_state.show_register = False
                st.rerun()
        
        with st.form("register_form"):
            name = st.text_input("Full Name", placeholder="John Doe")
            email = st.text_input("Email ID", placeholder="john@example.com")
            organization = st.text_input("Organization", placeholder="Optional")
            
            role = st.selectbox(
                "Account Type",
                ["public", "planner", "enterprise"],
                format_func=lambda x: {
                    "public": "👤 Public User",
                    "planner": "🏛️ City Planner",
                    "enterprise": "🏢 Enterprise"
                }.get(x, x)
            )
            
            password = st.text_input("Password", type="password", placeholder="Create password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            
            terms = st.checkbox("I agree to Terms & Conditions")
            
            st.markdown('<div class="create-account-btn">', unsafe_allow_html=True)
            submitted = st.form_submit_button("CREATE ACCOUNT", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            if submitted:
                if not all([name, email, password, confirm_password]):
                    st.error("Please fill in all required fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif not terms:
                    st.error("Please accept Terms")
                else:
                    success, message = create_user(
                        email=email,
                        password=password,
                        name=name,
                        role=role,
                        organization=organization
                    )
                    if success:
                        st.success("✅ Account created! Please login.")
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")

    # Default Login Form - EXACT MATCH TO IMAGE
    else:
        st.markdown('<div class="form-title"><h2>USER LOGIN</h2></div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email ID", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            # Remember me and Forgot Password row
            col1, col2 = st.columns(2)
            with col1:
                remember = st.checkbox("Remember me")
            with col2:
                st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
                forgot_clicked = st.form_submit_button("Forgot Password?", type="secondary")
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Login button (primary)
            login_submitted = st.form_submit_button("LOGIN", type="primary", use_container_width=True)
            
            if forgot_clicked:
                st.session_state.reset_step = "forgot"
                st.rerun()
            
            if login_submitted:
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    success, user_data, message = authenticate_user(email, password)
                    if success:
                        st.session_state['authenticated'] = True
                        st.session_state['user'] = user_data
                        st.session_state['user']['email'] = email
                        st.session_state['login_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        st.rerun()
                    else:
                        st.error(message)
        
        # Divider
        st.markdown("""
        <div class="divider">
            <span>OR</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Register button
        st.markdown('<div class="register-btn">', unsafe_allow_html=True)
        if st.button("REGISTER", key="register_btn", use_container_width=True):
            st.session_state.show_register = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Demo credentials
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1rem; background: #F9FAFB; border-radius: 6px; border: 1px solid #E5E7EB;">
            <p style="color: #4B5563; font-size: 0.75rem; margin: 0 0 0.5rem 0;"><strong>Demo Credentials:</strong></p>
            <p style="color: #6B7280; font-size: 0.75rem; margin: 0;">planner@city.gov / planner123</p>
            <p style="color: #6B7280; font-size: 0.75rem; margin: 0.25rem 0 0 0;">admin@citylens.com / admin123</p>
        </div>
        """, unsafe_allow_html=True)


# ======================
# AUTH CONTROL
# ======================

def logout():
    for key in ['authenticated', 'user', 'login_time']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

def require_auth():
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False

    if not st.session_state['authenticated']:
        login_form()
        st.stop()

    return st.session_state['user']

def get_current_user():
    return st.session_state.get('user', None)

def has_role(required_roles):
    user = get_current_user()
    if not user:
        return False
    return user.get('role') in required_roles