# 1. Dodaj nowe pola do database
with open('database.py', 'r') as f:
    db_content = f.read()

print("=== ADDING SUDDEN CHANGE ALERTS ===\n")

# Dodaj do defaultów
old_defaults = """                'alert_timeframe': '1h',  # Timeframe for technical alerts"""
new_defaults = """                'alert_timeframe': '1h',  # Timeframe for technical alerts
                'sudden_change_enabled': 0,  # Sudden price change alert
                'sudden_timeframe': '15m',  # Timeframe for sudden changes
                'sudden_threshold': 5,  # % threshold for sudden change"""

if 'sudden_change_enabled' not in db_content:
    db_content = db_content.replace(old_defaults, new_defaults)
    print("✅ Added sudden change settings to database")

with open('database.py', 'w') as f:
    f.write(db_content)

# 2. Dodaj do menu ustawień
with open('handlers.py', 'r') as f:
    handlers_content = f.read()

# Dodaj przycisk w alerts_settings_menu
old_buttons = """        [btn('MACD Cross', 'macd_cross_enabled')],
        [btn('EMA Cross', 'ema_cross_enabled')],"""

new_buttons = """        [btn('MACD Cross', 'macd_cross_enabled')],
        [btn('EMA Cross', 'ema_cross_enabled')],
        [btn('Nagłe Zmiany', 'sudden_change_enabled')],"""

handlers_content = handlers_content.replace(old_buttons, new_buttons)

# Dodaj do statusu w alerts_menu
old_status = """{status(settings['ema_cross_enabled'])} EMA Cross

⚙️ Ustawienia skanera:"""

new_status = """{status(settings['ema_cross_enabled'])} EMA Cross
{status(settings.get('sudden_change_enabled', 0))} Nagłe Zmiany ({settings.get('sudden_timeframe', '15m')}, ±{settings.get('sudden_threshold', 5)}%)

⚙️ Ustawienia skanera:"""

handlers_content = handlers_content.replace(old_status, new_status)

# Dodaj callback dla sudden settings
old_callbacks = """    elif data == 'set_alert_timeframe':
        await set_alert_timeframe(query, user_id, user)
        return"""

new_callbacks = """    elif data == 'set_alert_timeframe':
        await set_alert_timeframe(query, user_id, user)
        return
    
    elif data == 'set_sudden_timeframe':
        await set_sudden_timeframe_menu(query, user_id, user)
        return
    
    elif data.startswith('set_sudden_tf_'):
        tf = data.replace('set_sudden_tf_', '')
        await set_sudden_timeframe(query, user_id, user, tf)
        return
    
    elif data == 'set_sudden_threshold':
        await set_sudden_threshold_menu(query, user_id, user)
        return
    
    elif data.startswith('set_sudden_th_'):
        threshold = int(data.replace('set_sudden_th_', ''))
        await set_sudden_threshold(query, user_id, user, threshold)
        return"""

handlers_content = handlers_content.replace(old_callbacks, new_callbacks)

# Dodaj przyciski do menu settings
old_settings_btns = """        [InlineKeyboardButton('📈 Timeframe alertów', callback_data='set_alert_timeframe')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]"""

new_settings_btns = """        [InlineKeyboardButton('📈 Timeframe alertów', callback_data='set_alert_timeframe')],
        [InlineKeyboardButton('⚡ Nagłe zmiany - TF', callback_data='set_sudden_timeframe')],
        [InlineKeyboardButton('⚡ Nagłe zmiany - %', callback_data='set_sudden_threshold')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]"""

handlers_content = handlers_content.replace(old_settings_btns, new_settings_btns)

with open('handlers.py', 'w') as f:
    f.write(handlers_content)

print("✅ Added sudden change buttons to menu")

