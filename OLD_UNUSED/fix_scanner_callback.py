with open('handlers.py', 'r') as f:
    content = f.read()

# W handle_scan, callback używa analyze_SYMBOL
# Musimy przekonwertować symbol do formatu futures przed callbackiem

# Znajdź gdzie tworzy callback w skanerze
old_callback = """clean_symbol = r['symbol'].replace('/USDT:USDT', '').replace(':USDT', '')
            keyboard.append([InlineKeyboardButton("""

new_callback = """clean_symbol = r['symbol'].replace('/USDT:USDT', '').replace(':USDT', '')
            # Dla callbacka potrzebujemy pełnego symbolu z :USDT (futures format)
            full_symbol = r['symbol'] if ':USDT' in r['symbol'] else r['symbol'].replace('/USDT', '/USDT:USDT')
            keyboard.append([InlineKeyboardButton("""

if old_callback in content:
    content = content.replace(old_callback, new_callback)
    print("✅ Dodano full_symbol przed callbackiem")
    
    # Teraz zamień callback_data z clean_symbol na full_symbol
    # Szukaj: callback_data=f'analyze_{clean_symbol}
    content = content.replace(
        "callback_data=f'analyze_{clean_symbol}",
        "callback_data=f'analyze_{full_symbol}"
    )
    print("✅ Zmieniono callback na full_symbol")

with open('handlers.py', 'w') as f:
    f.write(content)

