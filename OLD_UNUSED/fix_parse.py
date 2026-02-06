import re

with open('handlers.py', 'r') as f:
    content = f.read()

# Znajdź blok elif data.startswith('analyze_'): (linia 406)
pattern = r"(\s+elif data\.startswith\('analyze_'\):.*?\n)(.*?)(?=\s+elif|\s+else|\s+$)"
match = re.search(pattern, content, re.DOTALL)

if match:
    old_block = match.group(0)
    indent = match.group(1)
    
    # Nowa poprawiona logika
    new_block = '''    elif data.startswith('analyze_'):
        await query.answer()
        # analyze_SYMBOL_TIMEFRAME lub analyze_SYMBOL (default z ustawień)
        data_clean = data.replace('analyze_', '')
        
        # Lista możliwych timeframe
        possible_timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
        
        # Sprawdź czy ostatni element to timeframe
        parts = data_clean.split('_')
        symbol_encoded = data_clean
        timeframe = user.get('interval', '15m')  # domyślny z ustawień
        
        # Sprawdź czy ostatni element to timeframe
        if len(parts) > 1 and parts[-1] in possible_timeframes:
            # Format: SYMBOL_TIMEFRAME
            symbol_encoded = '_'.join(parts[:-1])
            timeframe = parts[-1]
        
        # Dekoduj symbol
        symbol = symbol_encoded.replace('_USDT_USDT', '/USDT:USDT').replace('_', '/')
        
        # Dodaj /USDT jeśli brak
        if '/USDT' not in symbol:
            symbol = symbol + '/USDT'
            
        exchange = user.get('selected_exchange', 'mexc').lower()
        await show_pair_analysis(query, user_id, user, symbol, exchange, timeframe, 'manual')
        return
'''
    
    # Zamień
    new_content = content.replace(old_block, new_block)
    
    with open('handlers.py', 'w') as f:
        f.write(new_content)
    
    print('✅ Naprawiono parsowanie analyze_')
else:
    print('❌ Nie znaleziono bloku analyze_')
