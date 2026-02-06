#!/usr/bin/env python3
import asyncio
from datetime import datetime
from config import logger
from exchange_api import exchange_api

class AdvancedAISignals:
    
    # Blacklist: tokenizowane akcje i commodity (nie crypto!)
    BLACKLIST = ['TESLA', 'SILVER', 'GOLD', 'XAUT', 'AAPL', 'TSLA', 'GOOGL', 'AMZN', 'MSFT']
    
    # TOP cryptocurrencies by market cap (manual list - update quarterly)
    TOP_CRYPTOS = [
        'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'SOL/USDT', 'XRP/USDT',
        'ADA/USDT', 'AVAX/USDT', 'DOGE/USDT', 'DOT/USDT', 'MATIC/USDT',
        'LINK/USDT', 'TRX/USDT', 'SHIB/USDT', 'UNI/USDT', 'ATOM/USDT',
        'LTC/USDT', 'XLM/USDT', 'ETC/USDT', 'BCH/USDT', 'APT/USDT',
        'ARB/USDT', 'OP/USDT', 'INJ/USDT', 'SUI/USDT', 'TIA/USDT',
        'FIL/USDT', 'NEAR/USDT', 'IMX/USDT', 'STX/USDT', 'RUNE/USDT',
        'VET/USDT', 'FTM/USDT', 'ALGO/USDT', 'AAVE/USDT', 'GRT/USDT',
        'ICP/USDT', 'HBAR/USDT', 'APE/USDT', 'LDO/USDT', 'QNT/USDT',
        'MKR/USDT', 'SAND/USDT', 'MANA/USDT', 'AXS/USDT', 'THETA/USDT',
        'XTZ/USDT', 'EOS/USDT', 'FLOW/USDT', 'CHZ/USDT', 'GALA/USDT'
    ]  # Top 50 cryptos
    
    def __init__(self):
        self.timeframes = {
            '1m': '1 minuta', '3m': '3 minuty', '5m': '5 minut',
            '15m': '15 minut', '30m': '30 minut', '1h': '1 godzina',
            '2h': '2 godziny', '4h': '4 godziny', '8h': '8 godzin',
            '12h': '12 godzin', '1d': '1 dzień', '3d': '3 dni',
            '5d': '5 dni', '1w': '1 tydzień', '2w': '2 tygodnie',
            '1M': '1 miesiąc', '3M': '3 miesiące', '6M': '6 miesięcy',
            '1y': '1 rok', '2y': '2 lata', '3y': '3 lata'
        }
        
        self.scan_sizes = {
            'top10': 10, 'top50': 50, 'top100': 100,
            'top200': 200, 'top300': 300, 'top400': 400,
            'top500': 500, 'all': 9999
        }
    
    async def scan_with_filters(self, exchange, timeframe, scan_size='top10'):
        """Scan TOP pairs - SCORE ALL, show BEST"""
        try:
            all_symbols = await exchange_api.get_symbols(exchange)
            
            if not all_symbols:
                return []
            
            limit = self.scan_sizes.get(scan_size, 10)
            
            # Filter blacklist (akcje, commodity)
            all_symbols = [s for s in all_symbols if not any(bl in s for bl in self.BLACKLIST)]
            
            # Filter to only TOP cryptos if available
            if limit <= 50:
                # Use top cryptos list (with :USDT suffix for MEXC)
                top_with_suffix = [s.replace('/USDT', '/USDT:USDT') for s in self.TOP_CRYPTOS[:limit]]
                available_tops = [s for s in top_with_suffix if s in all_symbols]
                scan_symbols = available_tops if available_tops else list(all_symbols)[:limit]
            else:
                # For 100+, use all symbols
                scan_symbols = list(all_symbols)[:limit]
            
            logger.info(f"Scanning {len(scan_symbols)} pairs on {exchange}")
            
            results = []
            
            for symbol in scan_symbols:
                try:
                    data = await exchange_api.get_ohlcv(symbol, exchange, timeframe)
                    
                    if not data or len(data) < 50:
                        continue
                    
                    # Score każdej pary (0-100)
                    analysis = self.score_pair(symbol, data, timeframe)
                    
                    if analysis:
                        results.append(analysis)
                    
                except Exception as e:
                    logger.error(f"Error analyzing {symbol}: {e}")
                    continue
            
            # Sort by score (najlepsze pierwsze)
            results.sort(key=lambda x: x['score'], reverse=True)
            
            logger.info(f"Found {len(results)} signals, returning TOP 10")
            
            return results[:10]
            
        except Exception as e:
            logger.error(f"Scan error: {e}")
            return []
    
    def score_pair(self, symbol, data, timeframe):
        """Score pair 0-100 based on ALL indicators"""
        try:
            closes = [c[4] for c in data]
            volumes = [c[5] for c in data]
            highs = [c[2] for c in data]
            lows = [c[3] for c in data]
            
            current_price = closes[-1]
            prev_price = closes[-2]
            change_pct = ((current_price - prev_price) / prev_price) * 100
            
            # RSI
            rsi = self.calculate_rsi(closes)
            
            # Volume
            avg_volume = sum(volumes[-20:]) / 20
            current_volume = volumes[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # EMA
            ema_9 = self.calculate_ema(closes, 9)
            ema_21 = self.calculate_ema(closes, 21)
            ema_50 = self.calculate_ema(closes, 50)
            
            # Volatility (ATR-like)
            atr = sum([highs[i] - lows[i] for i in range(-14, 0)]) / 14
            volatility = (atr / current_price) * 100
            
            # SCORING SYSTEM
            score = 0
            signal = 'NEUTRAL'
            reasons = []
            confidence = 0
            
            # RSI scoring (0-25 points)
            if rsi < 30:
                score += 25
                reasons.append('RSI oversold')
                signal = 'LONG'
            elif rsi < 40:
                score += 15
                reasons.append('RSI low')
                signal = 'LONG'
            elif rsi > 70:
                score += 25
                reasons.append('RSI overbought')
                signal = 'SHORT'
            elif rsi > 60:
                score += 15
                reasons.append('RSI high')
                signal = 'SHORT'
            
            # Volume scoring (0-20 points)
            if volume_ratio > 3:
                score += 20
                reasons.append('Volume spike 3x+')
            elif volume_ratio > 2:
                score += 15
                reasons.append('Volume spike 2x+')
            elif volume_ratio > 1.5:
                score += 10
                reasons.append('Volume increase')
            
            # EMA Trend scoring (0-20 points)
            if ema_9 > ema_21 > ema_50:
                score += 20
                reasons.append('Strong uptrend')
                if signal == 'NEUTRAL':
                    signal = 'LONG'
            elif ema_9 < ema_21 < ema_50:
                score += 20
                reasons.append('Strong downtrend')
                if signal == 'NEUTRAL':
                    signal = 'SHORT'
            elif ema_9 > ema_21:
                score += 10
                reasons.append('Uptrend')
            elif ema_9 < ema_21:
                score += 10
                reasons.append('Downtrend')
            
            # Momentum scoring (0-20 points)
            if abs(change_pct) > 5:
                score += 20
                reasons.append(f'Strong momentum {change_pct:+.1f}%')
            elif abs(change_pct) > 3:
                score += 15
                reasons.append(f'Good momentum {change_pct:+.1f}%')
            elif abs(change_pct) > 1:
                score += 10
                reasons.append(f'Momentum {change_pct:+.1f}%')
            
            # Volatility scoring (0-15 points)
            if volatility > 3:
                score += 15
                reasons.append('High volatility')
            elif volatility > 2:
                score += 10
                reasons.append('Medium volatility')
            
            # Minimum score 20 to show (obniżony próg)
            if score < 20:
                logger.debug(f"score_pair {symbol}: score too low ({score}), skipping")
                return None
            
            # Calculate confidence from score
            confidence = min(score, 95)
            
            # Calculate TP levels
            if signal == 'LONG':
                tp1 = current_price * 1.015
                tp2 = current_price * 1.03
                tp3 = current_price * 1.05
            elif signal == 'SHORT':
                tp1 = current_price * 0.985
                tp2 = current_price * 0.97
                tp3 = current_price * 0.95
            else:
                tp1 = tp2 = tp3 = current_price
            
            # Log final score
            logger.info(f"score_pair {symbol}: score={score}, signal={signal}, conf={confidence}%")
            
            return {
                'symbol': symbol,
                'signal': signal,
                'score': score,
                'confidence': confidence,
                'entry': current_price,
                'tp1': tp1,
                'tp2': tp2,
                'tp3': tp3,
                'rsi': rsi,
                'volume_ratio': volume_ratio,
                'change_pct': change_pct,
                'reasons': reasons[:3]  # Top 3 reasons
            }
            
        except Exception as e:
            logger.error(f"Scoring error: {e}")
            return None
    
    def calculate_rsi(self, closes, period=14):
        """Calculate RSI"""
        if len(closes) < period:
            return 50
        
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        gains = [d if d > 0 else 0 for d in deltas[-period:]]
        losses = [-d if d < 0 else 0 for d in deltas[-period:]]
        
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_ema(self, closes, period):
        """Calculate EMA"""
        if len(closes) < period:
            return closes[-1]
        
        multiplier = 2 / (period + 1)
        ema = closes[0]
        
        for price in closes[1:]:
            ema = (price - ema) * multiplier + ema
        
        return ema

advanced_ai_signals = AdvancedAISignals()
logger.info("✅ Advanced AI Signals initialized")
