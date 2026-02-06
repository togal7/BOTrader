with open('handlers.py', 'r') as f:
    content = f.read()

print("=== MAKING HISTORY AS CARDS ===\n")

# Znajdź alerts_history_menu
old_history = """async def alerts_history_menu(query, user_id, user):
    \"\"\"Show alert history\"\"\"
    history = db.get_alert_history(user_id, limit=50)
    
    if not history:
        text = \"📜 HISTORIA ALERTÓW\\n\\nBrak alertów w historii.\"
    else:
        text = \"📜 HISTORIA ALERTÓW\\n\\nOstatnie 50 alertów:\\n\\n\"
        
        for alert in history:
            alert_type = alert['alert_type'].upper()
            symbol = alert['symbol']
            timestamp = alert['timestamp'][:16]  # YYYY-MM-DD HH:MM
            msg = alert['message'][:50]  # First 50 chars
            
            text += f\"🔔 {alert_type}\\n{symbol} - {timestamp}\\n{msg}...\\n\\n\"
    
    keyboard = [[InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))"""

new_history = """async def alerts_history_menu(query, user_id, user):
    \"\"\"Show alert history as interactive cards\"\"\"
    history = db.get_alert_history(user_id, limit=20)  # Reduced to 20 for better UX
    
    if not history:
        text = \"📜 HISTORIA ALERTÓW\\n\\nBrak alertów w historii.\"
        keyboard = [[InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]]
    else:
        # Show only last 10, with pagination later
        recent = history[:10]
        
        text = \"📜 HISTORIA ALERTÓW\\n\\nOstatnie 10 alertów (kliknij aby zobaczyć szczegóły):\\n\"
        
        keyboard = []
        for i, alert in enumerate(recent):
            alert_type = alert['alert_type'].upper()
            symbol = alert['symbol'].split('/')[0]  # Just BTC not BTC/USDT:USDT
            timestamp = alert['timestamp'][11:16]  # Just HH:MM
            
            # Emoji based on type
            emoji = {
                'BIG_GAIN': '🚀',
                'BIG_LOSS': '📉',
                'OVERSOLD': '🔥',
                'OVERBOUGHT': '💎',
                'AI_SIGNAL': '🤖',
                'VOLUME_SPIKE': '📊',
                'SUDDEN_CHANGE': '⚡'
            }.get(alert_type, '🔔')
            
            # Button with icon + symbol + time
            keyboard.append([
                InlineKeyboardButton(
                    f\"{emoji} {symbol} - {timestamp}\",
                    callback_data=f'alert_detail_{i}'
                )
            ])
        
        # Bottom navigation
        keyboard.append([
            InlineKeyboardButton('🔄 Odśwież', callback_data='alerts_history'),
            InlineKeyboardButton('⬅️ Menu', callback_data='alerts_menu')
        ])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))"""

content = content.replace(old_history, new_history)
print("✅ Changed history to card buttons")

# Dodaj handler dla alert_detail
new_detail_handler = """
    elif data.startswith('alert_detail_'):
        index = int(data.replace('alert_detail_', ''))
        await show_alert_detail(query, user_id, user, index)
        return
"""

# Wstaw przed innym callbackiem
insert_point = content.find("    elif data == 'alerts_menu':")
content = content[:insert_point] + new_detail_handler + content[insert_point:]

print("✅ Added alert_detail callback")

# Dodaj funkcję show_alert_detail
detail_function = """

async def show_alert_detail(query, user_id, user, index):
    \"\"\"Show full alert details with analysis button\"\"\"
    history = db.get_alert_history(user_id, limit=20)
    
    if index >= len(history):
        await query.answer('❌ Alert nie znaleziony')
        return
    
    alert = history[index]
    alert_type = alert['alert_type'].upper()
    symbol = alert['symbol']
    timestamp = alert['timestamp']
    message = alert['message']
    
    # Get user's timeframe setting
    settings = db.get_alert_settings(user_id)
    timeframe = settings.get('alert_timeframe', '1h')
    
    text = f\"\"\"📜 SZCZEGÓŁY ALERTU

{message}

⏰ Czas: {timestamp}
🔔 Typ: {alert_type}
\"\"\"
    
    # Buttons
    symbol_encoded = symbol.replace('/', '_').replace(':', '_')
    keyboard = [
        [InlineKeyboardButton(
            f'📊 Analiza {symbol.split("/")[0]} ({timeframe})',
            callback_data=f'analyze_{symbol_encoded}_{timeframe}'
        )],
        [InlineKeyboardButton('📜 Powrót do historii', callback_data='alerts_history')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

"""

# Wstaw przed ostatnim separatorem
insert_point = content.rfind("# ==========================================")
content = content[:insert_point] + detail_function + content[insert_point:]

print("✅ Added show_alert_detail function")

with open('handlers.py', 'w') as f:
    f.write(content)

