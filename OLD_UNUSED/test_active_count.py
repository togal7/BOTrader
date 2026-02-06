import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import exchange_api

async def test():
    symbols = await exchange_api.get_symbols('mexc')
    
    print(f"Active FUTURES: {len(symbols)}")
    print(f"\nFirst 10:")
    for s in list(symbols)[:10]:
        print(f"  {s}")
    
    # Sprawdź czy NVIDIA i TESLA zniknęły
    has_nvidia = any('NVIDIA' in s for s in symbols)
    has_tesla = any('TESLA' in s for s in symbols)
    
    print(f"\nNVIDIA: {'❌ FILTERED OUT' if not has_nvidia else '⚠️ STILL THERE'}")
    print(f"TESLA: {'❌ FILTERED OUT' if not has_tesla else '⚠️ STILL THERE'}")

asyncio.run(test())
