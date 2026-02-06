with open('handlers.py', 'r') as f:
    lines = f.readlines()

# Znajdź linię elif data.startswith('ai_sig_'):
in_ai_sig = False
start_line = 0

for i, line in enumerate(lines):
    if "elif data.startswith('ai_sig_'):" in line:
        in_ai_sig = True
        start_line = i
        print(f"Znaleziono ai_sig_ w linii {i+1}")
        break

if in_ai_sig:
    # Znajdź koniec (następny return)
    end_line = start_line
    for i in range(start_line, min(start_line + 20, len(lines))):
        if 'return' in lines[i] and i > start_line:
            end_line = i
            break
    
    # Nowy kod
    new_block = """    elif data.startswith('ai_sig_'):
        # ai_sig_SYMBOL_TIMEFRAME
        parts = data.replace('ai_sig_', '').split('_')
        base = parts[0]  # BNB
        timeframe = parts[1] if len(parts) > 1 else user.get('interval', '15m')
        exchange = user.get('selected_exchange', 'mexc').lower()
        
        # MEXC futures: BNB → BNB/USDT:USDT
        symbol = base + '/USDT:USDT'
        
        logger.info(f"ai_sig callback: {base} → {symbol}")
        
        await show_pair_analysis(query, user_id, user, symbol, exchange, timeframe, 'ai_signal')
        return
"""
    
    # Zastąp
    lines[start_line:end_line+1] = [new_block]
    
    with open('handlers.py', 'w') as f:
        f.writelines(lines)
    
    print(f"✅ Zastąpiono linie {start_line+1}-{end_line+1}")

