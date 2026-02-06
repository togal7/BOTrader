import sys
sys.path.insert(0, '/bots/BOTrader')

import asyncio
from central_ai_analyzer import central_analyzer

async def test():
    try:
        print("Start analysis...")
        result = await asyncio.wait_for(
            central_analyzer.analyze_pair_full('VET/USDT:USDT', 'mexc', '30m'),
            timeout=15.0
        )
        
        if result:
            print(f"✅ SUCCESS!")
        else:
            print(f"❌ Returned None")
            
    except asyncio.TimeoutError:
        print(f"❌ TIMEOUT after 15s - analysis HUNG!")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(test())
