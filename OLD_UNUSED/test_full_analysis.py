import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from central_ai_analyzer import central_analyzer

async def test():
    symbol = 'ADA/USDT:USDT'
    exchange = 'mexc'
    timeframe = '30m'
    
    print(f"Testing: {symbol} on {exchange} ({timeframe})")
    
    try:
        result = await central_analyzer.analyze_pair_full(symbol, exchange, timeframe)
        
        if result:
            print(f"✅ SUCCESS!")
            print(f"Signal: {result['signal']['direction']}")
            print(f"Confidence: {result['signal']['confidence']}%")
        else:
            print(f"❌ Returned None")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
