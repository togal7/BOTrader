import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import ExchangeAPI

async def test():
    api = ExchangeAPI()
    
    symbols = ['BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT']
    
    for symbol in symbols:
        print(f"\n=== Testing {symbol} ===")
        
        # Test get_ohlcv
        data = await api.get_ohlcv(symbol, 'mexc', '30m', 100)
        
        if data:
            print(f"✅ Got {len(data)} candles")
            print(f"First: {data[0]}")
        else:
            print(f"❌ No data returned!")
        
        # Test get_ticker
        ticker = await api.get_ticker(symbol, 'mexc')
        if ticker:
            print(f"✅ Ticker: ${ticker.get('last', 'N/A')}")
        else:
            print(f"❌ No ticker!")

asyncio.run(test())
