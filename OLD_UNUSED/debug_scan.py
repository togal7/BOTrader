import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from ai_signals_advanced import AdvancedAISignals

async def test():
    ai = AdvancedAISignals()
    
    # Symuluj scan
    from exchange_api import ExchangeAPI
    ex_api = ExchangeAPI()
    
    symbols = await ex_api.get_symbols('mexc')
    print(f"✅ Total symbols: {len(symbols)}")
    print(f"First 10: {symbols[:10]}")
    
    # Blacklist
    print(f"\n❌ Blacklist: {ai.BLACKLIST}")
    
    # Filtruj blacklist
    filtered = [s for s in symbols if not any(bl in s for bl in ai.BLACKLIST)]
    print(f"✅ After blacklist: {len(filtered)}")
    
    # TOP cryptos
    print(f"\n🔝 TOP_CRYPTOS (first 10): {ai.TOP_CRYPTOS[:10]}")
    
    # Konwersja
    top_with_suffix = [s.replace('/USDT', '/USDT:USDT') for s in ai.TOP_CRYPTOS[:10]]
    print(f"With suffix: {top_with_suffix}")
    
    # Które są dostępne?
    available = [s for s in top_with_suffix if s in filtered]
    print(f"\n✅ Available tops: {available}")
    
    if not available:
        print("\n❌ PROBLEM: Żaden TOP crypto nie jest dostępny!")
        print("Sprawdzam dokładnie...")
        print(f"BTC/USDT:USDT in symbols? {'BTC/USDT:USDT' in symbols}")
        print(f"ETH/USDT:USDT in symbols? {'ETH/USDT:USDT' in symbols}")

asyncio.run(test())
