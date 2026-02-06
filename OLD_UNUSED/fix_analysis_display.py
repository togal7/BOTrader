with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING ANALYSIS DISPLAY ===\n")

# Znajdź i popraw analyze_from_alert
old_display = """        # Format analysis result
        signal_data = analysis.get('signal', 'NEUTRAL')
        
        # Signal może być dict lub string
        if isinstance(signal_data, dict):
            signal = signal_data.get('direction', 'NEUTRAL')
        else:
            signal = signal_data
        
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
🌐 Giełda: {exchange.upper()}"""

new_display = """        # Format analysis result - BETTER extraction
        signal_data = analysis.get('signal', 'NEUTRAL')
        
        # Signal może być dict lub string
        if isinstance(signal_data, dict):
            signal = signal_data.get('direction', 'NEUTRAL')
        else:
            signal = str(signal_data) if signal_data else 'NEUTRAL'
        
        # Get all indicators - try multiple keys
        confidence = analysis.get('confidence', analysis.get('score', 0))
        rsi = analysis.get('rsi', analysis.get('rsi_14', 0))
        
        # Get more details
        macd = analysis.get('macd', {})
        ema_cross = analysis.get('ema_cross', 'N/A')
        volume_ratio = analysis.get('volume_ratio', 0)
        
        signal_emoji = {
            'LONG': '🟢',
            'SHORT': '🔴',
            'NEUTRAL': '⚪'
        }.get(signal.upper() if signal else 'NEUTRAL', '⚪')
        
        text = f\"\"\"📊 ANALIZA: {symbol.split('/')[0]}
        
{signal_emoji} Sygnał: {signal}
🎯 Pewność: {confidence}%
📈 RSI: {rsi:.1f}
📊 Volume: {volume_ratio:.1f}x
⏱ Interwał: {timeframe}
🌐 Giełda: {exchange.upper()}"""

content = content.replace(old_display, new_display)
print("✅ Improved analysis display")

# Dodaj lepszy error handling dla failed analysis
old_error = """        if not analysis:
            await query.edit_message_text(
                f"❌ Nie udało się przeanalizować {symbol}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_history')
                ]])
            )
            return"""

new_error = """        if not analysis:
            error_text = f\"\"\"❌ BŁĄD ANALIZY

Symbol: {symbol}
Interwał: {timeframe}
Giełda: {exchange}

Możliwe przyczyny:
• Brak danych dla tego interwału
• Symbol niepoprawny
• Problem z API giełdy

Spróbuj innego interwału.\"\"\"
            
            # Show interval buttons anyway
            intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']
            keyboard = []
            symbol_encoded = symbol.replace('/', '_').replace(':', '_')
            
            row = []
            for i, tf in enumerate(intervals):
                row.append(InlineKeyboardButton(f'⏱ {tf}', callback_data=f'analyze_{symbol_encoded}_{tf}'))
                if len(row) == 3:
                    keyboard.append(row)
                    row = []
            if row:
                keyboard.append(row)
            
            keyboard.append([InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_history')])
            
            await query.edit_message_text(error_text, reply_markup=InlineKeyboardMarkup(keyboard))
            return"""

content = content.replace(old_error, new_error)
print("✅ Improved error handling")

with open('handlers.py', 'w') as f:
    f.write(content)

