#!/usr/bin/env python3
import ccxt
from config import logger, EXCHANGES

class ExchangeAPI:
    def __init__(self):
        self.exchanges = {}
        for ex_id in EXCHANGES.keys():
            if ex_id == 'mexc':
                self.exchanges[ex_id] = ccxt.mexc({'enableRateLimit': True, 'options': {'defaultType': 'swap'}})
            elif ex_id == 'bybit':
                self.exchanges[ex_id] = ccxt.bybit()
            elif ex_id == 'binance':
                self.exchanges[ex_id] = ccxt.binance()
    
    async def get_symbols(self, exchange: str):
        """Get all FUTURES symbols from exchange"""
        try:
            ex = self.exchanges.get(exchange)
            if not ex:
                logger.error(f"Exchange {exchange} not found")
                return []
            
            # Load markets synchronously
            markets = ex.load_markets()
            
            # Filter ONLY FUTURES USDT pairs
            # MEXC: futures mają ':USDT' (colon)
            # Bybit/Binance: sprawdzamy market['type'] == 'swap' lub 'future'
            symbols = []
            for symbol, market in markets.items():
                # Skip if not USDT pair
                if 'USDT' not in symbol:
                    continue
                
                # MEXC futures: LINEAR (perpetual)
                if exchange == 'mexc':
                    # MEXC linear futures to perpetualne kontrakty
                    if market.get('linear') and market.get('type') in ['swap', 'future']:
                        if not market.get('active', True):
                            continue
                        symbols.append(symbol)
                # Bybit/Binance
                else:
                    if market.get('type') in ['swap', 'future'] and '/USDT' in symbol:
                        if not market.get('active', True):
                            continue
                        symbols.append(symbol)
            
            logger.info(f"Found {len(symbols)} FUTURES symbols on {exchange}")
            
            return symbols[:500]  # Return max 500
            
        except Exception as e:
            logger.error(f"Get symbols error: {e}")
            return []
    
    async def get_ohlcv(self, symbol: str, exchange: str, timeframe: str = "15m", limit: int = 100):
        """Get OHLCV data"""
        try:
            ex = self.exchanges.get(exchange)
            if not ex:
                return None
            
            ohlcv = ex.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
            
        except Exception as e:
            logger.error(f"Get OHLCV error for {symbol}: {e}")
            return None
    
    async def get_ticker(self, symbol: str, exchange: str):
        """Get ticker data (symbol first for consistency)"""
        try:
            ex = self.exchanges.get(exchange)
            if not ex:
                return None
            
            ticker = ex.fetch_ticker(symbol)
            return ticker
            
        except Exception as e:
            logger.error(f"Get ticker error for {symbol}: {e}")
            return None

exchange_api = ExchangeAPI()
logger.info("✅ Exchange API initialized")
