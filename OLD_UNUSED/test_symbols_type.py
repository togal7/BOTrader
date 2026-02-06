import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import exchange_api

async def test():
    symbols = await exchange_api.get_symbols('mexc')
    
    print(f"Total symbols: {len(symbols)}")
    
    # Sprawdź pierwsze 10
    sample = list(symbols)[:10]
    print(f"\nFirst 10:")
    for s in sample:
        print(f"  {s} - {'FUTURES' if ':USDT' in s else 'SPOT'}")
    
    # Zlicz futures vs spot
    futures = [s for s in symbols if ':USDT' in s]
    spot = [s for s in symbols if ':USDT' not in s]
    
    print(f"\nFutures: {len(futures)}")
    print(f"Spot: {len(spot)}")
    
    # Sprawdź TESLA
    has_tesla_spot = 'TESLA/USDT' in symbols
    has_tesla_futures = 'TESLA/USDT:USDT' in symbols
    
    print(f"\nTESLA/USDT (spot): {has_tesla_spot}")
    print(f"TESLA/USDT:USDT (futures): {has_tesla_futures}")

asyncio.run(test())
