# ==========================================
# POPRAW wszystkie wywołania w całym projekcie
# ==========================================

import re

files = ['central_ai_analyzer.py', 'ai_signals_advanced.py', 'handlers.py']

for filename in files:
    print(f"\n=== {filename} ===")
    
    with open(filename, 'r') as f:
        content = f.read()
    
    # Znajdź wszystkie wywołania get_ohlcv
    # Pattern: get_ohlcv(exchange, symbol, ...)
    # Zamień na: get_ohlcv(symbol, exchange, ...)
    
    # Regex: exchange_api.get_ohlcv(EXCHANGE, SYMBOL, ...)
    pattern = r'exchange_api\.get_ohlcv\(([^,]+),\s*([^,]+),\s*([^)]+)\)'
    
    def swap_params(match):
        exchange = match.group(1).strip()
        symbol = match.group(2).strip()
        rest = match.group(3).strip()
        # Zamień miejscami
        return f'exchange_api.get_ohlcv({symbol}, {exchange}, {rest})'
    
    new_content = re.sub(pattern, swap_params, content)
    
    # To samo dla get_ticker
    pattern2 = r'exchange_api\.get_ticker\(([^,]+),\s*([^)]+)\)'
    
    def swap_ticker(match):
        exchange = match.group(1).strip()
        symbol = match.group(2).strip()
        return f'exchange_api.get_ticker({symbol}, {exchange})'
    
    new_content = re.sub(pattern2, swap_ticker, new_content)
    
    # Zapisz
    if new_content != content:
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f"✅ Poprawiono wywołania")
    else:
        print(f"⚠️ Brak zmian")

print("\n✅ GOTOWE!")

