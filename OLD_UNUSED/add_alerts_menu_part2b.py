with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING ALERTS MENU - PART 2B ===\n")

# Dodaj pozostałe funkcje
more_functions = """

async def toggle_alert(query, user_id, user, alert_type):
    \"\"\"Toggle alert on/off\"\"\"
    settings = db.get_alert_settings(user_id)
    
    # alert_type to już nazwa pola z db (oversold_enabled, etc.)
    if alert_type in settings:
        new_value = 0 if settings[alert_type] else 1
        db.update_alert_settings(user_id, {alert_type: new_value})
        await query.answer(f"{'✅ Włączono' if new_value else '❌ Wyłączono'} alert")
    
    await alerts_settings_menu(query, user_id, user)


async def set_scan_range(query, user_id, user, range_val=None):
    \"\"\"Set scan range menu\"\"\"
    if range_val:
        db.update_alert_settings(user_id, {'scan_range': range_val})
        await query.answer(f'✅ Ustawiono zakres: TOP {range_val}')
        await alerts_settings_menu(query, user_id, user)
        return
    
    text = \"\"\"📊 ZAKRES SKANOWANIA

Ile par ma być skanowanych?

• TOP 10 - najszybsze
• TOP 50 - balans
• TOP 100 - dokładne
• TOP 200 - bardzo dokładne
• ALL - wszystkie pary (wolne)\"\"\"
    
    keyboard = [
        [InlineKeyboardButton('TOP 10', callback_data='set_scan_range_10'), InlineKeyboardButton('TOP 50', callback_data='set_scan_range_50')],
        [InlineKeyboardButton('TOP 100', callback_data='set_scan_range_100'), InlineKeyboardButton('TOP 200', callback_data='set_scan_range_200')],
        [InlineKeyboardButton('ALL (~700)', callback_data='set_scan_range_9999')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_settings')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def set_scan_frequency(query, user_id, user, freq=None):
    \"\"\"Set scan frequency\"\"\"
    if freq:
        db.update_alert_settings(user_id, {'scan_frequency': freq})
        await query.answer(f'✅ Częstotliwość: {freq}')
        await alerts_settings_menu(query, user_id, user)
        return
    
    text = \"\"\"⏰ CZĘSTOTLIWOŚĆ SKANOWANIA

Jak często bot ma sprawdzać rynek?

• 5m - bardzo często (więcej alertów)
• 15m - balans ⭐
• 30m - rzadziej
• 1h - oszczędne\"\"\"
    
    keyboard = [
        [InlineKeyboardButton('5 minut', callback_data='set_scan_freq_5m'), InlineKeyboardButton('15 minut', callback_data='set_scan_freq_15m')],
        [InlineKeyboardButton('30 minut', callback_data='set_scan_freq_30m'), InlineKeyboardButton('1 godzina', callback_data='set_scan_freq_1h')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_settings')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def alerts_history_menu(query, user_id, user):
    \"\"\"Show alert history\"\"\"
    history = db.get_alert_history(user_id, limit=50)
    
    if not history:
        text = \"\"\"📜 HISTORIA ALERTÓW

Brak alertów w historii.
Włącz alerty w ustawieniach!\"\"\"
        keyboard = [[InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    text = f\"\"\"📜 HISTORIA ALERTÓW

Ostatnie {len(history)} alertów:\\n\\n\"\"\"
    
    for alert in history[:10]:  # Show last 10
        time = alert['triggered_at'][:16].replace('T', ' ')
        text += f\"\"\"🔔 {alert['alert_type'].upper()}
{alert['symbol']} - {time}
{alert['message'][:60]}...\\n\\n\"\"\"
    
    keyboard = [[InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

"""

# Wstaw przed ostatnim separatorem
insert_point = content.rfind("# ==========================================")
if insert_point > 0:
    content = content[:insert_point] + more_functions + content[insert_point:]
    print("✅ Added toggle, set_range, set_frequency, history functions")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ PART 2B DONE")

