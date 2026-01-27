import aiohttp
import asyncio
from typing import List, Dict, Optional
from config import logger, EXCHANGES

class ExchangeAPI:
    def __init__(self):
        self.session = None
        self.timeout = aiohttp.ClientTimeout(total=10)
    
    async def get_session(self):
        """Tworzy lub zwraca istniejącą sesję"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self.session
    
    async def close(self):
        """Zamyka sesję"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    # ============================================
    # MEXC FUTURES
    # ============================================
    
    async def get_mexc_symbols(self) -> List[str]:
        """Pobiera listę par MEXC Futures"""
        try:
            session = await self.get_session()
            url = f"{EXCHANGES['MEXC']['base_url']}/api/v1/contract/detail"
            
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('success') and data.get('data'):
                        symbols = [item['symbol'] for item in data['data'] if item.get('symbol')]
                        logger.info(f"MEXC: pobrano {len(symbols)} par")
                        return sorted(symbols)
        except Exception as e:
            logger.error(f"MEXC symbols error: {e}")
        
        return []
    
    async def get_mexc_ticker(self, symbol: str) -> Optional[Dict]:
        """Pobiera ticker dla symbolu MEXC"""
        try:
            session = await self.get_session()
            url = f"{EXCHANGES['MEXC']['base_url']}/api/v1/contract/ticker"
            
            async with session.get(url, params={'symbol': symbol}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('success') and data.get('data'):
                        ticker = data['data'][0] if isinstance(data['data'], list) else data['data']
                        return {
                            'symbol': symbol,
                            'last_price': float(ticker.get('lastPrice', 0)),
                            'change_24h': float(ticker.get('riseFallRate', 0)),
                            'volume_24h': float(ticker.get('volume24', 0)),
                            'high_24h': float(ticker.get('high24Price', 0)),
                            'low_24h': float(ticker.get('low24Price', 0))
                        }
        except Exception as e:
            logger.error(f"MEXC ticker error for {symbol}: {e}")
        
        return None
    
    async def get_mexc_klines(self, symbol: str, interval: str, limit: int = 100) -> List[Dict]:
        """Pobiera świece MEXC"""
        try:
            session = await self.get_session()
            # MEXC używa Min1, Min5, Min15, Min30, Hour1, Hour4, Day1, Week1, Month1
            interval_map = {
                '1m': 'Min1', '3m': 'Min3', '5m': 'Min5', '15m': 'Min15', '30m': 'Min30',
                '1h': 'Hour1', '2h': 'Hour2', '4h': 'Hour4', '6h': 'Hour6', '12h': 'Hour12',
                '1d': 'Day1', '3d': 'Day3', '1w': 'Week1', '1M': 'Month1'
            }
            
            mexc_interval = interval_map.get(interval, 'Min15')
            url = f"{EXCHANGES['MEXC']['base_url']}/api/v1/contract/kline/{symbol}"
            
            async with session.get(url, params={'interval': mexc_interval, 'limit': limit}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('success') and data.get('data'):
                        klines = []
                        for k in data['data']['data']:
                            klines.append({
                                'time': k['time'],
                                'open': float(k['open']),
                                'high': float(k['high']),
                                'low': float(k['low']),
                                'close': float(k['close']),
                                'volume': float(k['vol'])
                            })
                        return klines
        except Exception as e:
            logger.error(f"MEXC klines error for {symbol}: {e}")
        
        return []
    
    # ============================================
    # BYBIT
    # ============================================
    
    async def get_bybit_symbols(self) -> List[str]:
        """Pobiera listę par Bybit"""
        try:
            session = await self.get_session()
            url = f"{EXCHANGES['BYBIT']['base_url']}/v5/market/instruments-info"
            
            async with session.get(url, params={'category': 'linear'}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('result') and data['result'].get('list'):
                        symbols = [item['symbol'] for item in data['result']['list'] if item.get('symbol')]
                        logger.info(f"Bybit: pobrano {len(symbols)} par")
                        return sorted(symbols)
        except Exception as e:
            logger.error(f"Bybit symbols error: {e}")
        
        return []
    
    async def get_bybit_ticker(self, symbol: str) -> Optional[Dict]:
        """Pobiera ticker Bybit"""
        try:
            session = await self.get_session()
            url = f"{EXCHANGES['BYBIT']['base_url']}/v5/market/tickers"
            
            async with session.get(url, params={'category': 'linear', 'symbol': symbol}) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('result') and data['result'].get('list'):
                        ticker = data['result']['list'][0]
                        return {
                            'symbol': symbol,
                            'last_price': float(ticker.get('lastPrice', 0)),
                            'change_24h': float(ticker.get('price24hPcnt', 0)) * 100,
                            'volume_24h': float(ticker.get('volume24h', 0)),
                            'high_24h': float(ticker.get('highPrice24h', 0)),
                            'low_24h': float(ticker.get('lowPrice24h', 0))
                        }
        except Exception as e:
            logger.error(f"Bybit ticker error for {symbol}: {e}")
        
        return None
    
    async def get_bybit_klines(self, symbol: str, interval: str, limit: int = 100) -> List[Dict]:
        """Pobiera świece Bybit"""
        try:
            session = await self.get_session()
            url = f"{EXCHANGES['BYBIT']['base_url']}/v5/market/kline"
            
            # Bybit: 1,3,5,15,30,60,120,240,360,720,D,W,M
            interval_map = {
                '1m': '1', '3m': '3', '5m': '5', '15m': '15', '30m': '30',
                '1h': '60', '2h': '120', '4h': '240', '6h': '360', '12h': '720',
                '1d': 'D', '3d': 'D', '1w': 'W', '1M': 'M'
            }
            
            bybit_interval = interval_map.get(interval, '15')
            
            async with session.get(url, params={
                'category': 'linear',
                'symbol': symbol,
                'interval': bybit_interval,
                'limit': limit
            }) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('result') and data['result'].get('list'):
                        klines = []
                        for k in data['result']['list']:
                            klines.append({
                                'time': int(k[0]),
                                'open': float(k[1]),
                                'high': float(k[2]),
                                'low': float(k[3]),
                                'close': float(k[4]),
                                'volume': float(k[5])
                            })
                        return list(reversed(klines))  # Bybit zwraca od najnowszych
        except Exception as e:
            logger.error(f"Bybit klines error for {symbol}: {e}")
        
        return []
    
    # ============================================
    # BINANCE FUTURES
    # ============================================
    
    async def get_binance_symbols(self) -> List[str]:
        """Pobiera listę par Binance Futures"""
        try:
            session = await self.get_session()
            url = f"{EXCHANGES['BINANCE']['base_url']}/fapi/v1/exchangeInfo"
            
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get('symbols'):
                        symbols = [s['symbol'] for s in data['symbols'] if s.get('status') == 'TRADING']
                        logger.info(f"Binance: pobrano {len(symbols)} par")
                        return sorted(symbols)
        except Exception as e:
            logger.error(f"Binance symbols error: {e}")
        
        return []
    
    async def get_binance_ticker(self, symbol: str) -> Optional[Dict]:
        """Pobiera ticker Binance"""
        try:
            session = await self.get_session()
            url = f"{EXCHANGES['BINANCE']['base_url']}/fapi/v1/ticker/24hr"
            
            async with session.get(url, params={'symbol': symbol}) as resp:
                if resp.status == 200:
                    ticker = await resp.json()
                    return {
                        'symbol': symbol,
                        'last_price': float(ticker.get('lastPrice', 0)),
                        'change_24h': float(ticker.get('priceChangePercent', 0)),
                        'volume_24h': float(ticker.get('volume', 0)),
                        'high_24h': float(ticker.get('highPrice', 0)),
                        'low_24h': float(ticker.get('lowPrice', 0))
                    }
        except Exception as e:
            logger.error(f"Binance ticker error for {symbol}: {e}")
        
        return None
    
    async def get_binance_klines(self, symbol: str, interval: str, limit: int = 100) -> List[Dict]:
        """Pobiera świece Binance"""
        try:
            session = await self.get_session()
            url = f"{EXCHANGES['BINANCE']['base_url']}/fapi/v1/klines"
            
            # Binance: 1m,3m,5m,15m,30m,1h,2h,4h,6h,12h,1d,3d,1w,1M
            
            async with session.get(url, params={
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    klines = []
                    for k in data:
                        klines.append({
                            'time': k[0],
                            'open': float(k[1]),
                            'high': float(k[2]),
                            'low': float(k[3]),
                            'close': float(k[4]),
                            'volume': float(k[5])
                        })
                    return klines
        except Exception as e:
            logger.error(f"Binance klines error for {symbol}: {e}")
        
        return []
    
    # ============================================
    # UNIWERSALNE METODY
    # ============================================
    
    async def get_symbols(self, exchange: str) -> List[str]:
        """Pobiera symbole z wybranej giełdy"""
        if exchange == 'MEXC':
            return await self.get_mexc_symbols()
        elif exchange == 'BYBIT':
            return await self.get_bybit_symbols()
        elif exchange == 'BINANCE':
            return await self.get_binance_symbols()
        return []
    
    async def get_ticker(self, exchange: str, symbol: str) -> Optional[Dict]:
        """Pobiera ticker z wybranej giełdy"""
        if exchange == 'MEXC':
            return await self.get_mexc_ticker(symbol)
        elif exchange == 'BYBIT':
            return await self.get_bybit_ticker(symbol)
        elif exchange == 'BINANCE':
            return await self.get_binance_ticker(symbol)
        return None
    
    async def get_klines(self, exchange: str, symbol: str, interval: str, limit: int = 100) -> List[Dict]:
        """Pobiera świece z wybranej giełdy"""
        if exchange == 'MEXC':
            return await self.get_mexc_klines(symbol, interval, limit)
        elif exchange == 'BYBIT':
            return await self.get_bybit_klines(symbol, interval, limit)
        elif exchange == 'BINANCE':
            return await self.get_binance_klines(symbol, interval, limit)
        return []
    
    async def scan_extremes(self, exchange: str, limit: int = 10) -> Dict:
        """Skanuje największe wzrosty i spadki"""
        symbols = await self.get_symbols(exchange)
        
        if not symbols:
            return {'gainers': [], 'losers': []}
        
        # Pobierz tickery dla wszystkich symboli (max 50 naraz)
        tickers = []
        for symbol in symbols[:50]:  # Limit dla wydajności
            ticker = await self.get_ticker(exchange, symbol)
            if ticker and ticker['change_24h'] != 0:
                tickers.append(ticker)
            await asyncio.sleep(0.1)  # Rate limit
        
        # Sortuj
        gainers = sorted(tickers, key=lambda x: x['change_24h'], reverse=True)[:limit]
        losers = sorted(tickers, key=lambda x: x['change_24h'])[:limit]
        
        return {
            'gainers': gainers,
            'losers': losers
        }

# Globalna instancja
exchange_api = ExchangeAPI()
