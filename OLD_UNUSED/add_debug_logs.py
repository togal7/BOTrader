with open('exchange_api.py', 'r') as f:
    content = f.read()

# Znajdź get_ohlcv i dodaj więcej logów
old_ohlcv = """    async def get_ohlcv(self, symbol: str, exchange: str, timeframe: str = '15m', limit: int = 100):
        \"\"\"Get OHLCV data (symbol first for consistency)\"\"\"
        try:
            ex = self.exchanges.get(exchange)
            if not ex:
                return None
            
            ohlcv = ex.fetch_ohlcv(symbol, timeframe, limit=limit)
            return ohlcv
        
        except Exception as e:
            logger.error(f"Get OHLCV error for {symbol}: {e}")
            return None"""

new_ohlcv = """    async def get_ohlcv(self, symbol: str, exchange: str, timeframe: str = '15m', limit: int = 100):
        \"\"\"Get OHLCV data (symbol first for consistency)\"\"\"
        try:
            logger.debug(f"get_ohlcv called: symbol={symbol}, exchange={exchange}, tf={timeframe}")
            
            ex = self.exchanges.get(exchange)
            if not ex:
                logger.error(f"Exchange {exchange} not found in self.exchanges")
                return None
            
            logger.debug(f"Calling fetch_ohlcv on {exchange}")
            ohlcv = ex.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            logger.debug(f"Got {len(ohlcv) if ohlcv else 0} candles")
            return ohlcv
        
        except Exception as e:
            logger.error(f"Get OHLCV error for {symbol}: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return None"""

content = content.replace(old_ohlcv, new_ohlcv)

with open('exchange_api.py', 'w') as f:
    f.write(content)

print("✅ Dodano debug logi")

