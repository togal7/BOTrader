"""
Integrate news aggregator with ai_trader.py
"""

with open('ai_trader.py', 'r') as f:
    content = f.read()

print("=== INTEGRATING NEWS WITH AI TRADER ===\n")

import re

# 1. Dodaj import na początku
if 'from news_aggregator import news_aggregator' not in content:
    # Znajdź ostatni import
    pattern = r'(import.*?\n\n)'
    replacement = r'\1from news_aggregator import news_aggregator\n\n'
    content = re.sub(pattern, replacement, content, count=1)
    print("✅ Added news_aggregator import")

# 2. Update analyze_pair - dodaj news analysis
old_analyze_pattern = r'(async def analyze_pair\(self.*?trading_mode.*?\):.*?)(# Get technical indicators)'

new_analyze_pattern = r'''\1
        # Get news sentiment for symbol
        try:
            symbol_base = symbol.split('/')[0] if '/' in symbol else symbol.split(':')[0]
            news_sentiment = await news_aggregator.get_aggregated_sentiment(symbol_base, hours=24)
        except Exception as e:
            logger.error(f"News aggregation error: {e}")
            news_sentiment = None
        
        \2'''

content = re.sub(old_analyze_pattern, new_analyze_pattern, content, flags=re.DOTALL)
print("✅ Added news sentiment fetching to analyze_pair")

# 3. Dodaj news do calculate_confidence
old_calc_pattern = r'(def calculate_confidence\(self, indicators, trading_mode.*?\):)'

new_calc_pattern = r'\1\n        news_sentiment = indicators.get(\'news_sentiment\')'

content = re.sub(old_calc_pattern, new_calc_pattern, content)
print("✅ Added news_sentiment parameter to calculate_confidence")

# 4. Dodaj news impact przed final multiplier
news_impact_code = '''
        # News sentiment impact
        if news_sentiment:
            news_impact = news_aggregator.calculate_confidence_impact(news_sentiment, trading_mode)
            confidence += news_impact
            logger.info(f"News impact ({trading_mode}): {news_impact:+d} -> Total: {confidence}")
        '''

# Wstaw przed "Apply trading mode multiplier"
pattern = r'(# Apply trading mode multiplier)'
replacement = news_impact_code + '\n        \\1'

content = re.sub(pattern, replacement, content)
print("✅ Added news sentiment impact to confidence calculation")

# 5. Przekaż news_sentiment do calculate_confidence
old_call = r'confidence = self\.calculate_confidence\(indicators, trading_mode\)'
new_call = '''# Add news sentiment to indicators for confidence calculation
        if news_sentiment:
            indicators['news_sentiment'] = news_sentiment
        
        confidence = self.calculate_confidence(indicators, trading_mode)'''

content = re.sub(old_call, new_call, content)
print("✅ Updated calculate_confidence call to include news")

# 6. Dodaj news info do zwracanego analysis dict
old_return_pattern = r"(return \{[^}]*'confidence': confidence,)"

new_return_pattern = r"""\1
            'news_sentiment': news_sentiment,"""

content = re.sub(old_return_pattern, new_return_pattern, content)
print("✅ Added news_sentiment to analysis result")

with open('ai_trader.py', 'w') as f:
    f.write(content)

print("\n✅ AI TRADER UPDATED WITH NEWS!")

