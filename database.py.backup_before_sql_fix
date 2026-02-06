import json
import os
from datetime import datetime, timedelta
from config import logger, FREE_TRIAL_DAYS, SUBSCRIPTION_DAYS

DB_FILE = 'users.json'

class Database:
    def __init__(self):
        self.users = self.load_users()
    
    def load_users(self):
        """Ładuje bazę użytkowników"""
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Błąd ładowania bazy: {e}")
                return {}
        return {}
    
    def save_users(self):
        """Zapisuje bazę użytkowników"""
        try:
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Błąd zapisu bazy: {e}")
    
    def get_user(self, user_id):
        """Pobiera dane użytkownika"""
        user_id = str(user_id)
        if user_id not in self.users:
            # Nowy użytkownik - FREE TRIAL
            self.users[user_id] = {
                'user_id': user_id,
                'subscription_end': (datetime.now() + timedelta(days=FREE_TRIAL_DAYS)).isoformat(),
                'is_blocked': False,
                'created_at': datetime.now().isoformat(),
                'total_signals': 0,
                'selected_exchange': 'MEXC',
                'selected_interval': '15m'
            }
            self.save_users()
            logger.info(f"Nowy użytkownik: {user_id} (FREE TRIAL {FREE_TRIAL_DAYS} dni)")
        
        return self.users[user_id]
    
    def has_active_subscription(self, user_id):
        """Sprawdza czy użytkownik ma aktywną subskrypcję"""
        user = self.get_user(user_id)
        
        if user['is_blocked']:
            return False
        
        sub_end = datetime.fromisoformat(user['subscription_end'])
        return datetime.now() < sub_end
    
    def extend_subscription(self, user_id, days):
        """Przedłuża subskrypcję"""
        user = self.get_user(user_id)
        current_end = datetime.fromisoformat(user['subscription_end'])
        
        # Jeśli wygasła, liczone od teraz
        if current_end < datetime.now():
            new_end = datetime.now() + timedelta(days=days)
        else:
            new_end = current_end + timedelta(days=days)
        
        self.users[str(user_id)]['subscription_end'] = new_end.isoformat()
        self.save_users()
        logger.info(f"Przedłużono subskrypcję dla {user_id} o {days} dni")
        return new_end
    
    def block_user(self, user_id):
        """Blokuje użytkownika"""
        user = self.get_user(user_id)
        self.users[str(user_id)]['is_blocked'] = True
        self.save_users()
        logger.info(f"Zablokowano użytkownika: {user_id}")
    
    def unblock_user(self, user_id):
        """Odblokowuje użytkownika"""
        user = self.get_user(user_id)
        self.users[str(user_id)]['is_blocked'] = False
        self.save_users()
        logger.info(f"Odblokowano użytkownika: {user_id}")
    
    def increment_signals(self, user_id):
        """Inkrementuje licznik sygnałów"""
        user = self.get_user(user_id)
        self.users[str(user_id)]['total_signals'] += 1
        self.save_users()
    
    def set_exchange(self, user_id, exchange):
        """Ustawia wybraną giełdę"""
        user = self.get_user(user_id)
        self.users[str(user_id)]['selected_exchange'] = exchange
        self.save_users()
    
    def set_interval(self, user_id, interval):
        """Ustawia wybrany interwał"""
        user = self.get_user(user_id)
        self.users[str(user_id)]['selected_interval'] = interval
        self.save_users()
    
    def get_all_users(self):
        """Zwraca wszystkich użytkowników"""
        return self.users
    
    def get_stats(self):
        """Statystyki bota"""
        total = len(self.users)
        active = sum(1 for u in self.users.values() if self.has_active_subscription(int(u['user_id'])))
        blocked = sum(1 for u in self.users.values() if u['is_blocked'])
        
        return {
            'total_users': total,
            'active_subscriptions': active,
            'blocked_users': blocked,
            'expired': total - active - blocked
        }


    def get_admin_chat(self, user_id):
        """Get chat history with user"""
        user = self.get_user(user_id)
        return user.get('admin_chat_history', [])
    
    def add_admin_chat_message(self, user_id, from_admin, message, timestamp):
        """Add message to chat history"""
        user = self.get_user(user_id)
        if not user:
            return
        
        if 'admin_chat_history' not in user:
            user['admin_chat_history'] = []
        
        user['admin_chat_history'].append({
            'from_admin': from_admin,
            'message': message,
            'timestamp': timestamp
        })
        
        # Keep only last 50 messages
        user['admin_chat_history'] = user['admin_chat_history'][-50:]
        
        self.update_user(user_id, user)

# Globalna instancja
    
    def add_user(self, user_data):
        """Add new user"""
        user_id = user_data['user_id']
        self.users[user_id] = user_data
        self.save_users()
    
    def update_user(self, user_id, user_data):
        """Update user data"""
        self.users[user_id] = user_data
        self.save_users()
    
    def get_user_count(self):
        """Total user count"""
        return len(self.users)
    
    def get_active_users(self, days=7):
        """Get active users"""
        from datetime import datetime, timedelta
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        return [u for u in self.users.values() if u.get('last_active', '') > cutoff]


    def get_alert_settings(self, user_id):
        """Get alert settings for user"""
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
                'alert_timeframe': '1h',  # Timeframe for technical alerts
                'sudden_change_enabled': 0,  # Sudden price change alert
                'sudden_timeframe': '15m',  # Timeframe for sudden changes
                'sudden_threshold': 5,  # % threshold for sudden change
                'notifications_enabled': 1,  # Show alerts on main screen
                'min_confidence': 70,
                'gain_threshold': 15,
                'loss_threshold': 15,
                'volume_multiplier': 3.0,
                'quiet_hours': 0
            }
            self.update_user(user_id, user)
        
        return user['alert_settings']
    
    def update_alert_settings(self, user_id, settings):
        """Update alert settings"""
        user = self.get_user(user_id)
        
        if 'alert_settings' not in user:
            user['alert_settings'] = {}
        
        user['alert_settings'].update(settings)
        self.update_user(user_id, user)
    
    def add_alert_history(self, user_id, alert_type, symbol, message):
        """Add alert to history"""
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
        """Get alert history for user"""
        user = self.get_user(user_id)
        
        if 'alert_history' not in user:
            return []
        
        return user['alert_history'][:limit]
    
db = Database()

