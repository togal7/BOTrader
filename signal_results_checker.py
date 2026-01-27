"""
Signal Results Checker - Sprawdza wyniki sygnałów po czasie
Uruchamiany jako background task co godzinę
"""

import asyncio
import logging
from ai_signals_tracker import tracker
import ccxt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def check_signals():
    """Check signal outcomes"""
    
    # Sprawdź sygnały po 24h
    signals_24h = tracker.get_signals_to_check(24)
    logger.info(f"📊 Checking {len(signals_24h)} signals after 24h")
    
    for signal in signals_24h:
        try:
            symbol = signal['symbol']
            exchange_name = signal['exchange']
            signal_id = signal['signal_id']
            
            # Pobierz aktualną cenę
            # Create exchange instance
            if exchange_name.lower() == 'mexc':
                exchange = ccxt.mexc()
            elif exchange_name.lower() == 'binance':
                exchange = ccxt.binance()
            elif exchange_name.lower() == 'bybit':
                exchange = ccxt.bybit()
            else:
                exchange = ccxt.mexc()  # default
            ticker = exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            
            # Sprawdź wynik
            tracker.check_signal_outcome(signal_id, current_price, 24)
            
        except Exception as e:
            logger.error(f"Error checking {signal_id}: {e}")
        
        await asyncio.sleep(1)  # Rate limiting
    
    # Sprawdź sygnały po 48h
    signals_48h = tracker.get_signals_to_check(48)
    logger.info(f"📊 Checking {len(signals_48h)} signals after 48h")
    
    for signal in signals_48h:
        try:
            symbol = signal['symbol']
            exchange_name = signal['exchange']
            signal_id = signal['signal_id']
            
            # Create exchange instance
            if exchange_name.lower() == 'mexc':
                exchange = ccxt.mexc()
            elif exchange_name.lower() == 'binance':
                exchange = ccxt.binance()
            elif exchange_name.lower() == 'bybit':
                exchange = ccxt.bybit()
            else:
                exchange = ccxt.mexc()  # default
            ticker = exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            
            tracker.check_signal_outcome(signal_id, current_price, 48)
            
        except Exception as e:
            logger.error(f"Error checking {signal_id}: {e}")
        
        await asyncio.sleep(1)
    
    # Sprawdź sygnały po 7 dniach
    signals_7d = tracker.get_signals_to_check(168)
    logger.info(f"📊 Checking {len(signals_7d)} signals after 7 days")
    
    for signal in signals_7d:
        try:
            symbol = signal['symbol']
            exchange_name = signal['exchange']
            signal_id = signal['signal_id']
            
            # Create exchange instance
            if exchange_name.lower() == 'mexc':
                exchange = ccxt.mexc()
            elif exchange_name.lower() == 'binance':
                exchange = ccxt.binance()
            elif exchange_name.lower() == 'bybit':
                exchange = ccxt.bybit()
            else:
                exchange = ccxt.mexc()  # default
            ticker = exchange.fetch_ticker(symbol)
            current_price = ticker['last']
            
            tracker.check_signal_outcome(signal_id, current_price, 168)
            
        except Exception as e:
            logger.error(f"Error checking {signal_id}: {e}")
        
        await asyncio.sleep(1)
    
    # Pokaż statystyki
    stats_24h = tracker.get_accuracy_stats('24h')
    stats_48h = tracker.get_accuracy_stats('48h')
    stats_7d = tracker.get_accuracy_stats('7d')
    
    logger.info(f"""
📊 ACCURACY STATS:
24h: {stats_24h.get('accuracy_pct', 0)}% ({stats_24h.get('correct_signals', 0)}/{stats_24h.get('total_signals', 0)})
48h: {stats_48h.get('accuracy_pct', 0)}% ({stats_48h.get('correct_signals', 0)}/{stats_48h.get('total_signals', 0)})
7d:  {stats_7d.get('accuracy_pct', 0)}% ({stats_7d.get('correct_signals', 0)}/{stats_7d.get('total_signals', 0)})
""")

async def main():
    """Main loop - check every hour"""
    while True:
        try:
            logger.info("🔄 Starting signal results check...")
            await check_signals()
            logger.info("✅ Check complete. Sleeping 1 hour...")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        
        await asyncio.sleep(3600)  # 1 hour

if __name__ == '__main__':
    asyncio.run(main())

