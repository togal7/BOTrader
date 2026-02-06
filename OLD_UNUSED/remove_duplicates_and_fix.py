with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== REMOVING DUPLICATE FUNCTIONS ===\n")

new_lines = []
skip_until_line = None

for i, line in enumerate(lines):
    # Jeśli mamy skipować
    if skip_until_line and i < skip_until_line:
        continue
    else:
        skip_until_line = None
    
    # Znajdź pierwszą alerts_history_menu (linia 1931)
    if i == 1930 and 'async def alerts_history_menu' in line:
        print(f"❌ Usuwam pierwszą alerts_history_menu (linia {i+1})")
        # Skipuj do następnej funkcji async def
        for j in range(i+1, len(lines)):
            if lines[j].startswith('async def ') or lines[j].startswith('# ===='):
                skip_until_line = j
                print(f"   Skip do linii {j+1}")
                break
        continue
    
    new_lines.append(line)

print(f"\n✅ Usunięto {len(lines) - len(new_lines)} linii")

# Teraz podmień drugą alerts_history_menu na wersję z kafelkami
content = ''.join(new_lines)

old_second = """async def alerts_history_menu(query, user_id, user):
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
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))"""

new_second = """async def alerts_history_menu(query, user_id, user):
    \"\"\"Show alert history as interactive cards\"\"\"
    history = db.get_alert_history(user_id, limit=20)
    
    if not history:
        text = \"📜 HISTORIA ALERTÓW\\n\\nBrak alertów w historii.\"
        keyboard = [[InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]]
    else:
        recent = history[:10]
        text = \"📜 HISTORIA ALERTÓW\\n\\nOstatnie 10 alertów (kliknij szczegóły):\\n\"
        
        keyboard = []
        for i, alert in enumerate(recent):
            alert_type = alert['alert_type'].upper()
            symbol = alert['symbol'].split('/')[0]
            time = alert.get('triggered_at', alert.get('timestamp', ''))[:16].replace('T', ' ')[11:16]
            
            emoji = {
                'BIG_GAIN': '🚀', 'BIG_LOSS': '📉',
                'OVERSOLD': '🔥', 'OVERBOUGHT': '💎',
                'AI_SIGNAL': '🤖', 'VOLUME_SPIKE': '📊',
                'SUDDEN_CHANGE': '⚡'
            }.get(alert_type, '🔔')
            
            keyboard.append([InlineKeyboardButton(
                f\"{emoji} {symbol} - {time}\",
                callback_data=f'alert_detail_{i}'
            )])
        
        keyboard.append([
            InlineKeyboardButton('🔄 Odśwież', callback_data='alerts_history'),
            InlineKeyboardButton('⬅️ Menu', callback_data='alerts_menu')
        ])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))"""

content = content.replace(old_second, new_second)
print("✅ Replaced with card version")

# Dodaj show_alert_detail jeśli nie ma
if 'async def show_alert_detail' not in content:
    detail_func = """

async def show_alert_detail(query, user_id, user, index):
    \"\"\"Show full alert details\"\"\"
    history = db.get_alert_history(user_id, limit=20)
    
    if index >= len(history):
        await query.answer('❌ Nie znaleziono')
        return
    
    alert = history[index]
    settings = db.get_alert_settings(user_id)
    timeframe = settings.get('alert_timeframe', '1h')
    
    text = f\"\"\"📜 SZCZEGÓŁY ALERTU

{alert['message']}

⏰ {alert.get('triggered_at', alert.get('timestamp', ''))}
🔔 {alert['alert_type'].upper()}\"\"\"
    
    symbol_encoded = alert['symbol'].replace('/', '_').replace(':', '_')
    keyboard = [
        [InlineKeyboardButton(f'📊 Analiza ({timeframe})', callback_data=f'analyze_{symbol_encoded}_{timeframe}')],
        [InlineKeyboardButton('📜 Powrót', callback_data='alerts_history')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

"""
    # Wstaw przed set_alert_timeframe
    insert_point = content.find('async def set_alert_timeframe')
    content = content[:insert_point] + detail_func + content[insert_point:]
    print("✅ Added show_alert_detail")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ Done!")

