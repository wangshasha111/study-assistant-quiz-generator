"""
Utility functions for session tracking
"""

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx


def get_session_id() -> str:
    """Get the current Streamlit session ID"""
    ctx = get_script_run_ctx()
    if ctx is None:
        return "unknown"
    return ctx.session_id


def get_client_ip() -> str:
    """
    Get the client's IP address
    Note: This works when Streamlit is behind a proxy with proper headers
    """
    try:
        # Use the new st.context.headers (Streamlit >= 1.29.0)
        if hasattr(st, 'context') and hasattr(st.context, 'headers'):
            headers = st.context.headers
        else:
            # Fallback for older versions
            from streamlit.web.server.websocket_headers import _get_websocket_headers
            headers = _get_websocket_headers()
        
        if headers:
            # Check for common proxy headers
            ip = (headers.get("X-Forwarded-For") or 
                  headers.get("X-Real-Ip") or
                  headers.get("CF-Connecting-IP") or
                  headers.get("True-Client-IP") or
                  "unknown")
            
            # X-Forwarded-For can contain multiple IPs, get the first one
            if ',' in ip:
                ip = ip.split(',')[0].strip()
            
            return ip
    except Exception:
        pass
    
    return "unknown"


def get_user_agent() -> str:
    """Get the user's browser user agent"""
    try:
        # Use the new st.context.headers (Streamlit >= 1.29.0)
        if hasattr(st, 'context') and hasattr(st.context, 'headers'):
            headers = st.context.headers
        else:
            # Fallback for older versions
            from streamlit.web.server.websocket_headers import _get_websocket_headers
            headers = _get_websocket_headers()
        
        if headers:
            return headers.get("User-Agent", "unknown")
    except Exception:
        pass
    
    return "unknown"


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
