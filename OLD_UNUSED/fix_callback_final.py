with open('handlers.py', 'r') as f:
    content = f.read()

# Znajdź ai_sig callback i popraw konwersję
old_callback = """        logger.info(f"ai_sig callback: {parts[0]} → {symbol}")"""

# Znajdź pełny blok ai_sig
import re
pattern = r"elif data\.startswith\('ai_sig_'\):.*?return"
match = re.search(pattern, content, re.DOTALL)

if match:
    old_block = match.group(0)
    
    new_block = """elif data.startswith('ai_sig_'):
        # ai_sig_SYMBOL_TIMEFRAME - z kontekstem AI signals
        parts = data.replace('ai_sig_', '').split('_')
        symbol = parts[0]  # np. "ATOM"
        timeframe = parts[1] if len(parts) > 1 else user.get('interval', '15m')
        exchange = user.get('selected_exchange', 'mexc').lower()
        
        # Konwertuj WŁAŚCIWIE: ATOM → ATOM/USDT:USDT (nie ATOM:USDT!)
        if '/USDT:USDT' not in symbol:
            symbol = symbol + '/USDT:USDT'
        
        logger.info(f"ai_sig callback: {parts[0]} → {symbol}")
        
        await show_pair_analysis(query, user_id, user, symbol, exchange, timeframe, 'ai_signal')
        return"""
    
    content = content.replace(old_block, new_block)
    
    with open('handlers.py', 'w') as f:
        f.write(content)
    
    print("✅ Naprawiono ai_sig callback!")
else:
    print("❌ Nie znaleziono ai_sig")

