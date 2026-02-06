with open('alert_scanner.py', 'r') as f:
    content = f.read()

print("=== ADDING ALERT CARDS WITH ANALYSIS BUTTON ===\n")

# Znajdź send_alert i zamień na kafelki
old_send = """    async def send_alert(self, user_id, alert_type, symbol, message):
        \"\"\"Send alert notification to user\"\"\"
        try:
            # Save to history
            db.add_alert_history(user_id, alert_type, symbol, message)
            
            # Update anti-spam tracker
            if user_id not in self.last_alerts:
                self.last_alerts[user_id] = {}
            self.last_alerts[user_id][symbol] = datetime.now()
            
            # DISABLED - alerts only in history
            # await self.app.bot.send_message(
            #     chat_id=user_id,
            #     text=f"🔔 ALERT\\n\\n{message}\\n\\n💡 Menu → Alerty → Historia",
            #     parse_mode=None
            # )
            
            logger.info(f"✅  Saved {alert_type} alert to history: {user_id} - {symbol}")
            
        except Exception as e:
            logger.error(f"Failed to save alert: {e}\")"""

new_send = """    async def send_alert(self, user_id, alert_type, symbol, message):
        \"\"\"Send alert notification to user\"\"\"
        try:
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            
            # Save to history
            db.add_alert_history(user_id, alert_type, symbol, message)
            
            # Update anti-spam tracker
            if user_id not in self.last_alerts:
                self.last_alerts[user_id] = {}
            self.last_alerts[user_id][symbol] = datetime.now()
            
            # Check if user wants notifications
            settings = db.get_alert_settings(user_id)
            if settings.get('notifications_enabled', 1):
                # Get timeframe for analysis button
                timeframe = settings.get('alert_timeframe', '1h')
                
                # Create alert card with analysis button
                keyboard = [
                    [InlineKeyboardButton(
                        f'📊 Analiza {symbol.split("/")[0]} ({timeframe})',
                        callback_data=f'analyze_{symbol.replace("/", "_").replace(":", "_")}_{timeframe}'
                    )],
                    [InlineKeyboardButton('📜 Historia alertów', callback_data='alerts_history')]
                ]
                
                await self.app.bot.send_message(
                    chat_id=user_id,
                    text=f"🔔 ALERT\\n\\n{message}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=None
                )
                
                logger.info(f"✅  Sent {alert_type} alert to {user_id}: {symbol}")
            else:
                logger.info(f"✅  Saved {alert_type} alert to history (notifications OFF): {user_id} - {symbol}")
            
        except Exception as e:
            logger.error(f"Failed to send alert: {e}\")"""

content = content.replace(old_send, new_send)
print("✅ Added alert cards with analysis button")

with open('alert_scanner.py', 'w') as f:
    f.write(content)

