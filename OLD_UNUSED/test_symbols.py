import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import exchange_api

async def test():
    symbols = await exchange_api.get_symbols('mexc')
    print(f"Total: {len(symbols)}")
    print(f"First 5: {list(symbols)[:5]}")
    
    # Sprawdź format
    if symbols:
        first = list(symbols)[0]
        print(f"\nFormat: {first}")
        print(f"Has :USDT? {':USDT' in first}")

asyncio.run(test())
