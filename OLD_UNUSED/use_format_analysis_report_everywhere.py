with open('handlers.py', 'r') as f:
    content = f.read()

print("=== USING format_analysis_report IN analyze_from_alert ===\n")

# Znajdź i zastąp analyze_from_alert
import re

# Usuń starą funkcję
pattern = r'async def analyze_from_alert\(query, user_id, user, symbol, timeframe\):.*?(?=\nasync def |\nclass |\Z)'
content = re.sub(pattern, '', content, flags=re.DOTALL)
print("✅ Removed old analyze_from_alert")

# Dodaj NOWĄ używającą format_analysis_report
new_function = """async def analyze_from_alert(query, user_id, user, symbol, timeframe):
    \"\"\"Show FULL professional analysis using format_analysis_report\"\"\"
    try:
        await query.answer()
        await query.edit_message_text('⏳ Analizuję...')
        
        exchange = user.get('selected_exchange', 'mexc')
        
        # Use central_analyzer (same as AI Signals)
        from central_ai_analyzer import central_analyzer
        analysis = await central_analyzer.analyze_pair_full(symbol, exchange, timeframe)
        
        if not analysis:
            await query.edit_message_text(
                f"❌ Nie udało się przeanalizować {symbol}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_history')
                ]])
            )
            return
        
        # Format using THE SAME function as AI Signals!
        from languages import get_user_language
        lang = get_user_language(user)
        text = format_analysis_report(analysis, lang)
        
        # Quick intervals at bottom
        intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
        keyboard = []
        symbol_encoded = symbol.replace('/', '_').replace(':', '_')
        
        row = []
        for i, tf in enumerate(intervals):
            emoji_btn = '✅' if tf == timeframe else '⏱'
            row.append(InlineKeyboardButton(
                f'{emoji_btn} {tf}',
                callback_data=f'analyze_{symbol_encoded}_{tf}'
            ))
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

# Wstaw przed show_alert_detail
insert_point = content.find('async def show_alert_detail')
if insert_point == -1:
    print("❌ Nie znaleziono show_alert_detail")
else:
    content = content[:insert_point] + new_function + content[insert_point:]
    print(f"✅ Inserted at position {insert_point}")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ DONE! analyze_from_alert now uses format_analysis_report!")

