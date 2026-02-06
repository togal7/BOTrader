with open('database.py', 'r') as f:
    content = f.read()

print("=== FORCE ADDING ALERT FUNCTIONS ===\n")

# Jeśli już są - skip
if 'get_alert_settings' in content:
    print("⚠️ Functions already exist - skipping")
else:
    # Dodaj przed def close()
    new_functions = """
    def get_alert_settings(self, user_id):
        \"\"\"Get alert settings for user\"\"\"
        cursor = self.conn.execute(
            'SELECT * FROM alert_settings WHERE user_id = ?',
            (user_id,)
        )
        row = cursor.fetchone()
        
        if not row:
            # Create default settings
            self.conn.execute('''
                INSERT INTO alert_settings (user_id)
                VALUES (?)
            ''', (user_id,))
            self.conn.commit()
            return self.get_alert_settings(user_id)
        
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    
    def update_alert_settings(self, user_id, settings):
        \"\"\"Update alert settings\"\"\"
        set_clause = ', '.join([f'{k} = ?' for k in settings.keys()])
        values = list(settings.values()) + [user_id]
        
        self.conn.execute(
            f'UPDATE alert_settings SET {set_clause} WHERE user_id = ?',
            values
        )
        self.conn.commit()
    
    def add_alert_history(self, user_id, alert_type, symbol, message):
        \"\"\"Add alert to history\"\"\"
        from datetime import datetime
        
        self.conn.execute('''
            INSERT INTO alert_history (user_id, alert_type, symbol, message, triggered_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, alert_type, symbol, message, datetime.now().isoformat()))
        self.conn.commit()
        
        # Keep only last 100 alerts per user
        self.conn.execute('''
            DELETE FROM alert_history
            WHERE id IN (
                SELECT id FROM alert_history
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT -1 OFFSET 100
            )
        ''', (user_id,))
        self.conn.commit()
    
    def get_alert_history(self, user_id, limit=50):
        \"\"\"Get alert history for user\"\"\"
        cursor = self.conn.execute('''
            SELECT * FROM alert_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT ?
        ''', (user_id, limit))
        
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
"""
    
    # Wstaw przed def close()
    content = content.replace('    def close(self):', new_functions + '    def close(self):')
    print("✅ Added alert functions to Database class")

with open('database.py', 'w') as f:
    f.write(content)

