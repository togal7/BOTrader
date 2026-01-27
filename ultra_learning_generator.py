"""
Ultra Learning Generator - MAKSYMALNA prędkość uczenia
500 analiz dziennie = 15,000/miesiąc = NAJSZYBSZY learning możliwy
"""

import asyncio
import random
import logging
from datetime import datetime
from signal_saver import save_analysis_result
from ai_signals_tracker import tracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def ultra_learning():
    """500 analiz z rate limiting aby nie przeciążyć systemu"""
    
    try:
        from analyzer_wrapper import analyzer_with_learning
        
        # WSZYSTKIE popularne pary (30 par)
        symbols = [
            'BTC/USDT:USDT', 'ETH/USDT:USDT', 'SOL/USDT:USDT', 
            'BNB/USDT:USDT', 'XRP/USDT:USDT', 'ADA/USDT:USDT',
            'DOGE/USDT:USDT', 'LTC/USDT:USDT', 'MATIC/USDT:USDT',
            'DOT/USDT:USDT', 'AVAX/USDT:USDT', 'LINK/USDT:USDT',
            'UNI/USDT:USDT', 'ATOM/USDT:USDT', 'FIL/USDT:USDT',
            'ETC/USDT:USDT', 'APT/USDT:USDT', 'ARB/USDT:USDT',
            'OP/USDT:USDT', 'NEAR/USDT:USDT', 'FTM/USDT:USDT',
            'ALGO/USDT:USDT', 'VET/USDT:USDT', 'ICP/USDT:USDT',
            'AAVE/USDT:USDT', 'CRV/USDT:USDT', 'LDO/USDT:USDT',
            'MKR/USDT:USDT', 'SNX/USDT:USDT', 'SAND/USDT:USDT'
        ]
        
        # Wszystkie timeframes
        timeframes = ['1m', '5m', '15m', '30m', '1h', '4h', '8h', '1d', '1w', '1M']
        
        logger.info(f"🔥 ULTRA LEARNING MODE ACTIVATED!")
        logger.info(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        logger.info(f"🎯 Target: 500 analiz (30 par × 10 timeframes)")
        logger.info(f"⏱️  Estimated time: ~3-5 min (z rate limiting)")
        
        success = 0
        failed = 0
        
        # Batch po 50 z przerwami
        for batch in range(10):  # 10 batchy × 50 = 500
            logger.info(f"\n📦 BATCH {batch+1}/10 (50 analiz)...")
            
            for i in range(50):
                symbol = random.choice(symbols)
                timeframe = random.choice(timeframes)
                
                try:
                    result = await analyzer_with_learning.analyze_pair_full(
                        symbol=symbol,
                        exchange='mexc',
                        timeframe=timeframe,
                        context='general'
                    )
                    
                    if result:
                        success += 1
                    else:
                        failed += 1
                    
                    # Minimal delay (0.15s = 400 analiz/min max)
                    await asyncio.sleep(0.15)
                    
                except Exception as e:
                    failed += 1
            
            # Przerwa między batches (odciążenie)
            logger.info(f"   ✅ Batch {batch+1} done: {success} sukces")
            await asyncio.sleep(2)  # 2s przerwa
        
        logger.info(f"\n{'='*60}")
        logger.info(f"🎉 ULTRA LEARNING ZAKOŃCZONY!")
        logger.info(f"   ✅ Sukces: {success}/500")
        logger.info(f"   ❌ Błędy: {failed}/500")
        logger.info(f"   📈 Success rate: {success/500*100:.1f}%")
        logger.info(f"{'='*60}")
        
        # Stats
        import json, os
        if os.path.exists('ai_signals_history.json'):
            with open('ai_signals_history.json', 'r') as f:
                data = json.load(f)
            real = {k: v for k, v in data.items() if 'TEST' not in k}
            logger.info(f"📊 BAZA SYGNAŁÓW: {len(real)} total")
            logger.info(f"🚀 Wzrost dziś: +{success}")
        
        return success
        
    except Exception as e:
        logger.error(f"CRITICAL: {e}")
        import traceback
        traceback.print_exc()
        return 0

if __name__ == '__main__':
    asyncio.run(ultra_learning())

