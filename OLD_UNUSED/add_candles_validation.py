with open('ai_trader.py', 'r') as f:
    lines = f.readlines()

# Znajdź gdzie pobiera OHLCV i dodaj sprawdzenie
for i, line in enumerate(lines):
    if 'ohlcv = await' in line or 'data = await exchange_api.get_ohlcv' in line:
        # Dodaj sprawdzenie PO tej linii
        if i+1 < len(lines) and 'if not ohlcv or len(ohlcv)' not in lines[i+1]:
            indent = len(line) - len(line.lstrip())
            check = ' ' * indent + 'if not ohlcv or len(ohlcv) < 50:\n'
            check += ' ' * indent + '    raise ValueError("Insufficient candles for analysis")\n'
            lines.insert(i+1, check)
            print(f"✅ Added validation at line {i+2}")
            break

with open('ai_trader.py', 'w') as f:
    f.writelines(lines)

