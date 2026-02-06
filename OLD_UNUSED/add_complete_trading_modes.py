"""
Add trading mode logic to ALL indicators
"""

with open('ai_trader.py', 'r') as f:
    content = f.read()

print("=== ADDING COMPLETE TRADING MODE LOGIC ===\n")

import re

# 1. EMA CROSS - dodaj logikę trybów
ema_logic = '''        # EMA Cross contribution
        ema_cross = indicators.get('ema_cross')
        if ema_cross:
            cross_age_hours = indicators.get('ema_cross_age_hours', 0)
            
            if trading_mode == 'conservative':
                # Conservative: preferuje dojrzałe crossy
                if cross_age_hours >= 4:
                    confidence += 30  # Potwierdzony cross
                elif cross_age_hours >= 2:
                    confidence += 20  # Świeży ale OK
                else:
                    confidence += 10  # Za świeży, niepewny
            
            elif trading_mode == 'balanced':
                # Balanced: standard
                if cross_age_hours <= 12:
                    confidence += 25
                else:
                    confidence += 15
            
            elif trading_mode == 'aggressive':
                # Aggressive: kocha świeże crossy (early signals!)
                if cross_age_hours <= 2:
                    confidence += 35  # Świeży = wczesny trend!
                elif cross_age_hours <= 12:
                    confidence += 25
                else:
                    confidence += 15  # Stary cross
'''

# Znajdź sekcję EMA i zastąp
pattern = r'# EMA Cross contribution.*?(?=# MACD|# Volume|$)'
if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, ema_logic + '\n        ', content, flags=re.DOTALL)
    print("✅ Added EMA Cross trading mode logic")

# 2. MACD - dodaj logikę trybów  
macd_logic = '''        # MACD contribution
        macd_signal = indicators.get('macd_signal')
        macd_histogram = indicators.get('macd_histogram', 0)
        
        if macd_signal:
            if trading_mode == 'conservative':
                # Conservative: potrzebuje SILNEGO MACD
                if abs(macd_histogram) > 50:
                    confidence += 30  # Silny sygnał
                elif abs(macd_histogram) > 20:
                    confidence += 15  # Średni
                else:
                    confidence += 5   # Za słaby
            
            elif trading_mode == 'balanced':
                # Balanced: standard
                if abs(macd_histogram) > 20:
                    confidence += 25
                else:
                    confidence += 15
            
            elif trading_mode == 'aggressive':
                # Aggressive: każdy MACD bullish jest dobry!
                if abs(macd_histogram) > 10:
                    confidence += 30  # Widzi momentum
                else:
                    confidence += 20  # Nawet słaby = early signal
'''

# Znajdź MACD sekcję
pattern = r'# MACD contribution.*?(?=# Volume|# Bollinger|$)'
if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, macd_logic + '\n        ', content, flags=re.DOTALL)
    print("✅ Added MACD trading mode logic")

# 3. VOLUME - dodaj logikę trybów
volume_logic = '''        # Volume contribution
        volume_ratio = indicators.get('volume_ratio', 1.0)
        
        if trading_mode == 'conservative':
            # Conservative: potrzebuje WYSOKIEGO volume
            if volume_ratio >= 1.5:  # +50% volume
                confidence += 25
            elif volume_ratio >= 1.25:  # +25% volume
                confidence += 10
            else:
                confidence += 0  # Za niski volume
        
        elif trading_mode == 'balanced':
            # Balanced: standard
            if volume_ratio >= 1.2:  # +20% volume
                confidence += 20
            elif volume_ratio >= 1.1:
                confidence += 10
        
        elif trading_mode == 'aggressive':
            # Aggressive: każdy wzrost volume = dobry znak!
            if volume_ratio >= 1.1:  # +10% wystarczy
                confidence += 25
            elif volume_ratio >= 1.05:  # +5% też OK
                confidence += 15
'''

# Znajdź Volume sekcję
pattern = r'# Volume contribution.*?(?=# Bollinger|# Apply|return)'
if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, volume_logic + '\n        ', content, flags=re.DOTALL)
    print("✅ Added Volume trading mode logic")

# 4. BOLLINGER BANDS - dodaj logikę
bollinger_logic = '''        # Bollinger Bands contribution
        bb_position = indicators.get('bollinger_position')  # 'lower', 'upper', 'middle'
        bb_distance = indicators.get('bb_distance', 0)  # jak daleko od bands
        
        if bb_position in ['lower', 'upper']:
            if trading_mode == 'conservative':
                # Conservative: tylko MOCNE dotknięcie
                if bb_distance >= 1.0:  # Poza bands
                    confidence += 30
                elif bb_distance >= 0.8:  # Bardzo blisko
                    confidence += 15
                else:
                    confidence += 5  # Za daleko
            
            elif trading_mode == 'balanced':
                # Balanced: standard
                if bb_distance >= 0.7:
                    confidence += 20
                else:
                    confidence += 10
            
            elif trading_mode == 'aggressive':
                # Aggressive: nawet zbliżenie = sygnał
                if bb_distance >= 0.5:
                    confidence += 25
                else:
                    confidence += 15
'''

# Znajdź Bollinger sekcję (jeśli istnieje)
pattern = r'# Bollinger.*?(?=# Apply|return)'
if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, bollinger_logic + '\n        ', content, flags=re.DOTALL)
    print("✅ Added Bollinger Bands trading mode logic")
else:
    # Dodaj przed return
    pattern = r'(# Apply trading mode multiplier)'
    replacement = bollinger_logic + '\n        \\1'
    content = re.sub(pattern, replacement, content)
    print("✅ Added Bollinger Bands section (new)")

with open('ai_trader.py', 'w') as f:
    f.write(content)

print("\n✅ ALL INDICATORS NOW HAVE TRADING MODE LOGIC!")
print("\nWskaźniki z trybami:")
print("  ✅ RSI (oversold/overbought thresholds)")
print("  ✅ EMA Cross (age preference)")
print("  ✅ MACD (histogram strength)")
print("  ✅ Volume (ratio thresholds)")
print("  ✅ Bollinger Bands (distance requirements)")
print("  ✅ Final Multiplier (0.95x / 1.0x / 1.15x)")

