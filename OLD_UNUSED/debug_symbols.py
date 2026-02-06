import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from exchange_api import exchange_api

async def test():
    symbols = await exchange_api.get_symbols('mexc')
    
    print(f"Total: {len(symbols)}")
    print("\n=== PIERWSZE 30 SYMBOLI ===")
    
    # Grupuj po formatach
    formats = {}
    for s in symbols[:50]:
        if '/USDT:USDT' in s:
            fmt = 'LINEAR_PERP'
        elif ':USDT' in s:
            fmt = 'COLON_USDT'
        elif '/USDT' in s:
            fmt = 'SLASH_USDT'
        else:
            fmt = 'OTHER'
        
        if fmt not in formats:
            formats[fmt] = []
        formats[fmt].append(s)
    
    for fmt, syms in formats.items():
        print(f"\n{fmt} ({len(syms)} par):")
        for s in syms[:10]:
            print(f"  {s}")

asyncio.run(test())
