import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import exchange_api

async def test():
    symbols = await exchange_api.get_symbols('mexc')
    
    # Szukaj NVIDIA i TESLA
    nvidia_variants = [s for s in symbols if 'NVDA' in s or 'NVIDIA' in s]
    tesla_variants = [s for s in symbols if 'TESLA' in s]
    
    print("NVIDIA variants:")
    for s in nvidia_variants:
        print(f"  {s}")
    
    print("\nTESLA variants:")
    for s in tesla_variants:
        print(f"  {s}")
    
    # Sprawdź czy to faktycznie futures
    print("\nFormat check:")
    for s in nvidia_variants + tesla_variants:
        has_colon = ':USDT' in s
        print(f"  {s} - {'FUTURES (:USDT)' if has_colon else 'SPOT?'}")

asyncio.run(test())
