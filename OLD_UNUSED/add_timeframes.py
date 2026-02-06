with open('config.py', 'r') as f:
    content = f.read()

print("=== ADDING TIMEFRAMES ===\n")

# Znajdź TIMEFRAMES dict i dodaj nowe
old_timeframes = """TIMEFRAMES = {
    '1m': {'label': '1 minuta', 'value': '1m'},
    '5m': {'label': '5 minut', 'value': '5m'},
    '15m': {'label': '15 minut', 'value': '15m'},
    '30m': {'label': '30 minut', 'value': '30m'},
    '1h': {'label': '1 godzina', 'value': '1h'},
    '4h': {'label': '4 godziny', 'value': '4h'},
    '1d': {'label': '1 dzień', 'value': '1d'}
}"""

new_timeframes = """TIMEFRAMES = {
    '1m': {'label': '1 minuta', 'value': '1m'},
    '5m': {'label': '5 minut', 'value': '5m'},
    '15m': {'label': '15 minut', 'value': '15m'},
    '30m': {'label': '30 minut', 'value': '30m'},
    '1h': {'label': '1 godzina', 'value': '1h'},
    '4h': {'label': '4 godziny', 'value': '4h'},
    '12h': {'label': '12 godzin', 'value': '12h'},
    '1d': {'label': '1 dzień', 'value': '1d'},
    '3d': {'label': '3 dni', 'value': '3d'},
    '5d': {'label': '5 dni', 'value': '5d'},
    '1w': {'label': '1 tydzień', 'value': '1w'},
    '2w': {'label': '2 tygodnie', 'value': '2w'},
    '1M': {'label': '1 miesiąc', 'value': '1M'},
    '3M': {'label': '3 miesiące', 'value': '3M'},
    '6M': {'label': '6 miesięcy', 'value': '6M'},
    '1Y': {'label': '1 rok', 'value': '1Y'}
}"""

if old_timeframes in content:
    content = content.replace(old_timeframes, new_timeframes)
    print("✅ Added 9 new timeframes (12h, 3d, 5d, 1w, 2w, 1M, 3M, 6M, 1Y)")
else:
    print("⚠️ Pattern not found - trying manual")

with open('config.py', 'w') as f:
    f.write(content)

