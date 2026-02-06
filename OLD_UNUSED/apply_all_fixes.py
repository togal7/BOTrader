import re

with open('handlers.py', 'r') as f:
    content = f.read()

print("Applying all fixes...")

# ==========================================
# FIX 1: Usuń :USDT z display w kafelkach AI signals
# ==========================================
print("1. Fixing display_symbol in ai_scan_execute...")

old_display = """        clean_symbol = r['symbol'].replace('/USDT', '').replace('/', '')"""
new_display = """        clean_symbol = r['symbol'].replace('/USDT:USDT', '').replace(':USDT', '')
            display_symbol = r["symbol"].replace(":USDT", "")"""

if old_display in content:
    content = content.replace(old_display, new_display)
    print("   ✅ Fixed display_symbol")

# ==========================================
# FIX 2: Zmień pts na %~
# ==========================================
print("2. Changing pts to %~...")
content = content.replace('}pts"', '}%~"')
print("   ✅ Changed pts to %~")

# ==========================================
# FIX 3: Usuń przyciski interwałów i "Więcej wskaźników"
# ==========================================
print("3. Removing interval buttons...")

keyboard_pattern = r"""keyboard = \[
            \[InlineKeyboardButton\('🔄 Odśwież analizę', callback_data=f'analyze_\{clean_symbol\}_\{timeframe\}'\)\],
            \[
                InlineKeyboardButton\('⏱ 15m', callback_data=f'analyze_\{clean_symbol\}_15m'\),
                InlineKeyboardButton\('⏱ 1h', callback_data=f'analyze_\{clean_symbol\}_1h'\),
                InlineKeyboardButton\('⏱ 4h', callback_data=f'analyze_\{clean_symbol\}_4h'\)
            \],
            \[InlineKeyboardButton\('📊 Więcej wskaźników', callback_data=f'details_\{clean_symbol\}_\{timeframe\}'\)\],
            \[InlineKeyboardButton\(back_label, callback_data=back_data\)\]
        \]"""

new_keyboard = """keyboard = [
            [InlineKeyboardButton('🔄 Odśwież analizę', callback_data=f'refresh_analysis_{symbol}_{timeframe}')],
            [InlineKeyboardButton(back_label, callback_data=back_data)]
        ]"""

content = re.sub(keyboard_pattern, new_keyboard, content)
print("   ✅ Removed interval buttons")

# ==========================================
# FIX 4: Dodaj handler refresh_analysis
# ==========================================
print("4. Adding refresh_analysis handler...")

if 'refresh_analysis_' not in content:
    refresh_handler = """
    elif data.startswith('refresh_analysis_'):
        # refresh_analysis_SYMBOL_TIMEFRAME
        parts = data.replace('refresh_analysis_', '').split('_')
        timeframe = parts[-1]
        symbol = '_'.join(parts[:-1])
        exchange = user.get('selected_exchange', 'mexc').lower()
        
        logger.info(f"refresh_analysis: {symbol}, tf={timeframe}")
        await show_pair_analysis(query, user_id, user, symbol, exchange, timeframe, 'ai_signal')
        return
"""
    
    # Wstaw przed show_cached_scan
    insert_point = """    elif data == 'show_cached_scan':"""
    content = content.replace(insert_point, refresh_handler + '\n' + insert_point)
    print("   ✅ Added refresh_analysis handler")

# ==========================================
# FIX 5: Dodaj import datetime
# ==========================================
if 'from datetime import datetime' not in content:
    content = 'from datetime import datetime\n' + content
    print("   ✅ Added datetime import")

# ==========================================
# FIX 6: Timeframe/Exchange pod ceną
# ==========================================
print("5. Moving timeframe under price...")

old_price = """💰 CENA: ${technical['price']:.6f}
📊 Zmiana 24h: {technical['change_24h']:+.2f}%

{reco_text}"""

new_price = """💰 CENA: ${technical['price']:.6f}
📊 Zmiana 24h: {technical['change_24h']:+.2f}%
⏱ Timeframe: {analysis['timeframe']} | 🌐 {analysis['exchange'].upper()} | 🕐 {datetime.now().strftime('%H:%M:%S')}

{reco_text}"""

content = content.replace(old_price, new_price)
print("   ✅ Moved timeframe under price")

# Usuń stary timeframe z dołu
old_tf_bottom = """⏱ Timeframe: {analysis['timeframe']}
🌐 Exchange: {analysis['exchange'].upper()}
🕐 {datetime.now().strftime('%H:%M:%S')}

{'='*30}"""

new_tf_bottom = """{'='*30}"""

content = content.replace(old_tf_bottom, new_tf_bottom)
print("   ✅ Removed old timeframe from bottom")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n🎉 ALL FIXES APPLIED!")

