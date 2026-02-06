import sys
sys.path.insert(0, '/bots/BOTrader')

# Pokaż jak scan wywołuje get_ohlcv
with open('ai_signals_advanced.py', 'r') as f:
    content = f.read()
    
import re
# Znajdź scan_with_filters i pokaż wywołania
match = re.search(r'async def scan_with_filters.*?(?=\n    async def|\nclass |\Z)', content, re.DOTALL)

if match:
    scan_code = match.group(0)
    
    # Znajdź wywołania get_ohlcv
    ohlcv_calls = re.findall(r'.*get_ohlcv.*', scan_code)
    
    print("=== scan_with_filters wywołania get_ohlcv ===")
    for call in ohlcv_calls:
        print(call.strip())

