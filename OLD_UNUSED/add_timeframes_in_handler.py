with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING TIMEFRAMES TO MENU ===\n")

# Znajdź change_interval_menu
old_menu = """async def change_interval_menu(query, user_id, user):
    \"\"\"Change interval\"\"\"
    text = "⏰  WYBIERZ INTERWAŁ\\n\\nDostępne:"
    keyboard = []
    for tf_id, tf_data in TIMEFRAMES.items():
        keyboard.append([InlineKeyboardButton(f"{tf_data['label']}", callback_data=f'set_interval_{tf_id}')])
    keyboard.append([InlineKeyboardButton('⬅️ Powrót', callback_data='settings')])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))"""

# Nowa - z HARDCODED interwałami (ominięcie config.py!)
new_menu = """async def change_interval_menu(query, user_id, user):
    \"\"\"Change interval\"\"\"
    text = "⏰  WYBIERZ INTERWAŁ\\n\\nDostępne:"
    
    # Hardcoded timeframes (ominięcie problemu w config.py)
    custom_tfs = {
        '1m': '1 minuta', '5m': '5 minut', '15m': '15 minut', '30m': '30 minut',
        '1h': '1 godzina', '4h': '4 godziny', '12h': '12 godzin',
        '1d': '1 dzień', '3d': '3 dni', '5d': '5 dni',
        '1w': '1 tydzień', '2w': '2 tygodnie',
        '1M': '1 miesiąc', '3M': '3 miesiące', '6M': '6 miesięcy', '1Y': '1 rok'
    }
    
    keyboard = []
    for tf_id, tf_label in custom_tfs.items():
        keyboard.append([InlineKeyboardButton(tf_label, callback_data=f'set_interval_{tf_id}')])
    keyboard.append([InlineKeyboardButton('⬅️ Powrót', callback_data='settings')])
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))"""

content = content.replace(old_menu, new_menu)
print("✅ Added 16 timeframes to menu (hardcoded in handler)")

with open('handlers.py', 'w') as f:
    f.write(content)

