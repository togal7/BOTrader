import ccxt

ex = ccxt.mexc()

symbols_to_test = ['VET/USDT:USDT', 'BTC/USDT:USDT']

for symbol in symbols_to_test:
    try:
        print(f"\nTest: {symbol}")
        ticker = ex.fetch_ticker(symbol)
        print(f"✅ SUCCESS: ${ticker['last']}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

