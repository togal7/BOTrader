import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import exchange_api

async def test():
    symbols = await exchange_api.get_symbols('mexc')
    
    print(f"Active symbols: {len(symbols)}")
    
    # Sprawdź czy stocks zniknęły
    has_tesla = any('TESLA' in s for s in symbols)
    has_nvidia = any('NVIDIA' in s for s in symbols)
    has_mstr = any('MSTR' in s for s in symbols)
    
    print(f"\nTESLA: {'❌ STILL THERE' if has_tesla else '✅ FILTERED OUT'}")
    print(f"NVIDIA: {'❌ STILL THERE' if has_nvidia else '✅ FILTERED OUT'}")
    print(f"MSTRSTOCK: {'❌ STILL THERE' if has_mstr else '✅ FILTERED OUT'}")

asyncio.run(test())
