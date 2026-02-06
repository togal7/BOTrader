import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import ExchangeAPI

async def test():
    api = ExchangeAPI()
    
    print(f"Exchanges dict: {api.exchanges.keys()}")
    print(f"MEXC exists: {'mexc' in api.exchanges}")
    
    if 'mexc' in api.exchanges:
        ex = api.exchanges['mexc']
        print(f"MEXC object: {ex}")
        
        # Test bezpośredni
        try:
            ohlcv = ex.fetch_ohlcv('BTC/USDT:USDT', '30m', limit=100)
            print(f"✅ Direct CCXT: {len(ohlcv)} candles")
        except Exception as e:
            print(f"❌ Direct CCXT error: {e}")
    
    # Test przez metodę
    symbol = 'BTC/USDT:USDT'
    print(f"\n=== Test get_ohlcv({symbol}, mexc, 30m) ===")
    
    try:
        data = await api.get_ohlcv(symbol, 'mexc', '30m', 100)
        print(f"Result: {data}")
        
        if data:
            print(f"✅ Got {len(data)} candles")
        else:
            print(f"❌ Returned None")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
