
scanner_code_part3 = """
    
    def should_send_alert(self, user_id, symbol):
        \"\"\"Anti-spam: check if we can send alert for this symbol\"\"\"
        
        if user_id not in self.last_alerts:
            self.last_alerts[user_id] = {}
        
        # Check last alert time for this symbol
        last_time = self.last_alerts[user_id].get(symbol)
        
        if last_time:
            # Don't send same alert for same symbol within 1 hour
            if datetime.now() - last_time < timedelta(hours=1):
                return False
        
        return True
    
    async def send_alert(self, user_id, alert_type, symbol, message):
        \"\"\"Send alert notification to user\"\"\"
        
        try:
            # Save to history
            db.add_alert_history(user_id, alert_type, symbol, message)
            
            # Update anti-spam tracker
            if user_id not in self.last_alerts:
                self.last_alerts[user_id] = {}
            self.last_alerts[user_id][symbol] = datetime.now()
            
            # Send Telegram message
            await self.app.bot.send_message(
                chat_id=user_id,
                text=f"🔔 ALERT\\n\\n{message}",
                parse_mode=None
            )
            
            logger.info(f"✅ Sent {alert_type} alert to {user_id}: {symbol}")
            
        except Exception as e:
            logger.error(f"Error sending alert to {user_id}: {e}")


# Global instance (will be initialized in bot.py)
alert_scanner = None
"""

# Append to existing file
with open('alert_scanner.py', 'a') as f:
    f.write(scanner_code_part3)

print("✅ Completed alert_scanner.py - PART 3")

# Compile check
import py_compile
py_compile.compile('alert_scanner.py')
print("✅ Syntax OK")

