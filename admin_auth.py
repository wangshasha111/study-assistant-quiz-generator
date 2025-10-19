"""
Admin Authentication Module
Handles password protection for Admin Dashboard
"""

import os
import streamlit as st
from typing import Optional


def get_admin_password() -> Optional[str]:
    """
    Get admin password from environment variable
    
    Returns:
        str or None: Admin password if set, None otherwise
    """
    return os.getenv("ADMIN_PASSWORD")


def is_admin_enabled() -> bool:
    """
    Check if admin dashboard is enabled
    Admin is disabled if no password is set
    
    Returns:
        bool: True if admin dashboard should be accessible
    """
    password = get_admin_password()
    return password is not None and password.strip() != ""


def check_admin_authentication() -> bool:
    """
    Check if user is authenticated as admin
    Handles authentication UI and session state
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    # Check if admin is enabled
    if not is_admin_enabled():
        st.error("🔒 Admin Dashboard is disabled")
        st.info("To enable Admin Dashboard, set the ADMIN_PASSWORD environment variable.")
        st.code("""
# In your terminal or .env file:
export ADMIN_PASSWORD="your_secure_password"

# Or create a .env file:
ADMIN_PASSWORD=your_secure_password
        """)
        st.stop()
        return False
    
    # Initialize session state for authentication
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    # If already authenticated, return True
    if st.session_state.admin_authenticated:
        return True
    
    # Show login form
    st.title("🔐 Admin Login")
    st.markdown("Please enter the admin password to access the dashboard.")
    
    # Password input
    with st.form("admin_login_form"):
        password_input = st.text_input(
            "Password",
            type="password",
            placeholder="Enter admin password"
        )
        submit_button = st.form_submit_button("🔓 Login", type="primary")
        
        if submit_button:
            admin_password = get_admin_password()
            
            if password_input == admin_password:
                st.session_state.admin_authenticated = True
                st.success("✅ Authentication successful!")
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please try again.")
    
    st.markdown("---")
    st.info("💡 **Tip:** The admin password is set via the ADMIN_PASSWORD environment variable.")
    
    # Stop execution if not authenticated
    st.stop()
    return False


def logout_admin():
    """Logout from admin dashboard"""
    if 'admin_authenticated' in st.session_state:
        st.session_state.admin_authenticated = False


def show_logout_button():
    """Display logout button in sidebar"""
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Logout", help="Logout from admin dashboard"):
            logout_admin()
            st.rerun()
