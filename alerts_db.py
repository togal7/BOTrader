"""
Alerts Database - SQLite storage for alert history
Separate from main Database (JSON)
"""
import sqlite3
from datetime import datetime

class AlertsDatabase:
    def __init__(self, db_file='botrader.db'):
        self.db_file = db_file
        self._init_db()
    
    def _init_db(self):
        """Initialize database and create table if needed"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            alert_type TEXT NOT NULL,
            symbol TEXT,
            message TEXT NOT NULL,
            triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_alert(self, user_id, alert_type, symbol, message):
        """Add alert to history"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO alerts_history (user_id, alert_type, symbol, message, triggered_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, alert_type, symbol, message, datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def get_alerts(self, user_id, limit=50):
        """Get alert history for user"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, alert_type, symbol, message, triggered_at
            FROM alerts_history
            WHERE user_id = ?
            ORDER BY triggered_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        # Convert to dict
        alerts = []
        for r in results:
            alerts.append({
                'id': r[0],
                'alert_type': r[1],
                'symbol': r[2],
                'message': r[3],
                'triggered_at': r[4]
            })
        
        return alerts

# Singleton instance
alerts_db = AlertsDatabase()
