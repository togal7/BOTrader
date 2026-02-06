with open('config.py', 'r') as f:
    content = f.read()

# Znajdź i zamień TIMEFRAMES (prosty string replace)
old = """TIMEFRAMES = {
    '1m': {'label': '1 minuta'},
    '5m': {'label': '5 minut'},
    '15m': {'label': '15 minut'},
    '30m': {'label': '30 minut'},
    '1h': {'label': '1 godzina'},
    '4h': {'label': '4 godziny'},
    '1d': {'label': '1 dzień'}
}"""

new = """TIMEFRAMES = {
    '1m': {'label': '1 minuta'},
    '5m': {'label': '5 minut'},
    '15m': {'label': '15 minut'},
    '30m': {'label': '30 minut'},
    '1h': {'label': '1 godzina'},
    '4h': {'label': '4 godziny'},
    '12h': {'label': '12 godzin'},
    '1d': {'label': '1 dzień'},
    '3d': {'label': '3 dni'},
    '5d': {'label': '5 dni'},
    '1w': {'label': '1 tydzień'},
    '2w': {'label': '2 tygodnie'},
    '1M': {'label': '1 miesiąc'},
    '3M': {'label': '3 miesiące'},
    '6M': {'label': '6 miesięcy'},
    '1Y': {'label': '1 rok'}
}"""

content = content.replace(old, new)

with open('config.py', 'w') as f:
    f.write(content)

print("✅ Fixed TIMEFRAMES in config.py")

