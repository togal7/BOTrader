# ============================================
# FIX 1: SEND_ALERT z kafelkami i check notifications
# ============================================
with open('alert_scanner.py', 'r') as f:
    scanner_content = f.read()

print("=== FIXING ALERT SCANNER ===\n")

old_send = """    async def send_alert(self, user_id, alert_type, symbol, message):
        \"\"\"Send alert notification to user\"\"\"
        try:
            # Save to history
            db.add_alert_history(user_id, alert_type, symbol, message)
            # Update anti-spam tracker
            if user_id not in self.last_alerts:
                self.last_alerts[user_id] = {}
            self.last_alerts[user_id][symbol] = datetime.now()
            # Send Telegram message with button
            await self.app.bot.send_message(
                chat_id=user_id,
                text=f"🔔 ALERT\\n\\n{message}",
                parse_mode=None
            )
            logger.info(f"✅  Sent {alert_type} alert to {user_id}: {symbol}")
        except Exception as e:"""

new_send = """    async def send_alert(self, user_id, alert_type, symbol, message):
        \"\"\"Send alert notification to user\"\"\"
        try:
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            
            # Save to history ALWAYS
            db.add_alert_history(user_id, alert_type, symbol, message)
            
            # Update anti-spam tracker
            if user_id not in self.last_alerts:
                self.last_alerts[user_id] = {}
            self.last_alerts[user_id][symbol] = datetime.now()
            
            # Check if user wants notifications
            settings = db.get_alert_settings(user_id)
            notifications_on = settings.get('notifications_enabled', 1)
            
            if notifications_on:
                # Get timeframe for analysis button
                timeframe = settings.get('alert_timeframe', '1h')
                
                # Create alert CARD with analysis button
                symbol_encoded = symbol.replace('/', '_').replace(':', '_')
                keyboard = [
                    [InlineKeyboardButton(
                        f'📊 Analiza {symbol.split("/")[0]} ({timeframe})',
                        callback_data=f'analyze_{symbol_encoded}_{timeframe}'
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
                logger.info(f"✅  Saved {alert_type} to history (notifications OFF): {user_id} - {symbol}")
            
        except Exception as e:"""

scanner_content = scanner_content.replace(old_send, new_send)
print("✅ Fixed send_alert with notifications check + cards")

with open('alert_scanner.py', 'w') as f:
    f.write(scanner_content)

# ============================================
# FIX 2: Dodaj quick intervals pod KAŻDĄ analizą
# ============================================
with open('handlers.py', 'r') as f:
    handlers_content = f.read()

print("\n=== ADDING QUICK INTERVALS EVERYWHERE ===\n")

# Funkcja helper do tworzenia quick interval buttons
helper_function = """

def create_quick_interval_buttons(symbol, current_timeframe, callback_prefix='analyze'):
    \"\"\"Create 3x3 grid of quick interval change buttons\"\"\"
    intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
    keyboard = []
    
    symbol_encoded = symbol.replace('/', '_').replace(':', '_')
    
    # 3 buttons per row
    row = []
    for i, tf in enumerate(intervals):
        emoji = '✅' if tf == current_timeframe else '⏱'
        row.append(InlineKeyboardButton(
            f'{emoji} {tf}',
            callback_data=f'{callback_prefix}_{symbol_encoded}_{tf}'
        ))
        
        if len(row) == 3 or i == len(intervals) - 1:
            keyboard.append(row)
            row = []
    
    return keyboard

"""

# Dodaj helper przed pierwszą funkcją
insert_point = handlers_content.find('async def start_command')
handlers_content = handlers_content[:insert_point] + helper_function + handlers_content[insert_point:]

print("✅ Added quick interval helper function")

with open('handlers.py', 'w') as f:
    f.write(handlers_content)

print("\n✅ ALL FIXES APPLIED!")

