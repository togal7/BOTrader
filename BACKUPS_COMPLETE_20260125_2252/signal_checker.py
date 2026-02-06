#!/usr/bin/env python3
"""
Signal Checker - Weryfikuje accuracy sygnałów
"""
import asyncio
import time
from datetime import datetime, timedelta
from ai_signals_tracker import tracker
from exchange_api import exchange_api
from config import logger

class SignalChecker:
    def __init__(self):
        self.check_interval = 3600  # Co godzinę
    
    async def check_signals(self):
        """Sprawdź sygnały które powinny się już sprawdzić"""
        now = datetime.now()
        checked = 0
        
        for sig_id, sig in tracker.signals_db.items():
            # Skip jeśli już sprawdzony
            if sig.get('checked'):
                continue
            
            # Oblicz ile czasu minęło
            timestamp = datetime.fromisoformat(sig['timestamp'])
            age_minutes = (now - timestamp).total_seconds() / 60
            
            # Czy czas sprawdzić?
            tf = sig.get('timeframe', '1h')
            tf_minutes = self._tf_to_minutes(tf)
            
            if age_minutes >= tf_minutes:
                await self._verify_signal(sig_id, sig)
                checked += 1
        
        if checked > 0:
            logger.info(f"✅ Sprawdzono {checked} sygnałów")
    
    def _tf_to_minutes(self, tf):
        """Konwertuj TF na minuty"""
        mapping = {
            '1m': 1, '3m': 3, '5m': 5, '15m': 15, '30m': 30,
            '1h': 60, '2h': 120, '4h': 240, '8h': 480,
            '12h': 720, '1d': 1440, '3d': 4320, '1w': 10080
        }
        return mapping.get(tf, 60)
    
    async def _verify_signal(self, sig_id, sig):
        """Sprawdź czy TP został osiągnięty"""
        try:
            symbol = sig['symbol']
            exchange = sig['exchange']
            
            # Pobierz aktualną cenę
            ohlcv = await exchange_api.get_ohlcv(exchange, symbol, '1m', limit=1)
            if not ohlcv:
                return
            
            current_price = ohlcv[-1][4]  # Close
            entry_price = sig['price']
            
            indicators = sig.get('indicators', {})
            tp1 = indicators.get('tp1')
            
            if not tp1:
                return
            
            signal_type = sig['signal']
            
            # Sprawdź czy TP osiągnięty
            hit = False
            if signal_type == 'LONG' and current_price >= tp1:
                hit = True
            elif signal_type == 'SHORT' and current_price <= tp1:
                hit = True
            
            # Zapisz wynik
            sig['checked'] = True
            sig['check_timestamp'] = datetime.now().isoformat()
            sig['check_price'] = current_price
            sig['tp_hit'] = hit
            sig['pnl_pct'] = ((current_price - entry_price) / entry_price * 100) if signal_type == 'LONG' else ((entry_price - current_price) / entry_price * 100)
            
            tracker._save_db()
            
            logger.info(f"{'✅' if hit else '❌'} {symbol} {signal_type} - {'HIT' if hit else 'MISS'} ({sig['pnl_pct']:.2f}%)")
            
        except Exception as e:
            logger.error(f"Verify error {sig_id}: {e}")
    
    async def run(self):
        """Main loop"""
        logger.info("🔍 SignalChecker started")
        
        while True:
            try:
                await self.check_signals()
                await asyncio.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"SignalChecker error: {e}")
                await asyncio.sleep(60)

if __name__ == '__main__':
    checker = SignalChecker()
    asyncio.run(checker.run())

