import ccxt

ex = ccxt.mexc()
markets = ex.load_markets()

# Sprawdź NVIDIA i TESLA
test_symbols = ['NVIDIA/USDT:USDT', 'TESLA/USDT:USDT']

for symbol in test_symbols:
    if symbol in markets:
        market = markets[symbol]
        print(f"\n{symbol}:")
        print(f"  Type: {market.get('type')}")
        print(f"  Contract: {market.get('contract', 'N/A')}")
        print(f"  Linear: {market.get('linear', 'N/A')}")
        print(f"  Active: {market.get('active', 'N/A')}")
        print(f"  ✅ EXISTS on MEXC Futures!")
    else:
        print(f"\n{symbol}: ❌ NOT FOUND")

# Test czy można pobrać ticker
print("\n=== TESTING TICKER ===")
for symbol in test_symbols:
    try:
        ticker = ex.fetch_ticker(symbol)
        print(f"{symbol}: ${ticker['last']} ✅")
    except Exception as e:
        print(f"{symbol}: ❌ {e}")

