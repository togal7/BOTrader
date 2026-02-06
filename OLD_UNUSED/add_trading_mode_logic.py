"""
Add trading mode (confidence calculation) to ai_trader.py
"""

with open('ai_trader.py', 'r') as f:
    content = f.read()

print("=== ADDING TRADING MODE LOGIC ===\n")

import re

# 1. Znajdź funkcję calculate_confidence i dodaj parametr trading_mode
old_func = r'def calculate_confidence\(self, indicators\):'
new_func = 'def calculate_confidence(self, indicators, trading_mode=\'balanced\'):'

content = re.sub(old_func, new_func, content)
print("✅ Added trading_mode parameter to calculate_confidence")

# 2. Znajdź gdzie liczymy confidence z RSI i dodaj tryby
old_rsi = r'(# RSI contribution.*?if rsi_value < 30:.*?confidence \+= )(\d+)'

# Zastąp hardcoded wartości logiką trybów
rsi_logic = '''# RSI contribution
        rsi_value = indicators.get('rsi')
        if rsi_value:
            # Conservative: tylko ekstremalne wartości
            if trading_mode == 'conservative':
                if rsi_value < 25:
                    confidence += 30
                elif rsi_value > 75:
                    confidence += 30
                elif rsi_value < 30:
                    confidence += 15
                elif rsi_value > 70:
                    confidence += 15
            
            # Balanced: standard
            elif trading_mode == 'balanced':
                if rsi_value < 30:
                    confidence += 25
                elif rsi_value > 70:
                    confidence += 25
                elif rsi_value < 35:
                    confidence += 15
                elif rsi_value > 65:
                    confidence += 15
            
            # Aggressive: szeroki zakres, wyższe wartości
            elif trading_mode == 'aggressive':
                if rsi_value < 35:
                    confidence += 30
                elif rsi_value > 65:
                    confidence += 30
                elif rsi_value < 40:
                    confidence += 20
                elif rsi_value > 60:
                    confidence += 20
            
            # Old code removed - confidence += '''

# Bezpieczniej: dodaj nową sekcję przed starym kodem
# Znajdź RSI section i zastąp
pattern = r'# RSI contribution.*?(?=# EMA)'
if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, rsi_logic + '\n        ', content, flags=re.DOTALL)
    print("✅ Added trading mode logic to RSI scoring")

# 3. Dodaj multiplier na końcu funkcji
old_return = r'return min\(100, confidence\)'
new_return = '''# Apply trading mode multiplier
        if trading_mode == 'conservative':
            confidence = confidence * 0.95  # Ostrożnie
        elif trading_mode == 'aggressive':
            confidence = confidence * 1.15  # Odważnie!
        
        return min(100, int(confidence))'''

content = re.sub(old_return, new_return, content)
print("✅ Added trading mode multiplier")

# 4. Update wywołań calculate_confidence - dodaj trading_mode
# Znajdź wszystkie wywołania i dodaj parametr
pattern = r'confidence = self\.calculate_confidence\(indicators\)'
replacement = 'confidence = self.calculate_confidence(indicators, trading_mode)'

content = re.sub(pattern, replacement, content)
print("✅ Updated calculate_confidence calls")

# 5. Dodaj trading_mode do analyze_pair
old_analyze = r'async def analyze_pair\(self, symbol, exchange=\'mexc\', timeframe=\'15m\'\):'
new_analyze = 'async def analyze_pair(self, symbol, exchange=\'mexc\', timeframe=\'15m\', trading_mode=\'balanced\'):'

content = re.sub(old_analyze, new_analyze, content)
print("✅ Added trading_mode parameter to analyze_pair")

with open('ai_trader.py', 'w') as f:
    f.write(content)

print("\n✅ Trading mode logic added to ai_trader.py")

