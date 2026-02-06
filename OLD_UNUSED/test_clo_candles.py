import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import exchange_api

async def test():
    ohlcv = await exchange_api.get_ohlcv('CLO/USDT:USDT', 'mexc', '1w')
    print(f"CLO/USDT 1w: {len(ohlcv)} candles")
    
    if len(ohlcv) < 50:
        print("⚠️ Za mało świec dla pełnej analizy (potrzeba min 50)")

asyncio.run(test())
