# -*- coding: utf-8 -*-
"""
Initialize demo users in the database
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from components.auth import create_user, load_users, save_users

def init_demo_users():
    """Create demo users if they don't exist"""
    
    demo_users = [
        {
            "email": "admin@citylens.com",
            "password": "Admin123",
            "name": "Admin User",
            "role": "admin",
            "organization": "City Lens"
        },
        {
            "email": "planner@city.gov",
            "password": "Planner123",
            "name": "City Planner",
            "role": "planner",
            "organization": "City Planning Dept"
        },
        {
            "email": "developer@realestate.com",
            "password": "Dev123",
            "name": "Real Estate Developer",
            "role": "enterprise",
            "organization": "Metro Developers"
        },
        {
            "email": "public@citizen.com",
            "password": "Public123",
            "name": "Community Member",
            "role": "public",
            "organization": "Community Board"
        }
    ]
    
    print("Initializing demo users...")
    
    for user in demo_users:
        success, message = create_user(
            email=user["email"],
            password=user["password"],
            name=user["name"],
            role=user["role"],
            organization=user["organization"]
        )
        if success:
            print(f"✅ Created: {user['email']}")
        else:
            print(f"⚠️ {user['email']}: {message}")
    
    print("\nDemo users initialized!")
    print("You can now log in with any of these credentials")

if __name__ == "__main__":
    init_demo_users()