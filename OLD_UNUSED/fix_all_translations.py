with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING ALL TRANSLATIONS ===\n")

# ==========================================
# FIX 1: scan_names - użyj t() zamiast hardcode
# ==========================================
print("1. Fixing scan_names...")

old_scan_names = """        scan_names = {
            'scan_gainers': '🚀 WZROSTY',
            'scan_losers': '📉 SPADKI',
            'scan_rsi_oversold': '🔥 RSI < 30',
            'scan_rsi_overbought': '💎 RSI > 70',
            'scan_volume': '📈 VOLUME TOP'
        }"""

new_scan_names = """        # Get user language
        lang = get_user_language(user)
        
        scan_names = {
            'scan_gainers': f\"🚀 {t('gainers', lang)}\",
            'scan_losers': f\"📉 {t('losers', lang)}\",
            'scan_rsi_oversold': f\"🔥 {t('rsi_oversold', lang)}\",
            'scan_rsi_overbought': f\"💎 {t('rsi_overbought', lang)}\",
            'scan_volume': f\"📈 {t('volume_top', lang)}\"
        }"""

content = content.replace(old_scan_names, new_scan_names)
print("   ✅ scan_names now uses t()")

# ==========================================
# FIX 2: :USDT w keyboard skanera
# ==========================================
print("\n2. Fixing :USDT in scanner buttons...")

# Znajdź for r in top_results (nie enumerate!)
old_loop = """        for r in top_results:
            keyboard.append([InlineKeyboardButton("""

new_loop = """        for r in top_results:
            display_symbol = r['symbol'].replace(':USDT', '')
            keyboard.append([InlineKeyboardButton("""

if old_loop in content:
    content = content.replace(old_loop, new_loop)
    
    # Zamień r['symbol'] na display_symbol w buttonach
    # Znajdź linię z InlineKeyboardButton w tym kontekście
    lines = content.split('\n')
    new_lines = []
    in_scanner = False
    
    for i, line in enumerate(lines):
        if 'for r in top_results:' in line:
            in_scanner = True
        
        if in_scanner and 'InlineKeyboardButton' in line and "r['symbol']" in line:
            line = line.replace("r['symbol']", "display_symbol")
            print(f"   ✅ Replaced r['symbol'] with display_symbol")
            in_scanner = False
        
        new_lines.append(line)
    
    content = '\n'.join(new_lines)

# ==========================================
# FIX 3: Dodaj brakujące tłumaczenia do languages.py
# ==========================================
print("\n3. Adding missing translations to languages.py...")

with open('languages.py', 'r') as f:
    lang_content = f.read()

# Sprawdź czy istnieją klucze
missing_keys = []
needed = ['gainers', 'losers', 'rsi_oversold', 'rsi_overbought', 'volume_top', 'found_pairs', 'top_10']

for key in needed:
    if f"'{key}':" not in lang_content:
        missing_keys.append(key)

if missing_keys:
    # Znajdź koniec TRANSLATIONS dict
    insert_pos = lang_content.rfind('}')
    
    new_translations = """,
    'gainers': {'pl': 'WZROSTY', 'en': 'GAINERS', 'it': 'RIALZI'},
    'losers': {'pl': 'SPADKI', 'en': 'LOSERS', 'it': 'RIBASSI'},
    'rsi_oversold': {'pl': 'RSI < 30', 'en': 'RSI < 30', 'it': 'RSI < 30'},
    'rsi_overbought': {'pl': 'RSI > 70', 'en': 'RSI > 70', 'it': 'RSI > 70'},
    'volume_top': {'pl': 'TOP WOLUMEN', 'en': 'VOLUME TOP', 'it': 'VOLUME TOP'},
    'found_pairs': {'pl': 'Znaleziono', 'en': 'Found', 'it': 'Trovato'},
    'top_10': {'pl': 'Top 10', 'en': 'Top 10', 'it': 'Top 10'}"""
    
    lang_content = lang_content[:insert_pos] + new_translations + lang_content[insert_pos:]
    
    with open('languages.py', 'w') as f:
        f.write(lang_content)
    
    print(f"   ✅ Added {len(missing_keys)} translations: {missing_keys}")

# ==========================================
# FIX 4: "Znaleziono" - użyj t()
# ==========================================
print("\n4. Fixing 'Znaleziono' text...")

content = content.replace(
    'text += f"Znaleziono: {len(results)} par\\nTop 10:\\n"',
    'text += f"{t(\'found_pairs\', lang)}: {len(results)} {t(\'pairs\', lang)}\\n{t(\'top_10\', lang)}:\\n"'
)

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ ALL TRANSLATIONS FIXED!")

