with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING SUDDEN CHANGE MENUS ===\n")

# Dodaj funkcje menu przed ostatnim separator
new_functions = """

async def set_sudden_timeframe_menu(query, user_id, user):
    \"\"\"Menu timeframe dla nagłych zmian\"\"\"
    settings = db.get_alert_settings(user_id)
    current = settings.get('sudden_timeframe', '15m')
    
    text = f\"\"\"⚡ NAGŁE ZMIANY - TIMEFRAME

Obecny: {current}

Na jakim interwale sprawdzać nagłe zmiany ceny?

• 5m - bardzo czułe (dużo alertów)
• 15m - czułe ⭐
• 30m - umiarkowane
• 1h - spokojne
• 4h - bardzo spokojne

Przykład: wzrost o 5% w ciągu 15 minut\"\"\"
    
    keyboard = [
        [InlineKeyboardButton('5m', callback_data='set_sudden_tf_5m'),
         InlineKeyboardButton('15m', callback_data='set_sudden_tf_15m'),
         InlineKeyboardButton('30m', callback_data='set_sudden_tf_30m')],
        [InlineKeyboardButton('1h', callback_data='set_sudden_tf_1h'),
         InlineKeyboardButton('4h', callback_data='set_sudden_tf_4h')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_settings')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def set_sudden_timeframe(query, user_id, user, tf):
    \"\"\"Ustaw timeframe dla nagłych zmian\"\"\"
    db.update_alert_settings(user_id, {'sudden_timeframe': tf})
    await query.answer(f'✅ Timeframe nagłych zmian: {tf}')
    await alerts_settings_menu(query, user_id, user)


async def set_sudden_threshold_menu(query, user_id, user):
    \"\"\"Menu progu % dla nagłych zmian\"\"\"
    settings = db.get_alert_settings(user_id)
    current = settings.get('sudden_threshold', 5)
    tf = settings.get('sudden_timeframe', '15m')
    
    text = f\"\"\"⚡ NAGŁE ZMIANY - PRÓG %

Obecny: ±{current}% w {tf}

Jaka zmiana% ma wywołać alert?

• 3% - bardzo czułe (dużo alertów)
• 5% - czułe ⭐
• 7% - umiarkowane
• 10% - spokojne
• 15% - tylko duże ruchy

Alert przyjdzie gdy cena zmieni się o wybrany % w czasie {tf}.\"\"\"
    
    keyboard = [
        [InlineKeyboardButton('3%', callback_data='set_sudden_th_3'),
         InlineKeyboardButton('5%', callback_data='set_sudden_th_5'),
         InlineKeyboardButton('7%', callback_data='set_sudden_th_7')],
        [InlineKeyboardButton('10%', callback_data='set_sudden_th_10'),
         InlineKeyboardButton('15%', callback_data='set_sudden_th_15')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_settings')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def set_sudden_threshold(query, user_id, user, threshold):
    \"\"\"Ustaw próg % dla nagłych zmian\"\"\"
    db.update_alert_settings(user_id, {'sudden_threshold': threshold})
    await query.answer(f'✅ Próg nagłych zmian: ±{threshold}%')
    await alerts_settings_menu(query, user_id, user)

"""

# Wstaw przed ostatnim separatorem
insert_point = content.rfind("# ==========================================")
content = content[:insert_point] + new_functions + content[insert_point:]

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Added sudden change menu functions")

