import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import exchange_api

async def test():
    # Test ticker
    print("=== TESTING MANYU/USDT:USDT ===\n")
    
    try:
        ticker = await exchange_api.get_ticker('MANYU/USDT:USDT', 'mexc')
        print(f"Ticker: {ticker}")
        print(f"Has 'last'? {'last' in ticker}")
        print(f"Has 'price'? {'price' in ticker}")
        
        # Test OHLCV
        ohlcv = await exchange_api.get_ohlcv('MANYU/USDT:USDT', 'mexc', '1w')
        print(f"\nOHLCV (1w): {len(ohlcv)} candles")
        if ohlcv:
            print(f"Last candle: {ohlcv[-1]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

asyncio.run(test())
