"""
Upgrade AI prompts to make it the world's best trader
"""

with open('ai_trader.py', 'r') as f:
    content = f.read()

print("=== UPGRADING AI PROMPTS ===\n")

import re

# 1. Dodaj SYSTEM PROMPT (nowy)
system_prompt = '''
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
'''

# Dodaj na początku klasy AITrader
pattern = r'(class AITrader:.*?def __init__)'
replacement = system_prompt + '\n\n\\1'
content = re.sub(pattern, replacement, content, flags=re.DOTALL, count=1)
print("✅ Added SYSTEM_PROMPT")

# 2. Zastąp prosty prompt zaawansowanym
old_analyze = r'async def analyze_with_deepseek\(self, symbol, data\):.*?prompt = f"Analyze.*?"\n'

new_analyze = '''async def analyze_with_deepseek(self, symbol, data, indicators, news_sentiment=None, trading_mode='balanced'):
        """DeepSeek analysis with comprehensive prompt"""
        try:
            # Build comprehensive prompt based on trading mode
            mode_instructions = {
                'conservative': """CONSERVATIVE MODE: Be extremely cautious.
- Only recommend BUY/SELL if confidence ≥ 85%
- Require STRONG confirmation from multiple indicators
- Negative news = major red flag (reduce confidence 20-30%)
- Prefer mature signals over early trends
- Focus on risk mitigation""",
                
                'balanced': """BALANCED MODE: Provide moderate risk/reward analysis.
- Recommend BUY/SELL if confidence ≥ 70%
- Require majority of indicators to agree (3/5+)
- News should support or be neutral
- Balance early signals with confirmation
- Standard risk management""",
                
                'aggressive': """AGGRESSIVE MODE: Focus on EARLY signals and high potential.
- Recommend BUY/SELL if confidence ≥ 60%
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
            bb_distance = indicators.get('bb_distance', 0)
            
            # News info
            news_info = ""
            if news_sentiment:
                fg = news_sentiment.get('fear_greed', {})
                fg_val = fg.get('value', 50) if fg else 50
                fg_class = fg.get('classification', 'Neutral') if fg else 'Neutral'
                
                overall = news_sentiment.get('overall_sentiment', 'neutral')
                pos_pct = news_sentiment.get('positive_pct', 0)
                neg_pct = news_sentiment.get('negative_pct', 0)
                
                top_news = news_sentiment.get('top_news', [])
                headlines = "\\n".join([f"   • {n['title'][:60]}" for n in top_news[:3]])
                
                news_info = f"""
NEWS SENTIMENT (24h):
• Fear & Greed Index: {fg_val}/100 ({fg_class})
• Overall sentiment: {overall.upper()}
• Positive: {pos_pct}% | Negative: {neg_pct}%
• Key headlines:
{headlines}"""
            else:
                news_info = "NEWS SENTIMENT: No data available"
            
            # Build comprehensive prompt
            prompt = f"""ANALYSIS TASK:
Symbol: {symbol}
Current Price: ${price}

{mode_instructions.get(trading_mode, mode_instructions['balanced'])}

TECHNICAL INDICATORS:
• RSI: {rsi:.1f} (oversold <30, overbought >70)
• EMA Cross: {"YES - " + ("FRESH" if ema_age < 2 else "MATURE") if ema_cross else "NO"} (age: {ema_age:.1f}h)
• MACD: {macd_signal} (histogram: {macd_hist:.2f})
• Volume: {volume_ratio:.2f}x average (1.0 = normal)
• Bollinger Bands: Price at {bb_position} (distance: {bb_distance:.2f})

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

            # Call DeepSeek API
            message = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500
            )
'''

# Zastąp starą funkcję
pattern = r'async def analyze_with_deepseek\(self, symbol, data\):.*?(?=async def [a-z_]+\(|    def [a-z_]+\()'
content = re.sub(pattern, new_analyze, content, flags=re.DOTALL, count=1)
print("✅ Replaced analyze_with_deepseek with advanced version")

# 3. Update wywołania w analyze_pair
old_call = r'deepseek_result = await self\.analyze_with_deepseek\(symbol, data\)'
new_call = 'deepseek_result = await self.analyze_with_deepseek(symbol, data, indicators, news_sentiment, trading_mode)'

content = re.sub(old_call, new_call, content)
print("✅ Updated analyze_with_deepseek call")

with open('ai_trader.py', 'w') as f:
    f.write(content)

print("\n✅ AI PROMPTS UPGRADED!")
print("\nChanges:")
print("  • Added SYSTEM_PROMPT (elite trader persona)")
print("  • Mode-specific instructions (conservative/balanced/aggressive)")
print("  • Comprehensive data (all indicators + news)")
print("  • Structured output format enforced")
print("  • Specific requirements (price targets, probabilities, timeframes)")

