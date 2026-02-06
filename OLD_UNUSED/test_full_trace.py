import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
import logging
logging.basicConfig(level=logging.DEBUG)

from central_ai_analyzer import central_analyzer

async def test():
    try:
        print("Wywołuję analyze_pair_full...")
        result = await central_analyzer.analyze_pair_full('VET/USDT:USDT', 'mexc', '30m')
        
        if result:
            print(f"✅ SUCCESS!")
            print(f"Keys: {result.keys()}")
        else:
            print(f"❌ Returned None")
            
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
