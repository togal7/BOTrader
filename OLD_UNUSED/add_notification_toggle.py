# 1. Dodaj do database
with open('database.py', 'r') as f:
    db_content = f.read()

print("=== ADDING NOTIFICATION TOGGLE ===\n")

old_defaults = """                'sudden_threshold': 5,  # % threshold for sudden change"""
new_defaults = """                'sudden_threshold': 5,  # % threshold for sudden change
                'notifications_enabled': 1,  # Show alerts on main screen"""

if 'notifications_enabled' not in db_content:
    db_content = db_content.replace(old_defaults, new_defaults)
    print("✅ Added notifications_enabled to database")

with open('database.py', 'w') as f:
    f.write(db_content)

# 2. Dodaj do menu settings
with open('handlers.py', 'r') as f:
    handlers_content = f.read()

# Dodaj przycisk
old_btns = """        [InlineKeyboardButton('⚡ Nagłe zmiany - TF', callback_data='set_sudden_timeframe')],
        [InlineKeyboardButton('⚡ Nagłe zmiany - %', callback_data='set_sudden_threshold')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]"""

new_btns = """        [InlineKeyboardButton('⚡ Nagłe zmiany - TF', callback_data='set_sudden_timeframe')],
        [InlineKeyboardButton('⚡ Nagłe zmiany - %', callback_data='set_sudden_threshold')],
        [InlineKeyboardButton('🔔 Powiadomienia', callback_data='toggle_alert_notifications_enabled')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]"""

handlers_content = handlers_content.replace(old_btns, new_btns)

# Dodaj do statusu
old_status = """⚙️ Ustawienia skanera:
📊 Zakres: TOP {settings['scan_range']}"""

new_status = """🔔 Powiadomienia: {'✅ Włączone' if settings.get('notifications_enabled', 1) else '❌ Wyłączone'}

⚙️ Ustawienia skanera:
📊 Zakres: TOP {settings['scan_range']}"""

handlers_content = handlers_content.replace(old_status, new_status)

with open('handlers.py', 'w') as f:
    f.write(handlers_content)

print("✅ Added notification toggle to menu")

