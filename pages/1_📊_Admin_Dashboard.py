"""
Admin Dashboard for Study Assistant
View all sessions, generations, and quiz results
"""

import streamlit as st
import pandas as pd
from database import DatabaseManager
from session_utils import format_file_size, truncate_text
from admin_auth import check_admin_authentication, show_logout_button
from datetime import datetime


def show_admin_dashboard():
    """Display admin dashboard with all user activity"""
    st.set_page_config(
        page_title="Admin Dashboard - Study Assistant",
        page_icon="📊",
        layout="wide"
    )
    
    # Check authentication first
    if not check_admin_authentication():
        return
    
    st.title("📊 Admin Dashboard")
    st.markdown("Monitor all user sessions and activity")
    
    # Show logout button
    show_logout_button()
    
    # Initialize database
    db = DatabaseManager()
    
    # Get statistics
    stats = db.get_statistics()
    
    # Display statistics
    st.header("📈 Overall Statistics")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Sessions", stats['total_sessions'])
    with col2:
        st.metric("Total Generations", stats['total_generations'])
    with col3:
        st.metric("Quiz Completions", stats['total_quiz_completions'])
    with col4:
        st.metric("Avg Quiz Score", f"{stats['average_quiz_score']:.1f}%")
    with col5:
        st.metric("Active (24h)", stats['active_sessions_24h'])
    
    st.markdown("---")
    
    # Sessions table
    st.header("👥 All Sessions")
    
    # Filters
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        search_query = st.text_input("🔍 Search by Session ID, Username, or IP", "")
    with col_f2:
        limit = st.number_input("Show last N sessions", min_value=10, max_value=1000, value=100)
    
    # Get sessions
    sessions = db.get_all_sessions_summary(limit=limit)
    
    # Filter sessions
    if search_query:
        sessions = [
            s for s in sessions 
            if search_query.lower() in s['session_id'].lower() or
               (s['username'] and search_query.lower() in s['username'].lower()) or
               (s['ip_address'] and search_query.lower() in s['ip_address'].lower())
        ]
    
    if sessions:
        # Convert to DataFrame
        df_sessions = pd.DataFrame(sessions)
        
        # Format timestamps
        df_sessions['created_at'] = pd.to_datetime(df_sessions['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        df_sessions['last_activity'] = pd.to_datetime(df_sessions['last_activity']).dt.strftime('%Y-%m-%d %H:%M:%S UTC')
        
        # Rename columns for display
        df_sessions = df_sessions.rename(columns={
            'session_id': 'Session ID',
            'username': 'Username',
            'ip_address': 'IP Address',
            'created_at': 'Created At',
            'last_activity': 'Last Activity',
            'generation_count': 'Generations',
            'quiz_count': 'Quizzes Taken'
        })
        
        # Display table
        st.dataframe(
            df_sessions,
            use_container_width=True,
            hide_index=True
        )
        
        # Export option
        csv = df_sessions.to_csv(index=False)
        st.download_button(
            label="📥 Download Sessions CSV",
            data=csv,
            file_name=f"sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No sessions found.")
    
    st.markdown("---")
    
    # Session detail view
    st.header("🔍 Session Details")
    
    if sessions:
        session_ids = [s['session_id'] for s in sessions]
        selected_session = st.selectbox(
            "Select a session to view details",
            options=session_ids,
            format_func=lambda x: f"{x[:8]}... - {next((s['username'] or 'Anonymous') for s in sessions if s['session_id'] == x)}"
        )
        
        if selected_session:
            # Get session info
            session_info = db.get_session_info(selected_session)
            
            # Display session info
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.subheader("Session Info")
                st.write(f"**Session ID:** {session_info['session_id'][:16]}...")
                st.write(f"**Username:** {session_info['username'] or 'Anonymous'}")
                st.write(f"**IP Address:** {session_info['ip_address']}")
            with col_s2:
                st.subheader("Timestamps")
                st.write(f"**Created:** {session_info['created_at']}")
                st.write(f"**Last Activity:** {session_info['last_activity']}")
            with col_s3:
                st.subheader("User Agent")
                st.write(truncate_text(session_info['user_agent'] or 'Unknown', 100))
            
            # Get generations
            generations = db.get_session_generations(selected_session)
            
            if generations:
                st.subheader(f"📝 Generations ({len(generations)})")
                
                for gen in generations:
                    with st.expander(f"Generation {gen['id']} - {gen['timestamp']}"):
                        col_g1, col_g2 = st.columns(2)
                        with col_g1:
                            st.write(f"**Timestamp:** {gen['timestamp']}")
                            st.write(f"**Input Method:** {gen['input_method']}")
                            if gen['file_name']:
                                st.write(f"**File:** {gen['file_name']}")
                                if gen['file_size']:
                                    st.write(f"**Size:** {format_file_size(gen['file_size'])}")
                        with col_g2:
                            st.write(f"**Model:** {gen['model_used']}")
                            st.write(f"**Content Length:** {gen['content_length']} chars")
                            st.write(f"**Debug Mode:** {'Yes' if gen['debug_mode'] else 'No'}")
            
            # Get quiz results
            quiz_results = db.get_session_quiz_results(selected_session)
            
            if quiz_results:
                st.subheader(f"✅ Quiz Results ({len(quiz_results)})")
                
                for qr in quiz_results:
                    with st.expander(f"Quiz {qr['id']} - {qr['completed_at']} - Score: {qr['score']}/{qr['total_questions']} ({qr['percentage']:.1f}%)"):
                        col_q1, col_q2 = st.columns(2)
                        with col_q1:
                            st.write(f"**Generation ID:** {qr['generation_id']}")
                            st.write(f"**Completed At:** {qr['completed_at']}")
                            st.write(f"**File:** {qr['file_name'] or 'N/A'}")
                        with col_q2:
                            st.write(f"**Score:** {qr['score']}/{qr['total_questions']}")
                            st.write(f"**Percentage:** {qr['percentage']:.1f}%")
                            st.write(f"**Answered:** {qr['answered_count']}/{qr['total_questions']}")
                        
                        # Grade
                        if qr['percentage'] >= 80:
                            st.success(f"🌟 Excellent ({qr['percentage']:.1f}%)")
                        elif qr['percentage'] >= 60:
                            st.info(f"👍 Good ({qr['percentage']:.1f}%)")
                        else:
                            st.warning(f"📚 Keep Learning ({qr['percentage']:.1f}%)")
            
            # Export session data
            st.markdown("---")
            if st.button(f"📥 Export Session Data ({selected_session[:8]}...)"):
                output_path = f"session_export_{selected_session[:8]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                if db.export_session_data(selected_session, output_path):
                    st.success(f"✅ Session data exported to {output_path}")
                    with open(output_path, 'r') as f:
                        st.download_button(
                            label="📥 Download JSON",
                            data=f.read(),
                            file_name=output_path,
                            mime="application/json"
                        )
                else:
                    st.error("Failed to export session data")


if __name__ == "__main__":
    show_admin_dashboard()
