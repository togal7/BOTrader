#!/usr/bin/env python3
import asyncio
import logging
from datetime import datetime
import random
from central_ai_analyzer import central_analyzer
from signal_saver import save_analysis_result

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger('bot_learning')

TOP_PAIRS = [
    'BTC/USDT:USDT', 'ETH/USDT:USDT', 'BNB/USDT:USDT', 'SOL/USDT:USDT',
    'XRP/USDT:USDT', 'ADA/USDT:USDT', 'DOGE/USDT:USDT', 'MATIC/USDT:USDT',
    'DOT/USDT:USDT', 'AVAX/USDT:USDT', 'LINK/USDT:USDT', 'UNI/USDT:USDT',
    'LTC/USDT:USDT', 'ATOM/USDT:USDT', 'XLM/USDT:USDT', 'BCH/USDT:USDT',
    'NEAR/USDT:USDT', 'ALGO/USDT:USDT', 'VET/USDT:USDT', 'FIL/USDT:USDT',
    'TRX/USDT:USDT', 'APT/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT',
    'SUI/USDT:USDT', 'HBAR/USDT:USDT', 'STX/USDT:USDT', 'INJ/USDT:USDT',
    'RUNE/USDT:USDT', 'FTM/USDT:USDT',
    'ETC/USDT:USDT', 'AAVE/USDT:USDT', 'UNI/USDT:USDT', 'MKR/USDT:USDT',
    'SNX/USDT:USDT', 'CRV/USDT:USDT', 'COMP/USDT:USDT', 'SUSHI/USDT:USDT',
    'YFI/USDT:USDT', 'BAL/USDT:USDT', '1INCH/USDT:USDT', 'ENJ/USDT:USDT',
    'MANA/USDT:USDT', 'SAND/USDT:USDT', 'GALA/USDT:USDT', 'AXS/USDT:USDT',
    'IMX/USDT:USDT', 'APE/USDT:USDT'
]
TIMEFRAMES = ['5m', '15m', '30m', '1h', '4h']

class BotLearning:
    def __init__(self):
        self.count = 0
        self.saved = 0

    async def analyze(self, symbol, tf):
        try:
            result = await central_analyzer.analyze_pair_full(symbol, 'mexc', tf, 'bot_learning')
            if result and result.get('signal', {}).get('confidence', 0) >= 50:
                # POPRAWNE PARAMETRY!
                signal_id = save_analysis_result(result, symbol, 'mexc', tf, 'bot_learning')
                if signal_id:
                    self.saved += 1
                    if self.saved % 5 == 0:
                        logger.info(f"💾 Saved {self.saved} signals")
                
                self.count += 1
                if self.count % 10 == 0:
                    logger.info(f"📊 {self.count} analyses, {self.saved} saved")
                return True
        except Exception as e:
            logger.error(f"Error {symbol}: {e}")
        return False

    async def run_hourly(self):
        logger.info("🔄 Hourly cycle starting...")
        tasks = []
        for _ in range(42):
            symbol = random.choice(TOP_PAIRS)
            tf = random.choice(TIMEFRAMES)
            tasks.append(self.analyze(symbol, tf))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        ok = sum(1 for r in results if r is True)
        logger.info(f"✅ Cycle: {ok}/42 successful, {self.saved} total saved")

    async def run_forever(self):
        logger.info("🚀 BOT LEARNING FIXED!")
        while True:
            try:
                await self.run_hourly()
                await asyncio.sleep(3600)
            except Exception as e:
                logger.error(f"Loop error: {e}")
                await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(BotLearning().run_forever())
