with open('alert_scanner.py', 'r') as f:
    content = f.read()

print("=== DISABLING ALERT NOTIFICATIONS ===\n")

# Znajdź funkcję send_alert i zakomentuj wysyłanie Telegrama
old_send = """    async def send_alert(self, user_id, alert_type, symbol, message):
        \"\"\"Send alert notification to user\"\"\"
        try:
            # Save to history
            db.add_alert_history(user_id, alert_type, symbol, message)
            
            # Update anti-spam tracker
            if user_id not in self.last_alerts:
                self.last_alerts[user_id] = {}
            self.last_alerts[user_id][symbol] = datetime.now()
            
            # Send Telegram message (no buttons - won't block bot)
            await self.app.bot.send_message(
                chat_id=user_id,
                text=f"🔔 ALERT\\n\\n{message}\\n\\n💡 Menu → Alerty → Historia",
                parse_mode=None
            )
            
            logger.info(f"✅  Sent {alert_type} alert to {user_id}: {symbol}")
            
        except Exception as e:
            logger.error(f"Failed to send alert: {e}\")"""

new_send = """    async def send_alert(self, user_id, alert_type, symbol, message):
        \"\"\"Send alert notification to user\"\"\"
        try:
            # Save to history
            db.add_alert_history(user_id, alert_type, symbol, message)
            
            # Update anti-spam tracker
            if user_id not in self.last_alerts:
                self.last_alerts[user_id] = {}
            self.last_alerts[user_id][symbol] = datetime.now()
            
            # DON'T send Telegram notification - only save to history
            # User can check: Menu → Alerty → Historia
            
            logger.info(f"✅  Saved {alert_type} alert to history: {user_id} - {symbol}")
            
        except Exception as e:
            logger.error(f"Failed to save alert: {e}\")"""

content = content.replace(old_send, new_send)
print("✅ Disabled Telegram notifications")
print("✅ Alerty zapisują się TYLKO w historii")

with open('alert_scanner.py', 'w') as f:
    f.write(content)

