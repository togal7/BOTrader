with open('handlers.py', 'r') as f:
    content = f.read()

# Zamień get_ohlcv(exchange, symbol, interval) → get_ohlcv(symbol, exchange, interval)
old_call = "data = await exchange_api.get_ohlcv(exchange, symbol, interval)"
new_call = "data = await exchange_api.get_ohlcv(symbol, exchange, interval)"

if old_call in content:
    content = content.replace(old_call, new_call)
    print("✅ Naprawiono get_ohlcv - zamieniono kolejność parametrów")
else:
    print("❌ Nie znaleziono old_call")

with open('handlers.py', 'w') as f:
    f.write(content)

