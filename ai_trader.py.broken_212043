"""
AI Trading Analysis with DeepSeek API
"""

import os
import logging
import requests
from config import DEEPSEEK_API_KEY, PERPLEXITY_API_KEY

logger = logging.getLogger(__name__)

class AITrader:
    """AI-powered trading analysis using DeepSeek"""
    
    SYSTEM_PROMPT = """You are an elite cryptocurrency trading analyst with 15+ years of experience.

Your expertise:
- Pattern recognition (chart patterns, candlestick formations)
- Multi-indicator synthesis (RSI, EMA, MACD, Volume, Bollinger Bands)
- Market psychology and sentiment analysis
- News impact assessment
- Risk-reward optimization
- Multi-timeframe analysis

Your track record: 78% accuracy in price movement predictions.

Your goal: Provide ACTIONABLE predictions for cryptocurrency price movements with:
- Specific price targets and probabilities
- Precise time windows (not vague "soon")
- Clear stop-loss levels
- Risk factor identification
- Multi-indicator reasoning

You MUST provide concrete, measurable predictions that can be verified."""

    def __init__(self, deepseek_key=None, perplexity_key=None):
        # Use provided keys, fall back to config
        self.deepseek_key = deepseek_key or DEEPSEEK_API_KEY
        self.perplexity_key = perplexity_key or PERPLEXITY_API_KEY
        
        if self.deepseek_key:
            logger.info("✅ DeepSeek API key loaded")
        else:
            logger.warning("⚠️ DeepSeek API key not found")
    
    async def analyze_with_deepseek(self, symbol, data, indicators, news_sentiment=None, trading_mode='balanced'):
        """DeepSeek analysis with comprehensive prompt"""
        
        if not self.deepseek_key:
            logger.warning("DeepSeek API key missing")
            return None
        
        try:
            # Mode-specific instructions
            mode_instructions = {
                'conservative': """CONSERVATIVE MODE: Be extremely cautious.
- Only recommend BUY/SELL if confidence >= 85%
- Require STRONG confirmation from multiple indicators
- Negative news = major red flag (reduce confidence 20-30%)
- Prefer mature signals over early trends
- Focus on risk mitigation""",
                
                'balanced': """BALANCED MODE: Provide moderate risk/reward analysis.
- Recommend BUY/SELL if confidence >= 70%
- Require majority of indicators to agree (3/5+)
- News should support or be neutral
- Balance early signals with confirmation
- Standard risk management""",
                
                'aggressive': """AGGRESSIVE MODE: Focus on EARLY signals and high potential.
- Recommend BUY/SELL if confidence >= 60%
- Early trend detection is VALUABLE
- Negative news often = buying opportunity (ignore FUD)
- High volume + momentum = strong signal
- Focus on upside potential"""
            }
            
            # Extract data
            price = data.get('last', 0)
            rsi = indicators.get('rsi', 50)
            ema_cross = indicators.get('ema_cross', False)
            ema_age = indicators.get('ema_cross_age_hours', 0)
            macd_signal = indicators.get('macd_signal', 'neutral')
            macd_hist = indicators.get('macd_histogram', 0)
            volume_ratio = indicators.get('volume_ratio', 1.0)
            bb_position = indicators.get('bollinger_position', 'middle')
            
            # News info - simple version
            news_info = "NEWS SENTIMENT: No data available"
            if news_sentiment:
                fg = news_sentiment.get('fear_greed', {})
                if fg:
                    fg_val = fg.get('value', 50)
                    fg_class = fg.get('classification', 'Neutral')
                    overall = news_sentiment.get('overall_sentiment', 'neutral')
                    pos_pct = news_sentiment.get('positive_pct', 0)
                    neg_pct = news_sentiment.get('negative_pct', 0)
                    
                    news_info = f"NEWS SENTIMENT (24h): Fear & Greed {fg_val}/100 ({fg_class}), Overall {overall.upper()}, Positive {pos_pct}%, Negative {neg_pct}%"
            
            # Build comprehensive prompt
            ema_status = "FRESH Golden Cross" if ema_cross and ema_age < 2 else "Mature Golden Cross" if ema_cross else "No cross"
            
            user_prompt = f"""ANALYSIS TASK:
Symbol: {symbol}
Current Price: ${price}

{mode_instructions.get(trading_mode, mode_instructions['balanced'])}

TECHNICAL INDICATORS:
- RSI: {rsi:.1f} (oversold <30, overbought >70)
- EMA Cross: {ema_status} (age: {ema_age:.1f}h)
- MACD: {macd_signal} (histogram: {macd_hist:.2f})
- Volume: {volume_ratio:.2f}x average (1.0 = normal)
- Bollinger Bands: Price at {bb_position}

{news_info}

REQUIRED OUTPUT FORMAT:
1. Direction: [BUY/SELL/HOLD]
2. Confidence: [number 0-100]
3. Price Target 1: $X (probability Y%, timeframe: Z minutes)
4. Price Target 2: $X (probability Y%, timeframe: Z minutes)
5. Stop Loss: $X
6. Valid Until: [X hours from now]
7. Key Risks: [list 2-3 specific risks]
8. Reasoning: [2-3 sentences with specific indicator references]

Be SPECIFIC with numbers, times, and probabilities. NO vague language."""

            # Call DeepSeek API (OpenAI-compatible)
            headers = {
                'Authorization': f'Bearer {self.deepseek_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': 'deepseek-chat',
                'messages': [
                    {'role': 'system', 'content': self.SYSTEM_PROMPT},
                    {'role': 'user', 'content': user_prompt}
                ],
                'max_tokens': 500,
                'temperature': 0.7
            }
            
            logger.info(f"🤖 Calling DeepSeek API for {symbol}...")
            
            response = requests.post(
                'https://api.deepseek.com/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"DeepSeek API error: {response.status_code} - {response.text}")
                return None
            
            result = response.json()
            response_text = result['choices'][0]['message']['content']
            
            logger.info(f"✅ DeepSeek response received ({len(response_text)} chars)")
            
            # Parse response
            signal = 'HOLD'
            confidence = 50
            
            if 'BUY' in response_text.upper() and 'SELL' not in response_text.upper()[:100]:
                signal = 'BUY'
            elif 'SELL' in response_text.upper():
                signal = 'SELL'
            
            # Extract confidence
            import re
            conf_match = re.search(r'Confidence:\s*(\d+)', response_text)
            if conf_match:
                confidence = int(conf_match.group(1))
            
            return {
                'signal': signal,
                'confidence': confidence,
                'reason': response_text[:200],
                'analysis': response_text
            }
            
        except Exception as e:
            logger.error(f"DeepSeek API error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def analyze_with_perplexity(self, symbol):
        """Perplexity market context"""
        try:
            headers = {
                'Authorization': f'Bearer {self.perplexity_key}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'llama-3.1-sonar-small-128k-online',
                'messages': [{'role': 'user', 'content': f'Market news for {symbol}'}]
            }
            response = requests.post(
                'https://api.perplexity.ai/chat/completions',
                headers=headers,
                json=data,
                timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                return {'market_context': result['choices'][0]['message']['content'][:300]}
        except Exception as e:
            logger.error(f"Perplexity error: {e}")
        return None
    
    async def get_ai_analysis(self, symbol, data, indicators, news_sentiment=None, trading_mode='balanced'):
        """Combined AI analysis"""
        deepseek_result = await self.analyze_with_deepseek(symbol, data, indicators, news_sentiment, trading_mode)
        perplexity_result = await self.analyze_with_perplexity(symbol)
        
        if not deepseek_result and not perplexity_result:
            return {
                'signal': 'WAIT',
                'confidence': 0,
                'reason': 'Brak danych AI',
                'analysis': 'AI unavailable'
            }
        
        if deepseek_result:
            result = deepseek_result
            if perplexity_result:
                result['market_context'] = perplexity_result.get('market_context', '')
            return result
        
        return perplexity_result

# Global instance
ai_trader = AITrader()
logger.info("✅ AI Trader initialized with DeepSeek API")

