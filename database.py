"""
Database module for Study Assistant
Handles multi-user session tracking and activity logging
"""

import sqlite3
import json
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
import os


class DatabaseManager:
    """Manages SQLite database for user sessions and activity tracking"""
    
    def __init__(self, db_path: str = "study_assistant.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                username TEXT,
                ip_address TEXT,
                user_agent TEXT,
                created_at TEXT NOT NULL,
                last_activity TEXT NOT NULL
            )
        """)
        
        # Generations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                file_name TEXT,
                file_size INTEGER,
                content_length INTEGER,
                input_method TEXT,
                summary TEXT,
                quiz TEXT,
                model_used TEXT,
                debug_mode INTEGER,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id)
            )
        """)
        
        # Quiz results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quiz_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                generation_id INTEGER NOT NULL,
                completed_at TEXT NOT NULL,
                score INTEGER,
                total_questions INTEGER,
                percentage REAL,
                answered_count INTEGER,
                user_answers TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions(session_id),
                FOREIGN KEY (generation_id) REFERENCES generations(id)
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sessions_created 
            ON sessions(created_at)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_generations_session 
            ON generations(session_id, timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_quiz_results_session 
            ON quiz_results(session_id, completed_at)
        """)
        
        conn.commit()
        conn.close()
    
    def get_utc_timestamp(self) -> str:
        """Get current UTC timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()
    
    def create_or_update_session(self, session_id: str, username: Optional[str] = None, 
                                 ip_address: Optional[str] = None, 
                                 user_agent: Optional[str] = None):
        """Create a new session or update existing one"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = self.get_utc_timestamp()
        
        # Check if session exists
        cursor.execute("SELECT session_id FROM sessions WHERE session_id = ?", (session_id,))
        exists = cursor.fetchone()
        
        if exists:
            # Update last activity
            cursor.execute("""
                UPDATE sessions 
                SET last_activity = ?,
                    username = COALESCE(?, username),
                    ip_address = COALESCE(?, ip_address),
                    user_agent = COALESCE(?, user_agent)
                WHERE session_id = ?
            """, (now, username, ip_address, user_agent, session_id))
        else:
            # Create new session
            cursor.execute("""
                INSERT INTO sessions (session_id, username, ip_address, user_agent, created_at, last_activity)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (session_id, username, ip_address, user_agent, now, now))
        
        conn.commit()
        conn.close()
    
    def log_generation(self, session_id: str, file_name: Optional[str] = None,
                      file_size: Optional[int] = None, content_length: Optional[int] = None,
                      input_method: str = "text", summary: str = "", quiz: str = "",
                      model_used: str = "", debug_mode: bool = False) -> int:
        """Log a content generation event"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = self.get_utc_timestamp()
        
        cursor.execute("""
            INSERT INTO generations 
            (session_id, timestamp, file_name, file_size, content_length, 
             input_method, summary, quiz, model_used, debug_mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (session_id, now, file_name, file_size, content_length,
              input_method, summary, quiz, model_used, int(debug_mode)))
        
        generation_id = cursor.lastrowid
        
        # Update session last activity
        cursor.execute("""
            UPDATE sessions SET last_activity = ? WHERE session_id = ?
        """, (now, session_id))
        
        conn.commit()
        conn.close()
        
        return generation_id
    
    def log_quiz_result(self, session_id: str, generation_id: int,
                       score: int, total_questions: int, answered_count: int,
                       user_answers: Dict[str, str]):
        """Log quiz completion results"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        now = self.get_utc_timestamp()
        percentage = (score / total_questions * 100) if total_questions > 0 else 0
        
        cursor.execute("""
            INSERT INTO quiz_results 
            (session_id, generation_id, completed_at, score, total_questions, 
             percentage, answered_count, user_answers)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (session_id, generation_id, now, score, total_questions,
              percentage, answered_count, json.dumps(user_answers)))
        
        # Update session last activity
        cursor.execute("""
            UPDATE sessions SET last_activity = ? WHERE session_id = ?
        """, (now, session_id))
        
        conn.commit()
        conn.close()
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session information"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT session_id, username, ip_address, user_agent, created_at, last_activity
            FROM sessions WHERE session_id = ?
        """, (session_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'session_id': row[0],
                'username': row[1],
                'ip_address': row[2],
                'user_agent': row[3],
                'created_at': row[4],
                'last_activity': row[5]
            }
        return None
    
    def get_session_generations(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all generations for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, timestamp, file_name, file_size, content_length,
                   input_method, model_used, debug_mode
            FROM generations 
            WHERE session_id = ?
            ORDER BY timestamp DESC
        """, (session_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'timestamp': row[1],
                'file_name': row[2],
                'file_size': row[3],
                'content_length': row[4],
                'input_method': row[5],
                'model_used': row[6],
                'debug_mode': bool(row[7])
            }
            for row in rows
        ]
    
    def get_session_quiz_results(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all quiz results for a session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT qr.id, qr.generation_id, qr.completed_at, qr.score, 
                   qr.total_questions, qr.percentage, qr.answered_count,
                   g.file_name, g.model_used
            FROM quiz_results qr
            JOIN generations g ON qr.generation_id = g.id
            WHERE qr.session_id = ?
            ORDER BY qr.completed_at DESC
        """, (session_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': row[0],
                'generation_id': row[1],
                'completed_at': row[2],
                'score': row[3],
                'total_questions': row[4],
                'percentage': row[5],
                'answered_count': row[6],
                'file_name': row[7],
                'model_used': row[8]
            }
            for row in rows
        ]
    
    def get_all_sessions_summary(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get summary of all sessions for admin view"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT s.session_id, s.username, s.ip_address, s.created_at, s.last_activity,
                   COUNT(DISTINCT g.id) as generation_count,
                   COUNT(DISTINCT qr.id) as quiz_count
            FROM sessions s
            LEFT JOIN generations g ON s.session_id = g.session_id
            LEFT JOIN quiz_results qr ON s.session_id = qr.session_id
            GROUP BY s.session_id
            ORDER BY s.last_activity DESC
            LIMIT ?
        """, (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                'session_id': row[0],
                'username': row[1],
                'ip_address': row[2],
                'created_at': row[3],
                'last_activity': row[4],
                'generation_count': row[5],
                'quiz_count': row[6]
            }
            for row in rows
        ]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total sessions
        cursor.execute("SELECT COUNT(*) FROM sessions")
        total_sessions = cursor.fetchone()[0]
        
        # Total generations
        cursor.execute("SELECT COUNT(*) FROM generations")
        total_generations = cursor.fetchone()[0]
        
        # Total quiz completions
        cursor.execute("SELECT COUNT(*) FROM quiz_results")
        total_quiz_completions = cursor.fetchone()[0]
        
        # Average quiz score
        cursor.execute("SELECT AVG(percentage) FROM quiz_results")
        avg_score = cursor.fetchone()[0] or 0
        
        # Active sessions (last 24 hours)
        cursor.execute("""
            SELECT COUNT(*) FROM sessions 
            WHERE datetime(last_activity) > datetime('now', '-1 day')
        """)
        active_sessions_24h = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_sessions': total_sessions,
            'total_generations': total_generations,
            'total_quiz_completions': total_quiz_completions,
            'average_quiz_score': round(avg_score, 2),
            'active_sessions_24h': active_sessions_24h
        }
    
    def export_session_data(self, session_id: str, output_path: str):
        """Export all data for a specific session to JSON"""
        session_info = self.get_session_info(session_id)
        if not session_info:
            return False
        
        generations = self.get_session_generations(session_id)
        quiz_results = self.get_session_quiz_results(session_id)
        
        data = {
            'session': session_info,
            'generations': generations,
            'quiz_results': quiz_results,
            'exported_at': self.get_utc_timestamp()
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
