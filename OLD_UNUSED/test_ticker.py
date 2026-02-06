import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import exchange_api

async def test():
    symbol = 'VET/USDT:USDT'
    
    print(f"Test 1: get_ohlcv({symbol})")
    ohlcv = await exchange_api.get_ohlcv(symbol, 'mexc', '30m', 100)
    print(f"  Result: {len(ohlcv) if ohlcv else None} candles")
    
    print(f"\nTest 2: get_ticker({symbol})")
    ticker = await exchange_api.get_ticker(symbol, 'mexc')
    print(f"  Result: {ticker}")
    
    if ticker:
        print(f"  Keys: {ticker.keys()}")
        print(f"  Last: ${ticker.get('last', 'N/A')}")
    else:
        print(f"  ❌ TICKER IS NONE!")

asyncio.run(test())
