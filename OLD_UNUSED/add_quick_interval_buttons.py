with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING QUICK INTERVAL BUTTONS ===\n")

# 1. Dodaj callback dla analyze_ z alertów
old_callbacks = """    elif data.startswith('set_sudden_th_'):
        threshold = int(data.replace('set_sudden_th_', ''))
        await set_sudden_threshold(query, user_id, user, threshold)
        return"""

new_callbacks = """    elif data.startswith('set_sudden_th_'):
        threshold = int(data.replace('set_sudden_th_', ''))
        await set_sudden_threshold(query, user_id, user, threshold)
        return
    
    elif data.startswith('analyze_'):
        # Format: analyze_BTC_USDT_USDT_1h
        parts = data.replace('analyze_', '').rsplit('_', 1)
        symbol_encoded = parts[0]
        timeframe = parts[1] if len(parts) > 1 else '1h'
        
        # Decode symbol
        symbol = symbol_encoded.replace('_USDT_USDT', '/USDT:USDT').replace('_', '/')
        
        await analyze_from_alert(query, user_id, user, symbol, timeframe)
        return"""

content = content.replace(old_callbacks, new_callbacks)
print("✅ Added analyze callback")

# 2. Dodaj funkcję analyze_from_alert z quick buttons
new_function = """

async def analyze_from_alert(query, user_id, user, symbol, timeframe):
    \"\"\"Show analysis with quick interval change buttons\"\"\"
    try:
        await query.answer('⏳ Analizuję...')
        
        exchange = user.get('selected_exchange', 'mexc')
        
        # Run analysis
        analysis = await central_analyzer.analyze_pair_full(symbol, exchange, timeframe)
        
        if not analysis:
            await query.edit_message_text(
                f"❌ Nie udało się przeanalizować {symbol}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')
                ]])
            )
            return
        
        # Format analysis result
        signal = analysis.get('signal', 'NEUTRAL')
        confidence = analysis.get('confidence', 0)
        rsi = analysis.get('rsi', 0)
        
        signal_emoji = {
            'LONG': '🟢',
            'SHORT': '🔴',
            'NEUTRAL': '⚪'
        }.get(signal, '⚪')
        
        text = f\"\"\"📊 ANALIZA: {symbol.split('/')[0]}
        
{signal_emoji} Sygnał: {signal}
🎯 Pewność: {confidence}%
📈 RSI: {rsi:.1f}
⏱ Interwał: {timeframe}
🌐 Giełda: {exchange.upper()}

━━━━━━━━━━━━━━━━
⚡ Szybka zmiana interwału:\"\"\"
        
        # Quick interval buttons (3 columns)
        intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
        keyboard = []
        
        # 3 przyciski w rzędzie
        row = []
        for i, tf in enumerate(intervals):
            emoji = '✅' if tf == timeframe else '⏱'
            row.append(InlineKeyboardButton(
                f'{emoji} {tf}',
                callback_data=f'analyze_{symbol.replace("/", "_").replace(":", "_")}_{tf}'
            ))
            
            if len(row) == 3 or i == len(intervals) - 1:
                keyboard.append(row)
                row = []
        
        # Bottom buttons
        keyboard.append([
            InlineKeyboardButton('📜 Historia alertów', callback_data='alerts_history'),
            InlineKeyboardButton('⬅️ Menu', callback_data='back_main')
        ])
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except Exception as e:
        logger.error(f"Error in analyze_from_alert: {e}")
        await query.edit_message_text(
            f"❌ Błąd: {e}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')
            ]])
        )

"""

# Wstaw przed ostatnim separatorem
insert_point = content.rfind("# ==========================================")
content = content[:insert_point] + new_function + content[insert_point:]

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Added quick interval change function")

