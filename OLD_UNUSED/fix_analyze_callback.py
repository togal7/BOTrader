with open('handlers.py', 'r') as f:
    content = f.read()

import re
pattern = r"elif data\.startswith\('analyze_'\):.*?return"
match = re.search(pattern, content, re.DOTALL)

if match:
    old_block = match.group(0)
    
    new_block = """elif data.startswith('analyze_'):
        # analyze_SYMBOL_TIMEFRAME lub analyze_SYMBOL (default 15m)
        parts = data.replace('analyze_', '').split('_')
        symbol = parts[0]  # np. "BTC"
        timeframe = parts[1] if len(parts) > 1 else user.get('interval', '15m')
        exchange = user.get('selected_exchange', 'mexc').lower()
        
        # Konwertuj: BTC → BTC/USDT:USDT
        if '/USDT:USDT' not in symbol:
            symbol = symbol + '/USDT:USDT'
        
        logger.info(f"analyze callback: {parts[0]} → {symbol}")
        
        await show_pair_analysis(query, user_id, user, symbol, exchange, timeframe, 'manual')
        return"""
    
    content = content.replace(old_block, new_block)
    
    with open('handlers.py', 'w') as f:
        f.write(content)
    
    print("✅ Naprawiono analyze callback!")

