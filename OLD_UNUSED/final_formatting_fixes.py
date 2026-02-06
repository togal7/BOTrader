with open('handlers.py', 'r') as f:
    content = f.read()

# ==========================================
# 1. Przenieś Timeframe/Exchange/Time pod cenę
# ==========================================

# Znajdź obecną strukturę
old_structure = """💰 CENA: ${technical['price']:.6f}
📊 Zmiana 24h: {technical['change_24h']:+.2f}%

{reco_text}"""

new_structure = """💰 CENA: ${technical['price']:.6f}
📊 Zmiana 24h: {technical['change_24h']:+.2f}%
⏱ Timeframe: {analysis['timeframe']} | 🌐 {analysis['exchange'].upper()} | 🕐 {datetime.now().strftime('%H:%M:%S')}

{reco_text}"""

content = content.replace(old_structure, new_structure)

# Usuń stary timeframe/exchange z końca (przed podsumowaniem)
old_footer = """    text += f\"\"\"
⏱ Timeframe: {analysis['timeframe']}
🌐 Exchange: {analysis['exchange'].upper()}
🕐 {datetime.now().strftime('%H:%M:%S')}

{'='*30}"""

new_footer = """    text += f\"\"\"
{'='*30}"""

content = content.replace(old_footer, new_footer)

# ==========================================
# 2. Przetłumacz reasons w AI Reasoning
# ==========================================

# Dodaj import datetime jeśli brak
if 'from datetime import datetime' not in content:
    content = 'from datetime import datetime\n' + content

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Poprawiono formatowanie!")

# ==========================================
# 3. Dodaj tłumaczenia reasons
# ==========================================

with open('handlers.py', 'r') as f:
    content = f.read()

# Znajdź sekcję z reason_translations i dodaj więcej
old_translations = """    reason_translations = {
        'oversold_signal': {'pl': 'Sygnał wyprzedania', 'en': 'Oversold signal'},
        'Low RSI': {'pl': 'Niski RSI', 'en': 'Low RSI'},
        'Strong downtrend': {'pl': 'Silny trend spadkowy', 'en': 'Strong downtrend'},
        'Selling pressure': {'pl': 'Presja sprzedaży', 'en': 'Selling pressure'},
        'Strong uptrend': {'pl': 'Silny trend wzrostowy', 'en': 'Strong uptrend'},
        'Buying pressure': {'pl': 'Presja kupna', 'en': 'Buying pressure'},
        'Volume spike': {'pl': 'Skok wolumenu', 'en': 'Volume spike'},
        'High volatility': {'pl': 'Wysoka zmienność', 'en': 'High volatility'},
    }"""

new_translations = """    reason_translations = {
        'oversold_signal': {'pl': 'Sygnał wyprzedania', 'en': 'Oversold signal'},
        'Low RSI': {'pl': 'Niski RSI', 'en': 'Low RSI'},
        'Niski RSI': {'pl': 'Niski RSI', 'en': 'Low RSI'},
        'Strong downtrend': {'pl': 'Silny trend spadkowy', 'en': 'Strong downtrend'},
        'Silny trend spadkowy': {'pl': 'Silny trend spadkowy', 'en': 'Strong downtrend'},
        'Selling pressure': {'pl': 'Presja sprzedaży', 'en': 'Selling pressure'},
        'Presja sprzedaży': {'pl': 'Presja sprzedaży', 'en': 'Selling pressure'},
        'Strong uptrend': {'pl': 'Silny trend wzrostowy', 'en': 'Strong uptrend'},
        'Buying pressure': {'pl': 'Presja kupna', 'en': 'Buying pressure'},
        'Volume spike': {'pl': 'Skok wolumenu', 'en': 'Volume spike'},
        'High volatility': {'pl': 'Wysoka zmienność', 'en': 'High volatility'},
    }"""

content = content.replace(old_translations, new_translations)

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Dodano tłumaczenia!")

