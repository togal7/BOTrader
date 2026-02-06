with open('handlers.py', 'r') as f:
    content = f.read()

print("=== IMPROVING ALERT CARDS ===\n")

# Znajdź alerts_history_menu i wymień na lepszą wersję
old_history = """async def alerts_history_menu(query, user_id, user):
    \"\"\"Show alert history as interactive cards\"\"\"
    history = db.get_alert_history(user_id, limit=20)
    
    if not history:
        text = "📜 HISTORIA ALERTÓW\\n\\nBrak alertów w historii."
        keyboard = [[InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]]
    else:
        recent = history[:10]
        text = "📜 HISTORIA ALERTÓW\\n\\nOstatnie 10 alertów (kliknij szczegóły):\\n"
        
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
                f"{emoji} {symbol} - {time}",
                callback_data=f'alert_detail_{i}'
            )])
        
        keyboard.append([
            InlineKeyboardButton('🔄 Odśwież', callback_data='alerts_history'),
            InlineKeyboardButton('⬅️ Menu', callback_data='alerts_menu')
        ])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))"""

new_history = """async def alerts_history_menu(query, user_id, user):
    \"\"\"Show alert history as interactive cards\"\"\"
    history = db.get_alert_history(user_id, limit=50)  # More alerts
    
    if not history:
        text = "📜 HISTORIA ALERTÓW\\n\\nBrak alertów w historii."
        keyboard = [[InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]]
    else:
        recent = history[:20]  # Show 20
        text = "📜 HISTORIA ALERTÓW\\n\\nKliknij aby zobaczyć szczegóły i analizę:\\n"
        
        keyboard = []
        for i, alert in enumerate(recent):
            alert_type = alert['alert_type'].upper()
            symbol = alert['symbol'].split('/')[0]
            message = alert['message']
            
            # Extract info from message
            change = ""
            if 'Zmiana 24h:' in message:
                parts = message.split('Zmiana 24h:')
                if len(parts) > 1:
                    change = parts[1].split('\\n')[0].strip()[:10]  # +15.3% or -10.2%
            elif 'WZROST:' in message or 'SPADEK:' in message:
                if '%' in message:
                    # Extract % from sudden change
                    parts = message.split('%')
                    if len(parts) > 1:
                        # Find number before %
                        num_part = parts[0].split()[-1]
                        change = num_part + '%'
            
            time = alert.get('triggered_at', alert.get('timestamp', ''))[:16].replace('T', ' ')[5:]  # MM-DD HH:MM
            
            emoji = {
                'BIG_GAIN': '🚀', 'BIG_LOSS': '📉',
                'OVERSOLD': '🔥', 'OVERBOUGHT': '💎',
                'AI_SIGNAL': '🤖', 'VOLUME_SPIKE': '📊',
                'SUDDEN_CHANGE': '⚡'
            }.get(alert_type, '🔔')
            
            # Better button text: emoji + symbol + change + time
            button_text = f"{emoji} {symbol} {change} | {time}"
            
            keyboard.append([InlineKeyboardButton(
                button_text,
                callback_data=f'alert_detail_{i}'
            )])
        
        keyboard.append([
            InlineKeyboardButton('🔄 Odśwież', callback_data='alerts_history'),
            InlineKeyboardButton('⬅️ Menu', callback_data='alerts_menu')
        ])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))"""

content = content.replace(old_history, new_history)
print("✅ Improved alert cards with change% and more info")

# Popraw show_alert_detail - dodaj BEZPOŚREDNI przycisk analizy
old_detail = """async def show_alert_detail(query, user_id, user, index):
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
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))"""

new_detail = """async def show_alert_detail(query, user_id, user, index):
    \"\"\"Show full alert details with DIRECT analysis\"\"\"
    history = db.get_alert_history(user_id, limit=50)
    
    if index >= len(history):
        await query.answer('❌ Nie znaleziono')
        return
    
    alert = history[index]
    symbol = alert['symbol']
    
    # Get user settings
    settings = db.get_alert_settings(user_id)
    timeframe = settings.get('alert_timeframe', '1h')
    exchange = user.get('selected_exchange', 'mexc')
    
    # Show loading
    await query.edit_message_text('⏳ Ładuję analizę...')
    
    try:
        # Run analysis DIRECTLY
        from central_ai_analyzer import central_analyzer
        analysis = await central_analyzer.analyze_pair_full(symbol, exchange, timeframe)
        
        if not analysis:
            raise Exception("Brak analizy")
        
        # Format result
        signal = analysis.get('signal', 'NEUTRAL')
        confidence = analysis.get('confidence', 0)
        rsi = analysis.get('rsi', 0)
        
        signal_emoji = {'LONG': '🟢', 'SHORT': '🔴', 'NEUTRAL': '⚪'}.get(signal, '⚪')
        
        text = f\"\"\"📊 ANALIZA: {symbol.split('/')[0]}

🔔 Alert: {alert['alert_type'].upper()}
⏰ {alert.get('triggered_at', '')[:16]}

{signal_emoji} Sygnał: {signal}
🎯 Pewność: {confidence}%
📈 RSI: {rsi:.1f}
⏱ Interwał: {timeframe}

━━━━━━━━━━━━━━━━
⚡ Szybka zmiana interwału:\"\"\"
        
        # Quick interval buttons
        intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
        keyboard = []
        symbol_encoded = symbol.replace('/', '_').replace(':', '_')
        
        row = []
        for i, tf in enumerate(intervals):
            emoji = '✅' if tf == timeframe else '⏱'
            row.append(InlineKeyboardButton(f'{emoji} {tf}', callback_data=f'analyze_{symbol_encoded}_{tf}'))
            
            if len(row) == 3:
                keyboard.append(row)
                row = []
        
        if row:
            keyboard.append(row)
        
        keyboard.append([
            InlineKeyboardButton('📜 Historia', callback_data='alerts_history'),
            InlineKeyboardButton('🏠 Menu', callback_data='back_main')
        ])
        
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        
    except Exception as e:
        text = f\"\"\"❌ Błąd analizy

{alert['message']}

⏰ {alert.get('triggered_at', '')}

Błąd: {str(e)}\"\"\"
        
        keyboard = [[InlineKeyboardButton('📜 Powrót', callback_data='alerts_history')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))"""

content = content.replace(old_detail, new_detail)
print("✅ Added DIRECT analysis to alert details with quick intervals")

with open('handlers.py', 'w') as f:
    f.write(content)

