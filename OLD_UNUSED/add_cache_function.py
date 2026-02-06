with open('handlers.py', 'r') as f:
    content = f.read()

# ==========================================
# 1. Dodaj funkcję show_cached_scan
# ==========================================

# Znajdź miejsce - po ai_scan_execute
insert_after = """async def ai_scan_execute(query, user_id, user, timeframe, scan_size="top10"):"""

# Znajdź koniec ai_scan_execute
import re
pattern = r'(async def ai_scan_execute.*?)(^async def )'
match = re.search(pattern, content, re.MULTILINE | re.DOTALL)

if match:
    ai_scan_end = match.end(1)
    
    new_function = """

async def show_cached_scan(query, user_id, user):
    \"\"\"Pokaż zapisane wyniki skanowania z cache\"\"\"
    
    cached = user.get('cached_scan_results')
    
    if not cached or len(cached) == 0:
        # Brak cache - uruchom nowe skanowanie
        logger.info(f"No cache for user {user_id}, starting new scan")
        timeframe = user.get('last_timeframe', '30m')
        scan_size = user.get('last_scan_size', 'top10')
        await ai_scan_execute(query, user_id, user, timeframe, scan_size)
        return
    
    # Mamy cache - pokaż wyniki
    logger.info(f"Showing {len(cached)} cached results for user {user_id}")
    
    timeframe = user.get('last_timeframe', '30m')
    scan_size = user.get('last_scan_size', 'top10')
    exchange = user.get('selected_exchange', 'mexc')
    
    # Formatuj wyniki jak w ai_scan_execute
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
        
        # Display symbol bez :USDT
        display_symbol = r['symbol'].replace(":USDT", "")
        
        text += f\"\"\"{i}. {emoji} {display_symbol}
   {r['signal']} | Pewność: {r['score']}%~

\"\"\"
    
    text += f\"\"\"{"="*30}

💡 Kliknij parę aby zobaczyć szczegóły
⚠️ %~ = wstępna ocena (pełna analiza po kliknięciu)\"\"\"
    
    # Przyciski - kafelki par
    keyboard = []
    for r in cached[:10]:
        clean_symbol = r['symbol'].replace('/USDT:USDT', '').replace(':USDT', '')
        emoji = "🟢" if r['signal'] == 'LONG' else "🔴"
        label = f"{emoji} {clean_symbol} | {r['signal']} {r['score']}%~"
        
        # callback: ai_sig_SYMBOL_TIMEFRAME
        keyboard.append([InlineKeyboardButton(
            label, 
            callback_data=f"ai_sig_{clean_symbol}_{timeframe}"
        )])
    
    keyboard.append([InlineKeyboardButton('🔄 Skanuj ponownie', callback_data=f'ai_scan_tf_{timeframe}')])
    keyboard.append([InlineKeyboardButton('⚙️ Zmień ustawienia', callback_data='ai_scan_menu')])
    keyboard.append([InlineKeyboardButton('⬅️ Menu główne', callback_data='back_main')])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

"""
    
    # Wstaw nową funkcję
    content = content[:ai_scan_end] + new_function + content[ai_scan_end:]
    
    print("✅ Dodano show_cached_scan")
else:
    print("❌ Nie znaleziono ai_scan_execute")

# ==========================================
# 2. Dodaj zapis cache w ai_scan_execute
# ==========================================

# Znajdź miejsce gdzie zapisujemy user po skanowaniu
pattern2 = r"(user\['signals_count'\] = user\.get\('signals_count', 0\) \+ len\(results\))"

if pattern2 in content:
    old_save = "user['signals_count'] = user.get('signals_count', 0) + len(results)"
    
    new_save = """user['signals_count'] = user.get('signals_count', 0) + len(results)
        user['last_scan_size'] = scan_size
        user['last_timeframe'] = timeframe
        # Cache wyników
        user['cached_scan_results'] = [
            {
                'symbol': r['symbol'],
                'signal': r['signal'],
                'score': int(r.get('score', r.get('confidence', 50)))
            }
            for r in results[:10]
        ]
        logger.info(f"Cached {len(user.get('cached_scan_results', []))} results for user {user_id}")"""
    
    content = content.replace(old_save, new_save)
    print("✅ Dodano cache save")
else:
    print("⚠️ Nie znaleziono signals_count")

with open('handlers.py', 'w') as f:
    f.write(content)

