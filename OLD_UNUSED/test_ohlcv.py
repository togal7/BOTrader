import ccxt
import asyncio

async def test():
    ex = ccxt.mexc({'enableRateLimit': True})
    
    symbols_to_test = ['BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT']
    
    for symbol in symbols_to_test:
        try:
            print(f"\n=== Testing {symbol} ===")
            
            # Test 1: fetch_ohlcv
            ohlcv = ex.fetch_ohlcv(symbol, '30m', limit=100)
            print(f"✅ OHLCV: {len(ohlcv)} candles")
            
            # Test 2: ticker
            ticker = ex.fetch_ticker(symbol)
            print(f"✅ Ticker: ${ticker['last']}")
            
        except Exception as e:
            print(f"❌ Error: {e}")

asyncio.run(test())
