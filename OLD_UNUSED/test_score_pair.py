import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from ai_signals_advanced import AdvancedAISignals
from exchange_api import exchange_api

async def test():
    ai = AdvancedAISignals()
    
    # Pobierz dane dla BTC
    symbol = 'BTC/USDT:USDT'
    data = await exchange_api.get_ohlcv(symbol, 'mexc', '30m', 100)
    
    print(f"✅ Got {len(data)} candles for {symbol}")
    
    # Test score_pair
    try:
        result = ai.score_pair(symbol, data, '30m')
        
        if result:
            print(f"\n✅ SCORE_PAIR RESULT:")
            print(f"  Symbol: {result['symbol']}")
            print(f"  Signal: {result['signal']}")
            print(f"  Score: {result['score']}")
            print(f"  Confidence: {result.get('confidence', 'N/A')}")
        else:
            print(f"\n❌ score_pair returned None/False")
            
    except Exception as e:
        print(f"\n❌ score_pair ERROR: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
