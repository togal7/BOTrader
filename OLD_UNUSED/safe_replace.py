with open('config.py', 'r') as f:
    content = f.read()

# Czytaj nowy dict
with open('/tmp/new_timeframes.txt', 'r') as f:
    new_dict = f.read()

# Znajdź stary TIMEFRAMES
import re
pattern = r"TIMEFRAMES = \{[^}]+\}"
content = re.sub(pattern, new_dict.strip(), content, count=1)

with open('config.py', 'w') as f:
    f.write(content)

print("✅ Replaced")

