with open('alert_scanner.py', 'r') as f:
    content = f.read()

print("=== ADDING BACK BUTTON TO ALERTS ===\n")

# Znajdź keyboard w send_alert
old_keyboard = """            keyboard = [
                [InlineKeyboardButton('📜 Zobacz historię', callback_data='alerts_history')],
                [InlineKeyboardButton('⚙️ Ustawienia alertów', callback_data='alerts_settings')]
            ]"""

new_keyboard = """            keyboard = [
                [InlineKeyboardButton('📜 Zobacz historię', callback_data='alerts_history')],
                [InlineKeyboardButton('⚙️ Ustawienia alertów', callback_data='alerts_settings')],
                [InlineKeyboardButton('🏠 Menu główne', callback_data='back_main')]
            ]"""

content = content.replace(old_keyboard, new_keyboard)
print("✅ Added 'Menu główne' button to alerts")

with open('alert_scanner.py', 'w') as f:
    f.write(content)

