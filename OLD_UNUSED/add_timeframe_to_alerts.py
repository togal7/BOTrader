
# 1. Dodaj timeframe do ustawień alertów w database.py
with open('database.py', 'r') as f:
    db_content = f.read()

print("=== ADDING TIMEFRAME SETTING ===\n")

# W get_alert_settings dodaj scan_timeframe do default (jeśli nie ma)
old_default = """                'scan_timeframe': '1h',"""
new_default = """                'scan_timeframe': '1h',
                'alert_timeframe': '1h',  # Timeframe for technical alerts"""

if 'alert_timeframe' not in db_content:
    db_content = db_content.replace(old_default, new_default)
    print("✅ Added alert_timeframe to database defaults")

with open('database.py', 'w') as f:
    f.write(db_content)

# 2. Dodaj menu wyboru timeframe w handlers.py
with open('handlers.py', 'r') as f:
    handlers_content = f.read()

# Dodaj callback handler
old_callback = """    elif data == 'set_scan_frequency':
        await set_scan_frequency(query, user_id, user)
        return"""

new_callback = """    elif data == 'set_scan_frequency':
        await set_scan_frequency(query, user_id, user)
        return
    
    elif data == 'set_alert_timeframe':
        await set_alert_timeframe(query, user_id, user)
        return
    
    elif data.startswith('set_alert_tf_'):
        tf = data.replace('set_alert_tf_', '')
        await set_alert_timeframe(query, user_id, user, tf)
        return"""

handlers_content = handlers_content.replace(old_callback, new_callback)

# Dodaj przycisk w alerts_settings_menu
old_settings_menu = """        [InlineKeyboardButton('📊 Zakres skanowania', callback_data='set_scan_range')],
        [InlineKeyboardButton('⏰ Częstotliwość', callback_data='set_scan_frequency')],"""

new_settings_menu = """        [InlineKeyboardButton('📊 Zakres skanowania', callback_data='set_scan_range')],
        [InlineKeyboardButton('⏰ Częstotliwość', callback_data='set_scan_frequency')],
        [InlineKeyboardButton('📈 Timeframe alertów', callback_data='set_alert_timeframe')],"""

handlers_content = handlers_content.replace(old_settings_menu, new_settings_menu)

# Dodaj status timeframe w alerts_menu
old_alert_status = """⚙️ Ustawienia skanera:
📊 Zakres: TOP {settings['scan_range']}
⏰ Częstotliwość: {settings['scan_frequency']}
📈 Timeframe: {settings['scan_timeframe']}"""

new_alert_status = """⚙️ Ustawienia skanera:
📊 Zakres: TOP {settings['scan_range']}
⏰ Częstotliwość: {settings['scan_frequency']}
📈 Timeframe: {settings.get('alert_timeframe', '1h')}"""

handlers_content = handlers_content.replace(old_alert_status, new_alert_status)

# Dodaj funkcję set_alert_timeframe
new_function = """

async def set_alert_timeframe(query, user_id, user, tf=None):
    \"\"\"Set alert timeframe\"\"\"
    if tf:
        db.update_alert_settings(user_id, {'alert_timeframe': tf})
        await query.answer(f'✅ Timeframe alertów: {tf}')
        await alerts_settings_menu(query, user_id, user)
        return
    
    text = \"\"\"📈 TIMEFRAME ALERTÓW

Na jakim interwale sprawdzać wskaźniki?

• 1m, 5m - bardzo krótki (scalping)
• 15m, 30m - krótki (day trading)
• 1h, 4h - średni (swing) ⭐
• 1d, 1w - długi (pozycje)
• 1M - bardzo długi

Wpływa na RSI, MACD, EMA, Volume.
Zmiana 24h zawsze na 1d.\"\"\"
    
    keyboard = [
        [InlineKeyboardButton('1m', callback_data='set_alert_tf_1m'), 
         InlineKeyboardButton('5m', callback_data='set_alert_tf_5m'), 
         InlineKeyboardButton('15m', callback_data='set_alert_tf_15m')],
        [InlineKeyboardButton('30m', callback_data='set_alert_tf_30m'), 
         InlineKeyboardButton('1h', callback_data='set_alert_tf_1h'), 
         InlineKeyboardButton('4h', callback_data='set_alert_tf_4h')],
        [InlineKeyboardButton('8h', callback_data='set_alert_tf_8h'), 
         InlineKeyboardButton('1d', callback_data='set_alert_tf_1d'), 
         InlineKeyboardButton('1w', callback_data='set_alert_tf_1w')],
        [InlineKeyboardButton('1M', callback_data='set_alert_tf_1M')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_settings')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
"""

# Wstaw przed ostatnim separatorem
insert_point = handlers_content.rfind("# ==========================================")
handlers_content = handlers_content[:insert_point] + new_function + handlers_content[insert_point:]

with open('handlers.py', 'w') as f:
    f.write(handlers_content)

print("✅ Added timeframe menu to handlers")

# 3. Użyj alert_timeframe w scannerze
with open('alert_scanner.py', 'r') as f:
    scanner_content = f.read()

# Zamień scan_timeframe na alert_timeframe dla technical indicators
old_tf = """        timeframe = settings['scan_timeframe']"""
new_tf = """        timeframe = settings.get('alert_timeframe', settings.get('scan_timeframe', '1h'))"""

scanner_content = scanner_content.replace(old_tf, new_tf)

with open('alert_scanner.py', 'w') as f:
    f.write(scanner_content)

print("✅ Updated scanner to use alert_timeframe")

print("\n✅ TIMEFRAME SELECTION ADDED!")

