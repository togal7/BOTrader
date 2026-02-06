with open('exchange_api.py', 'r') as f:
    content = f.read()

# Znajdź blok get_ticker i zamień
import re
pattern = r'(async def get_ticker\(.*?\):\s*""".*?"""\s*try:.*?ex = self\.exchanges\.get\(exchange\).*?if not ex:.*?return None\s*)(ticker = ex\.fetch_ticker\(symbol\))'

def replace_ticker(match):
    before = match.group(1)
    return before + '# Konwertuj symbol futures do spot\n            symbol_for_api = symbol.replace(":USDT", "") if ":USDT" in symbol else symbol\n            ticker = ex.fetch_ticker(symbol_for_api)'

new_content = re.sub(pattern, replace_ticker, content, flags=re.DOTALL)

with open('exchange_api.py', 'w') as f:
    f.write(new_content)

print('✅ Naprawiono get_ticker')
