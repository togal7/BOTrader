with open('database.py', 'r') as f:
    content = f.read()

print("=== ADDING ALERTS TABLES ===\n")

# Dodaj nowe tabele w __init__
old_init = """        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                subscription_expires TEXT,
                is_premium INTEGER DEFAULT 0,
                is_blocked INTEGER DEFAULT 0,
                selected_exchange TEXT DEFAULT 'mexc',
                interval TEXT DEFAULT '15m',
                language TEXT DEFAULT 'pl',
                last_active TEXT
            )
        ''')"""

new_init = """        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                subscription_expires TEXT,
                is_premium INTEGER DEFAULT 0,
                is_blocked INTEGER DEFAULT 0,
                selected_exchange TEXT DEFAULT 'mexc',
                interval TEXT DEFAULT '15m',
                language TEXT DEFAULT 'pl',
                last_active TEXT
            )
        ''')
        
        # Alert settings per user
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS alert_settings (
                user_id INTEGER PRIMARY KEY,
                oversold_enabled INTEGER DEFAULT 0,
                overbought_enabled INTEGER DEFAULT 0,
                big_gains_enabled INTEGER DEFAULT 0,
                big_losses_enabled INTEGER DEFAULT 0,
                ai_signals_enabled INTEGER DEFAULT 0,
                volume_spike_enabled INTEGER DEFAULT 0,
                macd_cross_enabled INTEGER DEFAULT 0,
                ema_cross_enabled INTEGER DEFAULT 0,
                scan_range INTEGER DEFAULT 50,
                scan_frequency TEXT DEFAULT '15m',
                scan_timeframe TEXT DEFAULT '1h',
                min_confidence INTEGER DEFAULT 70,
                gain_threshold INTEGER DEFAULT 15,
                loss_threshold INTEGER DEFAULT 15,
                volume_multiplier REAL DEFAULT 3.0,
                quiet_hours INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Alert history
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS alert_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                alert_type TEXT,
                symbol TEXT,
                message TEXT,
                triggered_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')"""

content = content.replace(old_init, new_init)

# Dodaj funkcje do zarządzania alertami
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

# Dodaj przed ostatnią funkcją close()
insert_before = "    def close(self):"
content = content.replace(insert_before, new_functions + '\n' + insert_before)

with open('database.py', 'w') as f:
    f.write(content)

print("✅ Added alert_settings table")
print("✅ Added alert_history table")
print("✅ Added alert management functions")

