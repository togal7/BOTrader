with open('handlers.py', 'r') as f:
    content = f.read()

# Znajdź TYLKO ai_scan_execute - linia z "for r in results[:10]:"
import re

# 1. Napraw kafelki w ai_scan_execute
pattern1 = r'(for r in results\[:10\]:\s+emoji = .*?else "🔴"\s+)clean_symbol = r\[\'symbol\'\]\.replace\(\'/USDT\', \'\'\)\.replace\(\'/\', \'\'\)'

replacement1 = r'\1clean_symbol = r["symbol"].replace("/USDT:USDT", "")'

content = re.sub(pattern1, replacement1, content)

# 2. Dodaj display_symbol po clean_symbol
pattern2 = r'(clean_symbol = r\["symbol"\]\.replace\("/USDT:USDT", ""\)\s+)(label =)'

replacement2 = r'\1display_symbol = r["symbol"].replace(":USDT", "")\n            \2'

content = re.sub(pattern2, replacement2, content)

# 3. Zmień label aby używał display_symbol
content = content.replace(
    'label = f"{emoji} {r[\'symbol\']} | {r[\'signal\']} {r[\'confidence\']}%"',
    'label = f"{emoji} {display_symbol} | {r[\'signal\']} {int(r.get(\'score\', r.get(\'confidence\', 50)))}pts"'
)

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Naprawiono handlers.py od zera")

