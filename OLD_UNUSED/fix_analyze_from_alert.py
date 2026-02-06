with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING ANALYZE_FROM_ALERT ===\n")

# Znajdź analyze_from_alert i podmień na działającą wersję
import re

# Znajdź funkcję
pattern = r'async def analyze_from_alert\(.*?\n(?=async def |class |# ====)'
match = re.search(pattern, content, re.DOTALL)

if match:
    print(f"Znaleziono analyze_from_alert, długość: {len(match.group(0))}")
    
    # Nowa wersja BEZ błędów
    new_function = """async def analyze_from_alert(query, user_id, user, symbol, timeframe):
    \"\"\"Show analysis with quick interval buttons\"\"\"
    try:
        # Answer immediately
        await query.answer()
        
        # Show loading
        await query.edit_message_text('⏳ Analizuję...')
        
        exchange = user.get('selected_exchange', 'mexc')
        
        # Import here to avoid circular import
        from central_ai_analyzer import central_analyzer
        
        # Run analysis
        analysis = await central_analyzer.analyze_pair_full(symbol, exchange, timeframe)
        
        if not analysis:
            await query.edit_message_text(
                f"❌ Nie udało się przeanalizować {symbol}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_history')
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
        
        # Quick interval buttons (3x3)
        intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
        keyboard = []
        
        symbol_encoded = symbol.replace('/', '_').replace(':', '_')
        
        # 3 buttons per row
        row = []
        for i, tf in enumerate(intervals):
            emoji_btn = '✅' if tf == timeframe else '⏱'
            row.append(InlineKeyboardButton(
                f'{emoji_btn} {tf}',
                callback_data=f'analyze_{symbol_encoded}_{tf}'
            ))
            
            if len(row) == 3 or i == len(intervals) - 1:
                keyboard.append(row)
                row = []
        
        # Bottom buttons
        keyboard.append([
            InlineKeyboardButton('📜 Historia', callback_data='alerts_history'),
            InlineKeyboardButton('🏠 Menu', callback_data='back_main')
        ])
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except Exception as e:
        logger.error(f"Error in analyze_from_alert: {e}")
        import traceback
        traceback.print_exc()
        
        await query.edit_message_text(
            f"❌ Błąd: {e}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_history')
            ]])
        )

"""
    
    content = re.sub(pattern, new_function, content, flags=re.DOTALL)
    print("✅ Replaced analyze_from_alert")
else:
    print("❌ Nie znaleziono analyze_from_alert")

with open('handlers.py', 'w') as f:
    f.write(content)

