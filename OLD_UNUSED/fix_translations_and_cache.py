with open('handlers.py', 'r') as f:
    content = f.read()

# ==========================================
# 1. PRZETŁUMACZ WSZYSTKIE reasons w signal['reasons']
# ==========================================

# Reasons pochodzą z central_ai_analyzer - tam są po angielsku
# Musimy je przetłumaczyć w format_analysis_report

# Znajdź sekcję z tłumaczeniami i dodaj WSZYSTKIE możliwe
old_reason_trans = """    reason_translations = {
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

new_reason_trans = """    reason_translations = {
        # Polskie (już przetłumaczone)
        'Niski RSI': {'pl': 'Niski RSI', 'en': 'Low RSI', 'it': 'RSI basso'},
        'Silny trend spadkowy': {'pl': 'Silny trend spadkowy', 'en': 'Strong downtrend', 'it': 'Forte trend ribassista'},
        'Presja sprzedaży': {'pl': 'Presja sprzedaży', 'en': 'Selling pressure', 'it': 'Pressione di vendita'},
        'Silny trend wzrostowy': {'pl': 'Silny trend wzrostowy', 'en': 'Strong uptrend', 'it': 'Forte trend rialzista'},
        'Presja kupna': {'pl': 'Presja kupna', 'en': 'Buying pressure', 'it': 'Pressione di acquisto'},
        
        # Angielskie (z central_analyzer)
        'Overbought': {'pl': 'Wykupienie', 'en': 'Overbought', 'it': 'Ipercomprato'},
        'Oversold': {'pl': 'Wyprzedanie', 'en': 'Oversold', 'it': 'Ipervenduto'},
        'High volume': {'pl': 'Wysoki wolumen', 'en': 'High volume', 'it': 'Alto volume'},
        'Low volume': {'pl': 'Niski wolumen', 'en': 'Low volume', 'it': 'Basso volume'},
        'Strong uptrend': {'pl': 'Silny trend wzrostowy', 'en': 'Strong uptrend', 'it': 'Forte trend rialzista'},
        'Strong downtrend': {'pl': 'Silny trend spadkowy', 'en': 'Strong downtrend', 'it': 'Forte trend ribassista'},
        'Buying pressure': {'pl': 'Presja kupna', 'en': 'Buying pressure', 'it': 'Pressione di acquisto'},
        'Selling pressure': {'pl': 'Presja sprzedaży', 'en': 'Selling pressure', 'it': 'Pressione di vendita'},
        'RSI indicates overbought, possible correction incoming': {
            'pl': 'RSI wskazuje wykupienie, możliwa korekta', 
            'en': 'RSI indicates overbought, possible correction incoming',
            'it': 'RSI indica ipercomprato, possibile correzione'
        },
        'RSI shows oversold conditions, potential bounce opportunity': {
            'pl': 'RSI wskazuje wyprzedanie, potencjalne odbicie',
            'en': 'RSI shows oversold conditions, potential bounce opportunity',
            'it': 'RSI mostra condizioni di ipervenduto, possibile rimbalzo'
        },
        'Downtrend remains intact on HTF': {
            'pl': 'Trend spadkowy utrzymuje się na wyższych interwałach',
            'en': 'Downtrend remains intact on HTF',
            'it': 'Trend ribassista rimane intatto su HTF'
        },
        'Uptrend confirmed on multiple timeframes': {
            'pl': 'Trend wzrostowy potwierdzony na wielu interwałach',
            'en': 'Uptrend confirmed on multiple timeframes',
            'it': 'Trend rialzista confermato su più timeframe'
        },
    }"""

content = content.replace(old_reason_trans, new_reason_trans)

# Zmień logikę tłumaczenia - szukaj po całym tekście, nie tylko kluczach
old_translate_logic = """    text += f\"\"\"🤖 {reasoning_labels.get(lang, 'ANALIZA AI')}:
\"""
    for reason in signal['reasons'][:5]:
        # Try to translate
        translated = reason
        for key, trans in reason_translations.items():
            if key in reason:
                translated = trans.get(lang, reason)
                break
        text += f"• {translated}\\n\""""

new_translate_logic = """    text += f\"\"\"🤖 {reasoning_labels.get(lang, 'ANALIZA AI')}:
\"""
    for reason in signal['reasons'][:5]:
        # Translate - sprawdź dokładne dopasowanie lub fragmenty
        translated = reason
        
        # Najpierw sprawdź dokładne dopasowanie
        if reason in reason_translations:
            translated = reason_translations[reason].get(lang, reason)
        else:
            # Sprawdź czy zawiera któryś klucz
            for key, trans in reason_translations.items():
                if key.lower() in reason.lower():
                    translated = trans.get(lang, reason)
                    break
        
        text += f"• {translated}\\n\""""

content = content.replace(old_translate_logic, new_translate_logic)

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Poprawiono tłumaczenia!")

# ==========================================
# 2. PROBLEM Z CACHE - sprawdź czy zapisuje
# ==========================================

# Sprawdź czy mamy funkcję zapisującą cache
if 'cached_scan_results' in content:
    print("✅ Cache save code istnieje")
else:
    print("❌ BRAK cache save code!")

# Sprawdź czy jest log
if 'Cached' in content and 'results for user' in content:
    print("✅ Cache log istnieje")
else:
    print("⚠️ Brak cache log")

