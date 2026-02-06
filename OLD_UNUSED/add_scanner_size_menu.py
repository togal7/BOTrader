with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING SCANNER SIZE SELECTION ===\n")

# 1. Dodaj menu wyboru przed skanowaniem
# Znajdź scan_extremes_menu
old_menu = """async def scan_extremes_menu(query, user_id, user):
    \"\"\"Extreme scanner menu\"\"\"
    keyboard = [
        [InlineKeyboardButton('🚀 Wzrosty', callback_data='scan_gainers')],
        [InlineKeyboardButton('📉 Spadki', callback_data='scan_losers')],
        [InlineKeyboardButton('🔥 RSI < 20', callback_data='scan_rsi_oversold')],
        [InlineKeyboardButton('💎 RSI > 80', callback_data='scan_rsi_overbought')],
        [InlineKeyboardButton('📈 Volume TOP', callback_data='scan_volume')],
        [InlineKeyboardButton('⬅️ Menu główne', callback_data='back_main')]
    ]"""

new_menu = """async def scan_extremes_menu(query, user_id, user):
    \"\"\"Extreme scanner menu\"\"\"
    keyboard = [
        [InlineKeyboardButton('🚀 Wzrosty', callback_data='scan_select_gainers')],
        [InlineKeyboardButton('📉 Spadki', callback_data='scan_select_losers')],
        [InlineKeyboardButton('🔥 RSI < 20', callback_data='scan_select_rsi_oversold')],
        [InlineKeyboardButton('💎 RSI > 80', callback_data='scan_select_rsi_overbought')],
        [InlineKeyboardButton('📈 Volume TOP', callback_data='scan_select_volume')],
        [InlineKeyboardButton('⬅️ Menu główne', callback_data='back_main')]
    ]"""

content = content.replace(old_menu, new_menu)
print("✅ Updated menu - callbacks now use scan_select_")

# 2. Dodaj nową funkcję wyboru zakresu
new_function = """

async def scan_size_menu(query, user_id, user, scan_type):
    \"\"\"Select how many pairs to scan\"\"\"
    
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
• WSZYSTKIE ~742 - najdokładniejsze (~2 min)

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
insert_before = "async def handle_scan(query, user_id, user, scan_type):"
content = content.replace(insert_before, new_function + '\n' + insert_before)
print("✅ Added scan_size_menu function")

# 3. Dodaj handlery dla nowych callbacków
new_handlers = """
    elif data.startswith('scan_select_'):
        scan_type = data.replace('scan_select_', '')
        await scan_size_menu(query, user_id, user, scan_type)
        return
    
    elif data.startswith('scan_') and '_' in data:
        # scan_TYPE_SIZE (np. scan_gainers_50)
        parts = data.replace('scan_', '').rsplit('_', 1)
        if len(parts) == 2:
            scan_type = parts[0]
            size = parts[1]
            await handle_scan(query, user_id, user, f'scan_{scan_type}', int(size) if size.isdigit() else 0)
            return
"""

# Wstaw po elif data.startswith('scan_'):
old_handler = """    elif data.startswith('scan_'):
        await handle_scan(query, user_id, user, data)
        return"""

new_handler = """    elif data.startswith('scan_'):
        # Check if it's old format or new
        if data.count('_') == 1:
            # Old format: scan_gainers
            await handle_scan(query, user_id, user, data, 50)  # Default 50
        elif data.count('_') >= 2:
            # New format: scan_gainers_100
            parts = data.replace('scan_', '').rsplit('_', 1)
            scan_type = f'scan_{parts[0]}'
            size = int(parts[1]) if parts[1].isdigit() else 0
            if size == 0:  # "all"
                size = 9999
            await handle_scan(query, user_id, user, scan_type, size)
        return"""

content = content.replace(old_handler, new_handler)
print("✅ Updated scan_ handlers")

# 4. Zmień handle_scan aby przyjmował size
old_def = "async def handle_scan(query, user_id, user, scan_type):"
new_def = "async def handle_scan(query, user_id, user, scan_type, scan_size=50):"

content = content.replace(old_def, new_def)

# Zmień for symbol in list(futures_symbols):
old_loop = "        for symbol in list(futures_symbols):  # Scan ALL futures"
new_loop = f"""        # Limit to selected size
        scan_limit = scan_size if scan_size < len(futures_symbols) else len(futures_symbols)
        logger.info(f'Scanning {{scan_limit}} / {{len(futures_symbols)}} futures')
        
        for symbol in list(futures_symbols)[:scan_limit]:"""

content = content.replace(old_loop, new_loop)
print("✅ Updated handle_scan to use size limit")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ SCANNER SIZE SELECTION ADDED!")

