import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import exchange_api

async def test():
    symbols = await exchange_api.get_symbols('mexc')
    
    search_term = 'BTC'
    matching = [s for s in symbols if search_term in s.upper()]
    
    print(f"Total symbols: {len(symbols)}")
    print(f"Search term: {search_term}")
    print(f"Matching: {len(matching)}")
    print(f"\nFirst 10 matches:")
    for s in matching[:10]:
        print(f"  {s}")

asyncio.run(test())
