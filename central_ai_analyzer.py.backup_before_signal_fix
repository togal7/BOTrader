#!/usr/bin/env python3
"""
CENTRALNY AI ANALYZER - Ultra zaawansowana analiza dla wszystkich funkcji bota
Łączy: Technical Analysis + DeepSeek AI + Perplexity News + Sentiment
"""
import asyncio
from datetime import datetime, timedelta
from config import logger
from exchange_api import exchange_api
import json
from elliott_wave_detector import ElliottWaveDetector
from volume_profile import VolumeProfile
from advanced_indicators import AdvancedIndicators

class CentralAIAnalyzer:
    def __init__(self):
        self.deepseek_enabled = True  # Later: integrate DeepSeek API
        self.perplexity_enabled = True  # Later: integrate Perplexity API
    
        logger.info('✅  Central AI Analyzer initialized')
        self.ewt = ElliottWaveDetector()
        self.vp = VolumeProfile()
        self.adv_ind = AdvancedIndicators()

    def _elliott_wave_analysis(self, data):
        """Elliott Wave analysis on multi-timeframes"""
        try:
            ewt_primary = self.ewt.detect_waves(data.get('primary', []), data.get('primary_tf', '1h'))
            ewt_higher = self.ewt.detect_waves(data.get('higher', []), data.get('higher_tf', '4h'))
            
            # Multi-TF alignment
            alignment = 0
            if ewt_higher.get('bias') == ewt_primary.get('bias'):
                alignment += 2
            if ewt_primary.get('current_wave') in [3, 5]:
                alignment += 2
            elif ewt_primary.get('current_wave') == 4:
                alignment += 1
            
            confidence = ewt_primary.get('confidence', 0)
            if alignment >= 3:
                confidence = min(100, confidence + 15)
            
            return {
                'primary': ewt_primary,
                'higher': ewt_higher,
                'alignment_score': alignment,
                'bias': ewt_primary.get('bias', 'NEUTRAL'),
                'confidence': confidence,
                'reasoning': ewt_primary.get('reasoning', 'No EWT pattern')
            }
        except Exception as e:
            logger.error(f"EWT error: {e}")
            return {'bias': 'NEUTRAL', 'confidence': 0}

    async def analyze_pair_full(self, symbol: str, exchange: str, timeframe: str = "15m", context: str = "general", language: str = "pl", skip_ai: bool = False):
        """
        GŁÓWNA FUNKCJA - Pełna analiza pary
        
        context: 'search', 'scan_extreme', 'ai_signal', 'general'
        """
        logger.info(f"Starting FULL analysis: {symbol} on {exchange} ({timeframe})")
        
        try:
            # 1. POBIERZ DANE
            ohlcv_data = await self._fetch_multi_timeframe_data(exchange, symbol, timeframe)
            ticker = await exchange_api.get_ticker(symbol, exchange)
            
            if not ohlcv_data or not ticker:
                return None
            
            # 2. TECHNICAL ANALYSIS (wszystkie wskaźniki)
            technical = self._technical_analysis(ohlcv_data, timeframe)
            
            # 3. MARKET STRUCTURE (S/R, patterns)
            structure = self._market_structure_analysis(ohlcv_data)
            
            # 4. VOLUME ANALYSIS
            volume_analysis = self._volume_analysis(ohlcv_data)
            
            # 5. SENTIMENT SCORE (z danych technicznych)
            sentiment = self._calculate_sentiment(technical, structure, volume_analysis)
            
            # 5b. ELLIOTT WAVE ANALYSIS
            ewt_analysis = self._elliott_wave_analysis(ohlcv_data)
            
            # 6. AI REASONING (później: DeepSeek)
            if skip_ai:
                # Fast mode - skip DeepSeek API
                ai_reasoning = {
                    'summary': ['Tryb szybki - tylko wskaźniki techniczne'],
                    'confidence': 50,
                    'signal': 'NEUTRAL',
                    'source': 'Fast Mode (Technical Only)'
                }
            else:
                ai_reasoning = await self._ai_reasoning(
                    symbol, technical, structure, volume_analysis, sentiment, context, language
                )
            
            # 7. NEWS & EVENTS (później: Perplexity)
            news_impact = await self._get_news_impact(symbol)
            
            # 8. GENERATE SIGNAL
            signal = await self._generate_trading_signal(
                technical, structure, volume_analysis, sentiment, ai_reasoning, news_impact, ewt_analysis
            )
            
            # 9. COMPILE FULL REPORT
            report = {
                'symbol': symbol,
                'exchange': exchange,
                'timeframe': timeframe,
                'timestamp': datetime.now().isoformat(),
                'current_price': ohlcv_data['current'][4],
                'technical': technical,
                'structure': structure,
                'volume': volume_analysis,
                'sentiment': sentiment,
                'ewt': ewt_analysis,
                'ai_reasoning': ai_reasoning,
                'news': news_impact,
                'signal': signal,
                'context': context
            }
            
            logger.info(f"Analysis complete: {symbol} - {signal['direction']} {signal['confidence']}%")
            
            return report
            
        except Exception as e:
            logger.error(f"Analysis error for {symbol}: {e}")
            return None
    
    async def _fetch_multi_timeframe_data(self, exchange, symbol, primary_tf):
        """Pobierz dane z wielu timeframe'ów"""
        try:
            # Primary timeframe (requested)
            primary = await exchange_api.get_ohlcv(symbol, exchange, primary_tf, 100)
            
            # Higher timeframe (trend context)
            higher_tf = self._get_higher_timeframe(primary_tf)
            higher = await exchange_api.get_ohlcv(symbol, exchange, higher_tf, 50)
            
            # Lower timeframe (entry precision)
            lower_tf = self._get_lower_timeframe(primary_tf)
            lower = await exchange_api.get_ohlcv(symbol, exchange, lower_tf, 200)
            
            return {
                'current': primary[-1] if primary else None,
                'primary': primary,
                'higher': higher,
                'lower': lower,
                'primary_tf': primary_tf,
                'higher_tf': higher_tf,
                'lower_tf': lower_tf
            }
        except:
            return None
    
    def _technical_analysis(self, data, timeframe):
        """Wszystkie wskaźniki techniczne"""
        primary = data['primary']
        
        if not primary or len(primary) < 50:
            return {}
        
        closes = [c[4] for c in primary]
        highs = [c[2] for c in primary]
        lows = [c[3] for c in primary]
        volumes = [c[5] for c in primary]
        
        # RSI (14, 7, 21)
        rsi_14 = self._calculate_rsi(closes, 14)
        rsi_7 = self._calculate_rsi(closes, 7)
        rsi_21 = self._calculate_rsi(closes, 21)
        
        # EMA (9, 21, 50, 200)
        ema_9 = self._calculate_ema(closes, 9)
        ema_21 = self._calculate_ema(closes, 21)
        ema_50 = self._calculate_ema(closes, 50)
        ema_200 = self._calculate_ema(closes, 200) if len(closes) >= 200 else None
        
        # MACD
        macd = self._calculate_macd(closes)
        
        # Bollinger Bands
        bb = self._calculate_bollinger_bands(closes)
        
        # ATR (volatility)
        atr = self._calculate_atr(highs, lows, closes)
        
        # Stochastic
        stoch = self._calculate_stochastic(highs, lows, closes)
        
        # ADX (trend strength)
        adx = self._calculate_adx(highs, lows, closes)
        
        current_price = closes[-1]
        

        # Ichimoku Cloud
        try:
            ichimoku = self.adv_ind.calculate_ichimoku(highs, lows, closes)
            atr_stop = self.adv_ind.calculate_atr_trailing_stop(highs, lows, closes)
        except Exception as e:
            logger.error(f'Ichimoku calc error: {e}')
            ichimoku = {'signal': 'NEUTRAL', 'confidence': 0}
            atr_stop = {}

        return {
            'price': current_price,
            'rsi': {'14': rsi_14, '7': rsi_7, '21': rsi_21},
            'ema': {'9': ema_9, '21': ema_21, '50': ema_50, '200': ema_200},
            'macd': macd,
            'bollinger': bb,
            'atr': atr,
            'stochastic': stoch,
            'adx': adx,
            'ichimoku': ichimoku,
            'atr_stop': atr_stop,
            'change_24h': ((current_price - closes[-24]) / closes[-24] * 100) if len(closes) >= 24 else 0
        }
    
    def _market_structure_analysis(self, data):
        """Support/Resistance, patterns, trend"""
        primary = data['primary']
        
        if not primary or len(primary) < 50:
            return {}
        
        closes = [c[4] for c in primary]
        highs = [c[2] for c in primary]
        lows = [c[3] for c in primary]
        
        # Find S/R levels
        support_levels = self._find_support_levels(lows, closes[-1])
        resistance_levels = self._find_resistance_levels(highs, closes[-1])
        
        # Trend direction
        trend = self._identify_trend(closes)
        
        # Chart patterns (simplified)
        patterns = self._detect_patterns(closes, highs, lows)
        
        return {
            'support': support_levels[:3],  # Top 3
            'resistance': resistance_levels[:3],
            'trend': trend,
            'patterns': patterns
        }
    
    def _volume_analysis(self, data):
        """Volume profile, buying/selling pressure + VP"""
        primary = data['primary']
        if not primary:
            return {
                'current_vs_avg': 1.0,
                'vp_data': {}
            }
        
        volumes = [c[5] for c in primary]
        closes = [c[4] for c in primary]
        opens = [c[1] for c in primary]
        
        avg_volume = sum(volumes[-20:]) / 20
        current_volume = volumes[-1]
        volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
        
        # Buying vs selling pressure
        buy_volume = sum([volumes[i] for i in range(-20, 0) if closes[i] > opens[i]])
        sell_volume = sum([volumes[i] for i in range(-20, 0) if closes[i] < opens[i]])
        buy_pressure = (buy_volume / (buy_volume + sell_volume) * 100) if (buy_volume + sell_volume) > 0 else 50
        
        # Volume Profile + POC
        try:
            vp_data = self.vp.analyze(primary, data.get('primary_tf', '1h'))
        except Exception as e:
            logger.error(f"VP error: {e}")
            vp_data = {}
        
        return {
            'current': current_volume,
            'average': avg_volume,
            'ratio': volume_ratio,
            'current_vs_avg': volume_ratio,
            'buy_pressure': buy_pressure,
            'sell_pressure': 100 - buy_pressure,
            'vp_data': vp_data,
            'current_price': closes[-1]
        }

    def _calculate_sentiment(self, technical, structure, volume):
        """Oblicz ogólny sentyment rynku dla pary"""
        score = 0
        signals = []
        
        # RSI sentiment
        rsi = technical.get('rsi', {}).get('14', 50)
        if rsi < 30:
            score += 30
            signals.append('Oversold')
        elif rsi < 40:
            score += 15
            signals.append('Low RSI')
        elif rsi > 70:
            score -= 30
            signals.append('Overbought')
        elif rsi > 60:
            score -= 15
            signals.append('High RSI')
        
        # EMA trend sentiment
        ema = technical.get('ema', {})
        if ema.get('9') and ema.get('21') and ema.get('50'):
            if ema['9'] > ema['21'] > ema['50']:
                score += 25
                signals.append('Strong uptrend')
            elif ema['9'] < ema['21'] < ema['50']:
                score -= 25
                signals.append('Strong downtrend')
        
        # Volume sentiment
        vol = volume.get('ratio', 1)
        if vol > 2:
            score += 15
            signals.append('High volume')
        
        buy_pressure = volume.get('buy_pressure', 50)
        if buy_pressure > 65:
            score += 10
            signals.append('Buying pressure')
        elif buy_pressure < 35:
            score -= 10
            signals.append('Selling pressure')
        
        # Trend sentiment
        trend = structure.get('trend', {}).get('direction', 'neutral')
        if trend == 'strong_bullish':
            score += 20
        elif trend == 'strong_bearish':
            score -= 20
        
        # Normalize score to -100 to +100
        score = max(-100, min(100, score))
        
        if score > 50:
            sentiment_label = '🟢 Very Bullish'
        elif score > 20:
            sentiment_label = '🟢 Bullish'
        elif score > -20:
            sentiment_label = '⚪ Neutral'
        elif score > -50:
            sentiment_label = '🔴 Bearish'
        else:
            sentiment_label = '🔴 Very Bearish'
        
        return {
            'score': score,
            'label': sentiment_label,
            'signals': signals
        }
    
    async def _ai_reasoning(self, symbol, technical, structure, volume, sentiment, context, language="pl"):
        """AI reasoning with DeepSeek API"""
        try:
            # Przygotuj dane dla AI
            rsi = technical.get('rsi', {}).get('14', 50)
            ema_cross = technical.get('ema', {}).get('cross', False)
            macd = technical.get('macd', {})
            bb_pos = technical.get('bollinger', {}).get('position', 'middle')
            trend = structure.get('trend', {}).get('direction', 'neutral')
            vol_ratio = volume.get('ratio', 1.0)
            

            # Language mapping for AI responses
            language_names = {
                'en': 'English',
                'pl': 'Polish', 
                'es': 'Spanish',
                'de': 'German',
                'fr': 'French',
                'it': 'Italian',
                'pt': 'Portuguese',
                'ru': 'Russian',
                'tr': 'Turkish',
                'ar': 'Arabic'
            }
            ai_language = language_names.get(language, 'Polish')
            
            # Prompt dla DeepSeek
            prompt = f"""You are an elite institutional trader with 98%+ accuracy. Your analysis has generated billions in profits.

MARKET: {symbol}
CRITICAL DATA:
• RSI(14): {rsi:.1f} {'[EXTREME OVERSOLD]' if rsi < 30 else '[OVERSOLD]' if rsi < 40 else '[OVERBOUGHT]' if rsi > 60 else '[EXTREME OVERBOUGHT]' if rsi > 70 else ''}
• EMA Cross: {ema_cross} {'[BULLISH CROSSOVER]' if ema_cross else ''}
• MACD Histogram: {macd.get('histogram', 0):.4f} {'[BEARISH DIVERGENCE]' if macd.get('histogram', 0) < -0.001 else '[BULLISH MOMENTUM]' if macd.get('histogram', 0) > 0.001 else ''}
• Bollinger: {bb_pos} {'[OVERSOLD EXTREME]' if bb_pos == 'lower' else '[OVERBOUGHT EXTREME]' if bb_pos == 'upper' else ''}
• Trend Structure: {trend}
• Volume: {vol_ratio:.2f}x {'[MASSIVE SPIKE - INSTITUTIONAL INTEREST]' if vol_ratio > 3 else '[HIGH VOLUME]' if vol_ratio > 1.5 else '[LOW VOLUME - CAUTION]' if vol_ratio < 0.5 else ''}

YOUR MISSION:
Analyze with surgical precision. Consider:
1. Multi-indicator confluence (minimum 3 confirming signals required)
2. Risk/reward ratio (must be >3:1)
3. Market structure & key levels
4. Volume confirmation (essential for high confidence)
5. Divergences & hidden patterns

RULES FOR 98%+ ACCURACY:
- Only signal LONG/SHORT when 4+ indicators align perfectly
- Confidence >80% requires EXTREME confluence + volume confirmation
- Confidence 60-80% requires 3+ aligned indicators
- Confidence <60% or conflicting signals = NEUTRAL (skip trade)
- Never chase FOMO - patience is profit

OUTPUT STRICT JSON:
{{
  "signal": "LONG" or "SHORT" or "NEUTRAL",
  "confidence": 0-100 (be conservative - real money at stake),
  "reasoning": [
    "Główny sygnał z konkretną wartością (e.g. RSI=23.5 - skrajnie wyprzedany)",
    "Secondary confirmation with data",
    "Volume/momentum validation",
    "Risk/reward calculation"
  ],
  "risk_level": "low" (80%+ conf) or "medium" (60-80%) or "high" (<60%),
  "entry_quality": "A+" (perfect) or "A" (excellent) or "B" (good) or "C" (skip)
}}

THINK LIKE A BILLIONAIRE TRADER - ONLY THE BEST SETUPS.

IMPORTANT: Respond in {ai_language} language for all reasoning text. Use professional trading terminology in Polish."""

            # Call DeepSeek API
            import requests
            from config import DEEPSEEK_API_KEY
            
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'deepseek-chat',
                    'messages': [
                        {'role': 'system', 'content': 'You are an expert crypto trader. Respond only with valid JSON.'},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.3,
                    'max_tokens': 500
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_text = data['choices'][0]['message']['content']
                
                # Parse JSON response
                import json
                import re
                # Extract JSON from response (może być w ```json```)
                json_match = re.search(r'\{.*\}', ai_text, re.DOTALL)
                if json_match:
                    ai_result = json.loads(json_match.group())
                    
                    logger.info(f"🤖 DeepSeek: {ai_result.get('signal')} {ai_result.get('confidence')}%")
                    
                    return {
                        'summary': ai_result.get('reasoning', []),
                        'confidence': ai_result.get('confidence', 50),
                        'signal': ai_result.get('signal', 'NEUTRAL'),
                        'risk_level': ai_result.get('risk_level', 'medium'),
                        'source': 'DeepSeek AI'
                    }
            
            # Fallback to technical if API fails
            logger.warning("DeepSeek API failed, using technical analysis")
            
        except Exception as e:
            logger.error(f"DeepSeek error: {e}")
        
        # Fallback: Technical reasoning (original code)
        reasoning = []
        rsi = technical.get('rsi', {}).get('14', 50)
        if rsi < 35:
            reasoning.append("RSI shows oversold conditions, potential bounce opportunity")
        elif rsi > 65:
            reasoning.append("RSI indicates overbought, possible correction incoming")
        
        trend = structure.get('trend', {}).get('direction', 'neutral')
        if 'bullish' in trend:
            reasoning.append("Price respects higher timeframe uptrend")
        elif 'bearish' in trend:
            reasoning.append("Downtrend remains intact on HTF")
        
        if volume.get('ratio', 1) > 2:
            reasoning.append("Unusual volume spike suggests strong interest")
        
        return {
            'summary': reasoning,
            'confidence': self._calculate_reasoning_confidence(technical, structure, volume),
            'source': 'Technical Analysis (AI unavailable)'
        }

    async def _get_news_impact(self, symbol):
        """News & events - później Perplexity"""
        # PLACEHOLDER - później integration with Perplexity
        
        return {
            'recent_news': [],
            'sentiment': 'neutral',
            'impact_score': 0,
            'source': 'None'  # Later: 'Perplexity AI'
        }
    
    async def _generate_trading_signal(self, technical, structure, volume, sentiment, ai_reasoning, news, ewt_analysis=None):
        """Generate final trading signal"""
        
        # Determine direction
        sent_score = sentiment['score']
        
        if sent_score > 30:
            direction = 'LONG'
        elif sent_score < -30:
            direction = 'SHORT'
        else:
            direction = 'NEUTRAL'
        
        # Calculate confidence (0-100)
        confidence = self._calculate_signal_confidence(
            technical, structure, volume, sentiment, ai_reasoning
        )
        
        # Calculate TP/SL levels
        current_price = technical['price']
        atr = technical.get('atr', current_price * 0.02)
        
        if direction == 'LONG':
            entry = current_price
            tp1 = current_price + (atr * 1.5)
            tp2 = current_price + (atr * 3)
            tp3 = current_price + (atr * 5)
            sl = current_price - (atr * 2)
        elif direction == 'SHORT':
            entry = current_price
            tp1 = current_price - (atr * 1.5)
            tp2 = current_price - (atr * 3)
            tp3 = current_price - (atr * 5)
            sl = current_price + (atr * 2)
        else:
            # NEUTRAL - podaj range (możliwość obu kierunków)
            entry = current_price
            tp1 = current_price + (atr * 1.5)  # Upside target
            tp2 = current_price - (atr * 1.5)  # Downside target  
            tp3 = current_price  # No strong direction
            sl = current_price  # No clear stop
        
        # Risk/Reward
        if direction != 'NEUTRAL':
            risk = abs(entry - sl)
            reward = abs(tp2 - entry)
            rr_ratio = reward / risk if risk > 0 else 0
        else:
            rr_ratio = 0
        

        # Get AI analysis
        try:
            # ai_analysis = await ai_trader.get_ai_analysis(
            # symbol=symbol,
            # data=data,
            # indicators=indicators,
            # news_sentiment=news_sentiment,
            # trading_mode=trading_mode
            # )
            ai_analysis = None  # AI trader disabled
            
            if ai_analysis:
                logger.info(f"✅ AI analysis received for {symbol}")
                # Możemy użyć ai_analysis['analysis'] w outputcie
        except Exception as e:
            logger.error(f"AI analysis error: {e}")
            ai_analysis = None
        
        return {
            'direction': direction,
            'confidence': confidence,
            'score': score if 'score' in locals() else 0,
            'reasoning': reasoning if 'reasoning' in locals() else [],
            'horizon': self._calculate_time_horizon(direction, confidence, ewt_analysis),
            'ai_analysis': ai_analysis,
            'entry': entry,
            'tp1': tp1,
            'tp2': tp2,
            'tp3': tp3,
            'sl': sl,
            'rr_ratio': rr_ratio,
            'reasons': sentiment['signals'] + ai_reasoning['summary'][:3]
        }
    
    # HELPER FUNCTIONS (indicators)
    
    def _calculate_rsi(self, closes, period=14):
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
        return 100 - (100 / (1 + rs))
    
    def _calculate_ema(self, closes, period):
        if len(closes) < period:
            return closes[-1]
        multiplier = 2 / (period + 1)
        ema = closes[0]
        for price in closes[1:]:
            ema = (price - ema) * multiplier + ema
        return ema
    
    def _calculate_macd(self, closes):
        ema_12 = self._calculate_ema(closes, 12)
        ema_26 = self._calculate_ema(closes, 26)
        macd_line = ema_12 - ema_26
        # Signal line (9 EMA of MACD) - simplified
        signal_line = macd_line * 0.9
        histogram = macd_line - signal_line
        return {'macd': macd_line, 'signal': signal_line, 'histogram': histogram}
    
    def _calculate_bollinger_bands(self, closes, period=20):
        if len(closes) < period:
            return {}
        sma = sum(closes[-period:]) / period
        variance = sum([(c - sma) ** 2 for c in closes[-period:]]) / period
        std_dev = variance ** 0.5
        return {
            'upper': sma + (2 * std_dev),
            'middle': sma,
            'lower': sma - (2 * std_dev)
        }
    
    def _calculate_atr(self, highs, lows, closes, period=14):
        if len(closes) < period:
            return (highs[-1] - lows[-1])
        true_ranges = []
        for i in range(1, len(closes)):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1])
            )
            true_ranges.append(tr)
        return sum(true_ranges[-period:]) / period
    
    def _calculate_stochastic(self, highs, lows, closes, period=14):
        if len(closes) < period:
            return 50
        lowest_low = min(lows[-period:])
        highest_high = max(highs[-period:])
        if highest_high == lowest_low:
            return 50
        k = ((closes[-1] - lowest_low) / (highest_high - lowest_low)) * 100
        return k
    
    def _calculate_adx(self, highs, lows, closes, period=14):
        # Simplified ADX
        if len(closes) < period:
            return 20
        # Placeholder - real ADX is complex
        return 25
    
    def _find_support_levels(self, lows, current_price):
        # Find recent lows as support
        supports = sorted(set([l for l in lows[-50:] if l < current_price]))
        return supports[-5:] if supports else []
    
    def _find_resistance_levels(self, highs, current_price):
        # Find recent highs as resistance
        resistances = sorted(set([h for h in highs[-50:] if h > current_price]))
        return resistances[:5] if resistances else []
    
    def _identify_trend(self, closes):
        if len(closes) < 50:
            return {'direction': 'neutral', 'strength': 0}
        
        recent = closes[-20:]
        older = closes[-50:-30]
        
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)
        
        change = ((recent_avg - older_avg) / older_avg) * 100
        
        if change > 5:
            return {'direction': 'strong_bullish', 'strength': min(change, 100)}
        elif change > 2:
            return {'direction': 'bullish', 'strength': change}
        elif change < -5:
            return {'direction': 'strong_bearish', 'strength': abs(change)}
        elif change < -2:
            return {'direction': 'bearish', 'strength': abs(change)}
        else:
            return {'direction': 'neutral', 'strength': 0}
    
    def _detect_patterns(self, closes, highs, lows):
        # Simplified pattern detection
        patterns = []
        
        # Double bottom/top (simplified)
        if len(lows) >= 20:
            recent_lows = lows[-20:]
            if min(recent_lows[-5:]) > min(recent_lows[-15:-10]):
                patterns.append('Potential Double Bottom')
        
        return patterns
    
    def _calculate_reasoning_confidence(self, technical, structure, volume):
        # Calculate AI reasoning confidence
        score = 50  # Base
        
        # Strong indicators add confidence
        rsi = technical.get('rsi', {}).get('14', 50)
        if rsi < 25 or rsi > 75:
            score += 15
        
        vol_ratio = volume.get('ratio', 1)
        if vol_ratio > 2:
            score += 10
        
        trend = structure.get('trend', {}).get('strength', 0)
        if trend > 5:
            score += 10
        
        return min(score, 95)
    
    def _calculate_signal_confidence(self, technical, structure, volume, sentiment, ai_reasoning):
        # Final signal confidence
        base = abs(sentiment.get('sentiment', 0))  # 0-100
        
        # Boost from AI reasoning
        ai_conf = ai_reasoning.get('confidence', 50)
        
        # Average weighted
        confidence = (base * 0.5) + (ai_conf * 0.5)
        
        return min(int(confidence), 95)
    
    def _get_higher_timeframe(self, tf):
        mapping = {
            '1m': '5m', '3m': '15m', '5m': '15m', '15m': '1h',
            '30m': '4h', '1h': '4h', '2h': '1d', '4h': '1d',
            '8h': '1d', '12h': '1d', '1d': '1w', '3d': '1w',
            '1w': '1M', '2w': '1M', '1M': '3M'
        }
        return mapping.get(tf, '1d')
    
    def _get_lower_timeframe(self, tf):
        mapping = {
            '5m': '1m', '15m': '5m', '30m': '15m', '1h': '15m',
            '4h': '1h', '1d': '4h', '1w': '1d', '1M': '1w'
        }
        return mapping.get(tf, tf)

    def _get_mtf_set(self, main_tf):
        """Get complete MTF set: LTF, Main, HTF1, HTF2"""
        ltf = self._get_lower_timeframe(main_tf)
        htf1 = self._get_higher_timeframe(main_tf)
        htf2 = self._get_higher_timeframe(htf1)
        
        return {
            'ltf': ltf,
            'main': main_tf,
            'htf1': htf1,
            'htf2': htf2
        }



    def _calculate_time_horizon(self, direction: str, confidence: int, ewt_analysis=None) -> str:
        """Oblicz horyzont czasowy (kompatybilność z Sygnały AI)"""
        if direction == "NEUTRAL" or confidence < 50:
            return "?"
        
        # EWT-based
        if ewt_analysis and ewt_analysis.get('primary', {}).get('valid'):
            wave = ewt_analysis['primary'].get('current_wave')
            if wave in [3, 5]:
                return "4h-1d" if confidence >= 80 else "1h-4h"
            elif wave in [2, 4]:
                return "1h-4h"
        
        # Confidence-based
        if confidence >= 80:
            return "4h-1d"
        elif confidence >= 70:
            return "1h-4h"
        else:
            return "15m-1h"

    async def analyze_for_ai_signals(self, symbol: str, main_tf: str, exchange: str = 'mexc', language: str = 'pl') -> dict:
        """
        Multi-Timeframe Analysis dla AI Signals
        
        Waliduje sygnał na 3 timeframe'ach:
        - HTF (Higher): Trend direction
        - Main TF: Główny sygnał
        - LTF (Lower): Entry timing
        
        Returns dict z enhanced confidence i realistic targets
        """
        logger.info(f"🎯 AI Signals MTF: {symbol} on {main_tf}")
        
        # Mapowanie TF → HTF/LTF
        tf_map = {
            '1m': {'htf': '5m', 'ltf': None},
            '3m': {'htf': '15m', 'ltf': '1m'},
            '5m': {'htf': '15m', 'ltf': '1m'},
            '15m': {'htf': '1h', 'ltf': '5m'},
            '30m': {'htf': '1h', 'ltf': '15m'},
            '1h': {'htf': '4h', 'ltf': '30m'},
            '2h': {'htf': '4h', 'ltf': '1h'},
            '4h': {'htf': '1d', 'ltf': '1h'},
            '8h': {'htf': '1d', 'ltf': '4h'},
            '12h': {'htf': '1d', 'ltf': '4h'},
            '1d': {'htf': '1w', 'ltf': '4h'},
            '3d': {'htf': '1w', 'ltf': '1d'},
            '1w': {'htf': '1M', 'ltf': '1d'},
            '2w': {'htf': '1M', 'ltf': '1w'},
            '1M': {'htf': None, 'ltf': '1w'}
        }
        
        htf = tf_map.get(main_tf, {}).get('htf')
        ltf = tf_map.get(main_tf, {}).get('ltf')
        
        # Analiza głównego TF
        main_analysis = await self.analyze_pair_full(symbol, exchange, main_tf, 'ai_signals', language)
        
        if not main_analysis or not main_analysis.get('signal'):
            return None
        
        main_signal = main_analysis['signal']
        base_confidence = main_signal.get('confidence', 0) if isinstance(main_signal, dict) else 0
        direction = main_signal.get('direction', 'NEUTRAL') if isinstance(main_signal, dict) else 'NEUTRAL'
        
        # Skip NEUTRAL - tylko LONG/SHORT
        # if direction == 'NEUTRAL':
        #            return None
        

        # ════════════════════════════════════════════════════════
        # PATTERN BOOST - Hard-coded strong patterns (+25%)
        # ════════════════════════════════════════════════════════
        pattern_boost = 0
        pattern_reason = []
        
        # Pobierz technical indicators
        tech = main_analysis.get('technical', {})
        
        # RSI może być dict lub liczba
        rsi_raw = tech.get('rsi', 50)
        rsi = rsi_raw.get('value', 50) if isinstance(rsi_raw, dict) else rsi_raw
        
        # EMA może być dict lub liczba
        ema_20_raw = tech.get('ema_20', 0)
        ema_20 = ema_20_raw.get('value', 0) if isinstance(ema_20_raw, dict) else ema_20_raw
        
        ema_50_raw = tech.get('ema_50', 0)
        ema_50 = ema_50_raw.get('value', 0) if isinstance(ema_50_raw, dict) else ema_50_raw
        
        volume_ratio = tech.get('volume_ratio', 1.0)
        
        # LONG patterns
        if direction == 'LONG':
            if rsi < 30 and volume_ratio > 1.5:
                pattern_boost += 15
                pattern_reason.append("Oversold + Volume")
            if ema_20 > 0 and ema_50 > 0 and ema_20 > ema_50:
                pattern_boost += 10
                pattern_reason.append("Golden Cross")
            if rsi < 25:
                pattern_boost += 5
                pattern_reason.append("Extreme Oversold")
        
        # SHORT patterns
        elif direction == 'SHORT':
            if rsi > 70 and volume_ratio > 1.5:
                pattern_boost += 15
                pattern_reason.append("Overbought + Volume")
            if ema_20 > 0 and ema_50 > 0 and ema_20 < ema_50:
                pattern_boost += 10
                pattern_reason.append("Death Cross")
            if rsi > 75:
                pattern_boost += 5
                pattern_reason.append("Extreme Overbought")
        
        if pattern_boost > 0:
            logger.info(f"  🎯 Pattern boost: +{pattern_boost}% ({', '.join(pattern_reason)})")

        # Multi-TF Validation
        mtf_boost = 0
        htf_aligned = False
        ltf_aligned = False
        
        # HTF validation (trend)
        if htf:
            try:
                htf_analysis = await self.analyze_pair_full(symbol, exchange, htf, 'ai_signals_htf', language)
                if htf_analysis and htf_analysis.get('signal'):
                    htf_dir = htf_analysis['signal'].get('direction', 'NEUTRAL') if isinstance(htf_analysis.get('signal'), dict) else 'NEUTRAL'
                    if htf_dir == direction:
                        htf_aligned = True
                        mtf_boost += 15
                        logger.info(f"  ✅ HTF {htf}: {htf_dir} aligned")
            except:
                pass
        
        # LTF validation (entry timing)
        if ltf:
            try:
                ltf_analysis = await self.analyze_pair_full(symbol, exchange, ltf, 'ai_signals_ltf', language)
                if ltf_analysis and ltf_analysis.get('signal'):
                    ltf_dir = ltf_analysis['signal'].get('direction', 'NEUTRAL') if isinstance(ltf_analysis.get('signal'), dict) else 'NEUTRAL'
                    # LTF może być pullback (opposite OK dla entry)
                    if ltf_dir == direction or ltf_dir == 'NEUTRAL':
                        ltf_aligned = True
                        mtf_boost += 10
                        logger.info(f"  ✅ LTF {ltf}: entry OK")
            except:
                pass
        
        # Enhanced confidence
        final_confidence = min(base_confidence + mtf_boost + pattern_boost, 95)
        
        # Realistic TP based on TF
        current_price = main_analysis.get('current_price', 0)
        if not current_price or current_price == 0:
            logger.error(f"Invalid price for {symbol}")
            return None
        atr = main_analysis['technical'].get('atr', current_price * 0.02)
        
        # TP multipliers per TF category
        tf_multipliers = {
            '1m': 0.3, '3m': 0.4, '5m': 0.5,
            '15m': 1.0, '30m': 1.5, '1h': 2.0,
            '2h': 2.5, '4h': 3.0, '8h': 3.5,
            '12h': 4.0, '1d': 4.5, '3d': 5.0,
            '1w': 6.0, '2w': 7.0, '1M': 8.0
        }
        
        multiplier = tf_multipliers.get(main_tf, 1.5)
        
        if direction == 'LONG':
            tp1 = current_price + (atr * multiplier * 0.5)
            tp2 = current_price + (atr * multiplier * 1.0)
            tp3 = current_price + (atr * multiplier * 1.5)
            sl = current_price - (atr * multiplier * 0.7)
        else:  # SHORT
            tp1 = current_price - (atr * multiplier * 0.5)
            tp2 = current_price - (atr * multiplier * 1.0)
            tp3 = current_price - (atr * multiplier * 1.5)
            sl = current_price + (atr * multiplier * 0.7)
        
        return {
            'symbol': symbol,
            'timeframe': main_tf,
            'signal': direction,
            'confidence': final_confidence,
            'base_confidence': base_confidence,
            'mtf_boost': mtf_boost,
            'entry': current_price,
            'tp1': tp1,
            'tp2': tp2,
            'tp3': tp3,
            'sl': sl,
            'atr': atr,
            'validation': {
                'htf_aligned': htf_aligned,
                'ltf_aligned': ltf_aligned,
                'htf': htf,
                'ltf': ltf
            },
            'analysis': main_analysis,
            'realistic_for_tf': True
        }

central_analyzer = CentralAIAnalyzer()
logger.info("✅ Central AI Analyzer initialized")
