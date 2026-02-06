with open('alert_scanner.py', 'r') as f:
    content = f.read()

print("=== ADDING BUTTON TO ALERTS ===\n")

# Znajdź send_alert
old_send = """            # Send Telegram message
            await self.app.bot.send_message(
                chat_id=user_id,
                text=f"🔔 ALERT\\n\\n{message}",
                parse_mode=None
            )"""

new_send = """            # Send Telegram message with button
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            
            keyboard = [
                [InlineKeyboardButton('📜 Zobacz historię', callback_data='alerts_history')],
                [InlineKeyboardButton('⚙️ Ustawienia alertów', callback_data='alerts_settings')]
            ]
            
            await self.app.bot.send_message(
                chat_id=user_id,
                text=f"🔔 ALERT\\n\\n{message}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=None
            )"""

content = content.replace(old_send, new_send)
print("✅ Added buttons to alerts")

with open('alert_scanner.py', 'w') as f:
    f.write(content)

