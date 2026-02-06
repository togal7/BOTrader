with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FINAL COMPLETE FIX ===\n")

# ==========================================
# FIX 1: display_symbol w kafelkach
# ==========================================
print("1. Fixing :USDT in tiles...")

# W ai_scan_execute - kafelki
old_tile = """            clean_symbol = r['symbol'].replace('/USDT', '').replace('/', '')
            label = f\"{emoji} {r['symbol']} | {r['signal']} {r['confidence']}%\""""

new_tile = """            clean_symbol = r['symbol'].replace('/USDT:USDT', '').replace(':USDT', '')
            display_symbol = r['symbol'].replace(':USDT', '')
            label = f\"{emoji} {display_symbol} | {r['signal']} {int(r.get('score', r.get('confidence', 50)))}%~\""""

if old_tile in content:
    content = content.replace(old_tile, new_tile)
    print("   ✅ Fixed tiles in ai_scan_execute")
else:
    print("   ⚠️ Pattern not found - trying alternative...")
    # Alternatywne wyszukiwanie
    import re
    pattern = r"clean_symbol = r\['symbol'\]\.replace\('/USDT', ''\)\.replace\('/', ''\)\s+label = f\"{emoji} {r\['symbol'\]}"
    if re.search(pattern, content):
        content = re.sub(
            pattern,
            """clean_symbol = r['symbol'].replace('/USDT:USDT', '').replace(':USDT', '')
            display_symbol = r['symbol'].replace(':USDT', '')
            label = f\"{emoji} {display_symbol}""",
            content
        )
        print("   ✅ Fixed with regex")

# ==========================================
# FIX 2: Dodaj show_cached_scan
# ==========================================
print("2. Adding show_cached_scan function...")

if 'async def show_cached_scan' not in content:
    # Znajdź koniec ai_scan_execute
    import re
    
    # Wstaw PRZED następną funkcją async def
    pattern = r'(async def ai_scan_execute.*?)(^async def (?!ai_scan_execute))'
    
    new_func = """

async def show_cached_scan(query, user_id, user):
    \"\"\"Show cached scan results\"\"\"
    
    cached = user.get('cached_scan_results')
    
    if not cached or len(cached) == 0:
        logger.info(f"No cache, starting new scan")
        timeframe = user.get('last_timeframe', '30m')
        scan_size = user.get('last_scan_size', 'top50')
        await ai_scan_execute(query, user_id, user, timeframe, scan_size)
        return
    
    logger.info(f"Showing {len(cached)} cached results")
    
    timeframe = user.get('last_timeframe', '30m')
    scan_size = user.get('last_scan_size', 'top50')
    exchange = user.get('selected_exchange', 'mexc')
    
    size_labels = {
        'top10': 'TOP10', 'top20': 'TOP20', 'top30': 'TOP30',
        'top50': 'TOP50', 'top100': 'TOP100', 'all': 'WSZYSTKIE'
    }
    
    tf_labels = {'15m': '15 minut', '30m': '30 minut', '1h': '1 godzina', '4h': '4 godziny'}
    
    text = f\"\"\"🎯 SYGNAŁY AI - {exchange.upper()}

⏱ Timeframe: {tf_labels.get(timeframe, timeframe)}
📊 Zakres: {size_labels.get(scan_size, scan_size.upper())}
🔍 Znaleziono: {len(cached)} sygnałów

{"="*30}
\"\"\"
    
    for i, r in enumerate(cached[:10], 1):
        emoji = "🟢" if r['signal'] == 'LONG' else "🔴" if r['signal'] == 'SHORT' else "⚪"
        display_symbol = r['symbol'].replace(":USDT", "")
        
        text += f\"\"\"{i}. {emoji} {display_symbol}
   {r['signal']} | Pewność: {r['score']}%~

\"\"\"
    
    text += f\"\"\"{"="*30}

💡 Kliknij parę aby zobaczyć szczegóły
⚠️ %~ = wstępna ocena\"\"\"
    
    # Kafelki
    keyboard = []
    for r in cached[:10]:
        clean_symbol = r['symbol'].replace('/USDT:USDT', '').replace(':USDT', '')
        emoji = "🟢" if r['signal'] == 'LONG' else "🔴"
        label = f"{emoji} {clean_symbol} | {r['signal']} {r['score']}%~"
        
        keyboard.append([InlineKeyboardButton(
            label, 
            callback_data=f"ai_sig_{clean_symbol}_{timeframe}"
        )])
    
    keyboard.append([InlineKeyboardButton('🔄 Skanuj ponownie', callback_data=f'ai_scan_tf_{timeframe}')])
    keyboard.append([InlineKeyboardButton('⚙️ Zmień ustawienia', callback_data='ai_scan_menu')])
    keyboard.append([InlineKeyboardButton('⬅️ Menu główne', callback_data='back_main')])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

"""
    
    # Znajdź miejsce wstawienia
    lines = content.split('\n')
    insert_idx = -1
    
    for i, line in enumerate(lines):
        if line.startswith('async def ai_scan_execute'):
            # Szukaj następnej async def
            for j in range(i+1, len(lines)):
                if lines[j].startswith('async def ') and 'ai_scan_execute' not in lines[j]:
                    insert_idx = j
                    break
            break
    
    if insert_idx > 0:
        lines.insert(insert_idx, new_func)
        content = '\n'.join(lines)
        print("   ✅ Added show_cached_scan")
    else:
        print("   ❌ Could not find insertion point")

# ==========================================
# FIX 3: Zapisz cache w ai_scan_execute
# ==========================================
print("3. Adding cache save...")

if "user['cached_scan_results']" not in content:
    old_save = "user['signals_count'] = user.get('signals_count', 0) + len(results)"
    
    new_save = """user['signals_count'] = user.get('signals_count', 0) + len(results)
        user['last_scan_size'] = scan_size
        user['last_timeframe'] = timeframe
        user['cached_scan_results'] = [
            {
                'symbol': r['symbol'],
                'signal': r['signal'],
                'score': int(r.get('score', r.get('confidence', 50)))
            }
            for r in results[:10]
        ]
        logger.info(f"Cached {len(user['cached_scan_results'])} results")"""
    
    content = content.replace(old_save, new_save)
    print("   ✅ Added cache save")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ ALL FIXES APPLIED!")

