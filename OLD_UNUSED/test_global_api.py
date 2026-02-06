import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio

# Import jak w ai_signals_advanced
from exchange_api import exchange_api

async def test():
    print(f"exchange_api object: {exchange_api}")
    print(f"Has get_ohlcv: {hasattr(exchange_api, 'get_ohlcv')}")
    print(f"exchanges: {exchange_api.exchanges.keys()}")
    
    # Test wywołania
    result = await exchange_api.get_ohlcv('BTC/USDT:USDT', 'mexc', '30m', 100)
    print(f"Result: {len(result) if result else None}")

asyncio.run(test())
