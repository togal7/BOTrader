with open('handlers.py', 'r') as f:
    content = f.read()

# Dodaj funkcję scan_size_menu PRZED handle_scan
new_function = """
async def scan_size_menu(query, user_id, user, scan_type):
    \"\"\"Select scan size\"\"\"
    
    scan_names = {
        'gainers': '🚀 WZROSTY',
        'losers': '📉 SPADKI', 
        'rsi_oversold': '🔥 RSI < 20',
        'rsi_overbought': '💎 RSI > 80',
        'volume': '📈 VOLUME TOP'
    }
    
    text = f\"\"\"📊 {scan_names.get(scan_type, 'SKANER')}

Wybierz zakres skanowania:

• TOP 50 - szybkie (~10 sek)
• TOP 100 - średnie (~20 sek)  
• TOP 200 - wolne (~40 sek)
• WSZYSTKIE - najdokładniejsze (~2 min)

Im więcej par, tym lepsze okazje! 💎\"\"\"
    
    keyboard = [
        [InlineKeyboardButton('⚡ TOP 50 (~10s)', callback_data=f'scan_{scan_type}_50')],
        [InlineKeyboardButton('📊 TOP 100 (~20s)', callback_data=f'scan_{scan_type}_100')],
        [InlineKeyboardButton('🔍 TOP 200 (~40s)', callback_data=f'scan_{scan_type}_200')],
        [InlineKeyboardButton('💎 WSZYSTKIE (~2min)', callback_data=f'scan_{scan_type}_all')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='scan_extremes')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

"""

# Wstaw przed handle_scan
insert_point = "async def handle_scan(query, user_id, user, scan_type):"
if insert_point in content:
    content = content.replace(insert_point, new_function + insert_point)
    print("✅ Added scan_size_menu function")

with open('handlers.py', 'w') as f:
    f.write(content)

