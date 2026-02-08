#!/usr/bin/env python3
"""
Signal Checker - Weryfikuje accuracy sygnałów z ai_signals_history.json
"""
import asyncio
import json
from datetime import datetime
from exchange_api import exchange_api
from config import logger

class SignalChecker:
    def __init__(self):
        self.check_interval = 3600  # Co godzinę
        self.history_file = 'ai_signals_history.json'
    
    def _load_history(self):
        """Wczytaj historię sygnałów"""
        try:
            with open(self.history_file) as f:
                return json.load(f)
        except:
            return {}
    
    def _save_history(self, history):
        """Zapisz historię"""
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    async def check_signals(self):
        """Sprawdź sygnały które powinny się już sprawdzić"""
        history = self._load_history()
        now = datetime.now()
        checked = 0
        
        for sig_id, sig in history.items():
            # Skip jeśli już sprawdzony
            if sig.get('checked_24h'):
                continue
            
            # Oblicz ile czasu minęło
            timestamp = datetime.fromisoformat(sig['timestamp'])
            age_hours = (now - timestamp).total_seconds() / 3600
            
            # Sprawdź po 24h
            if age_hours >= 24:
                await self._verify_signal(sig_id, sig, history)
                checked += 1
        
        if checked > 0:
            self._save_history(history)
            logger.info(f"✅ Sprawdzono {checked} sygnałów")
    
    async def _verify_signal(self, sig_id, sig, history, period="24h"):
        """Sprawdź czy TP został osiągnięty"""
        try:
            symbol = sig['symbol']
            exchange_name = sig['exchange']
            
            # Pobierz dane cenowe z ostatnich 24h
            ohlcv = await exchange_api.get_ohlcv(exchange_name, symbol, '1h', limit=24)
            if not ohlcv:
                return
            
            entry_price = sig['entry_price']
            signal_type = sig['signal']
            
            # Sprawdź high/low w ostatnich 24h
            highs = [candle[2] for candle in ohlcv]
            lows = [candle[3] for candle in ohlcv]
            
            highest = max(highs)
            lowest = min(lows)
            
            # Oblicz czy TP1 osiągnięty (załóżmy TP1 = +3% dla LONG, -3% dla SHORT)
            tp1 = entry_price * 1.03 if signal_type == 'LONG' else entry_price * 0.97
            
            hit = False
            if signal_type == 'LONG' and highest >= tp1:
                hit = True
            elif signal_type == 'SHORT' and lowest <= tp1:
                hit = True
            
            # Zapisz wynik
            sig[f'checked_{period}'] = True
            sig['verified'] = True
            sig['correct'] = hit
            sig['check_timestamp'] = datetime.now().isoformat()
            sig['highest_24h'] = highest
            sig['lowest_24h'] = lowest
            
            logger.info(f"{'✅' if hit else '❌'} {symbol} {signal_type} - {'HIT' if hit else 'MISS'}")
            
        except Exception as e:
            logger.error(f"Verify error {sig_id}: {e}")
    
    async def run(self):
        """Main loop"""
        logger.info("🔍 SignalChecker started")
        
        
        history = self._load_history()  # Pierwsze sprawdzenie
        logger.info(f"✅ Sprawdzono {len(history)} sygnałów")
        
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
