with open('database.py', 'r') as f:
    content = f.read()

print("=== ADDING ALERTS TO JSON DATABASE ===\n")

# Dodaj funkcje przed "db = Database()"
new_functions = """
    def get_alert_settings(self, user_id):
        \"\"\"Get alert settings for user\"\"\"
        user = self.get_user(user_id)
        
        # Default settings if not exist
        if 'alert_settings' not in user:
            user['alert_settings'] = {
                'oversold_enabled': 0,
                'overbought_enabled': 0,
                'big_gains_enabled': 0,
                'big_losses_enabled': 0,
                'ai_signals_enabled': 0,
                'volume_spike_enabled': 0,
                'macd_cross_enabled': 0,
                'ema_cross_enabled': 0,
                'scan_range': 50,
                'scan_frequency': '15m',
                'scan_timeframe': '1h',
                'min_confidence': 70,
                'gain_threshold': 15,
                'loss_threshold': 15,
                'volume_multiplier': 3.0,
                'quiet_hours': 0
            }
            self.update_user(user_id, user)
        
        return user['alert_settings']
    
    def update_alert_settings(self, user_id, settings):
        \"\"\"Update alert settings\"\"\"
        user = self.get_user(user_id)
        
        if 'alert_settings' not in user:
            user['alert_settings'] = {}
        
        user['alert_settings'].update(settings)
        self.update_user(user_id, user)
    
    def add_alert_history(self, user_id, alert_type, symbol, message):
        \"\"\"Add alert to history\"\"\"
        from datetime import datetime
        
        user = self.get_user(user_id)
        
        if 'alert_history' not in user:
            user['alert_history'] = []
        
        alert = {
            'alert_type': alert_type,
            'symbol': symbol,
            'message': message,
            'triggered_at': datetime.now().isoformat()
        }
        
        user['alert_history'].insert(0, alert)
        
        # Keep only last 100
        user['alert_history'] = user['alert_history'][:100]
        
        self.update_user(user_id, user)
    
    def get_alert_history(self, user_id, limit=50):
        \"\"\"Get alert history for user\"\"\"
        user = self.get_user(user_id)
        
        if 'alert_history' not in user:
            return []
        
        return user['alert_history'][:limit]
    
"""

# Wstaw przed "db = Database()"
content = content.replace('db = Database()', new_functions + 'db = Database()')

with open('database.py', 'w') as f:
    f.write(content)

print("✅ Added alert functions to JSON Database")

