with open('handlers.py', 'r') as f:
    content = f.read()

# Znajdź i zamień całą pętlę w show_cached_scan
old_loop = """    keyboard = []
    for r in cached:
        emoji = "🟢" if r['signal'] == 'LONG' else "🔴" if r['signal'] == 'SHORT' else "⚪ "
            clean_symbol = r['symbol'].replace('/USDT:USDT', '')  # BTC/USDT:USDT → BTC
        label = f"{emoji} {r['symbol']} | {r['signal']} {r['score']}pts"
        keyboard.append([InlineKeyboardButton(label, callback_data=f'ai_sig_{clean_symbol}_{timeframe}')])"""

new_loop = """    keyboard = []
    for r in cached:
        emoji = "🟢" if r['signal'] == 'LONG' else "🔴" if r['signal'] == 'SHORT' else "⚪"
        clean_symbol = r['symbol'].replace('/USDT:USDT', '')  # BTC/USDT:USDT → BTC
        display_symbol = r['symbol'].replace(':USDT', '')  # BTC/USDT:USDT → BTC/USDT
        label = f"{emoji} {display_symbol} | {r['signal']} {r['score']}pts"
        keyboard.append([InlineKeyboardButton(label, callback_data=f'ai_sig_{clean_symbol}_{timeframe}')])"""

if old_loop in content:
    content = content.replace(old_loop, new_loop)
    print("✅ Naprawiono pętlę w show_cached_scan")
else:
    print("❌ Nie znaleziono starego kodu - naprawiam ręcznie...")
    
    # Plan B: znajdź linię po linii
    import re
    # Usuń złą linię z wcięciem
    content = re.sub(r'\s+clean_symbol = r\[\'symbol\'\]\.replace\(\'/USDT:USDT\', \'\'\).*\n', '', content)
    
    # Dodaj poprawnie w pętli for r in cached
    pattern = r'(for r in cached:\s+emoji = .*? else "⚪"\s*\n)'
    replacement = r'\1        clean_symbol = r["symbol"].replace("/USDT:USDT", "")\n        display_symbol = r["symbol"].replace(":USDT", "")\n'
    content = re.sub(pattern, replacement, content)
    print("✅ Naprawiono przez regex")

with open('handlers.py', 'w') as f:
    f.write(content)

