import ccxt

ex = ccxt.mexc()

print("MEXC supported timeframes:")
if hasattr(ex, 'timeframes'):
    for tf in ex.timeframes:
        print(f"  {tf}")
else:
    print("  No timeframes attribute")

# Test konkretnie 1w
print("\nTesting specific intervals:")
test_tfs = ['1w', '2w', '1M', '3M', '6M', '1Y', '3d', '5d']

for tf in test_tfs:
    try:
        # Próba pobrania
        data = ex.fetch_ohlcv('BTC/USDT:USDT', timeframe=tf, limit=5)
        print(f"  {tf}: ✅ Works ({len(data)} candles)")
    except Exception as e:
        print(f"  {tf}: ❌ {str(e)[:50]}")

