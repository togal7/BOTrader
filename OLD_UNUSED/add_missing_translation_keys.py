with open('languages.py', 'r') as f:
    content = f.read()

# Dodaj brakujące klucze przed zamykającym }
new_keys = """    'select_exchange': {
        'pl': 'WYBIERZ GIEŁDĘ', 'en': 'SELECT EXCHANGE', 'es': 'SELECCIONAR EXCHANGE',
        'de': 'BÖRSE WÄHLEN', 'fr': 'CHOISIR EXCHANGE', 'it': 'SELEZIONA EXCHANGE',
        'pt': 'SELECIONAR EXCHANGE', 'ru': 'ВЫБРАТЬ БИРЖУ', 'tr': 'BORSA SEÇ', 'zh': '选择交易所'
    },
    'available_exchanges': {
        'pl': 'Dostępne giełdy', 'en': 'Available exchanges', 'es': 'Exchanges disponibles',
        'de': 'Verfügbare Börsen', 'fr': 'Exchanges disponibles', 'it': 'Exchange disponibili',
        'pt': 'Exchanges disponíveis', 'ru': 'Доступные биржи', 'tr': 'Mevcut borsalar', 'zh': '可用交易所'
    },
"""

# Wstaw przed ostatni }
insert_point = content.rfind('}')
content = content[:insert_point] + new_keys + content[insert_point:]

with open('languages.py', 'w') as f:
    f.write(content)

print("✅ Added missing translation keys")

