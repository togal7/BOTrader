with open('handlers.py', 'r') as f:
    lines = f.readlines()

changes = 0

for i, line in enumerate(lines):
    # Stary kod: replace('/USDT', '').replace('/', '')
    if "clean_symbol = r['symbol'].replace('/USDT', '').replace('/', '')" in line:
        # Zamień na nowy
        lines[i] = "            clean_symbol = r['symbol'].replace('/USDT:USDT', '')  # BTC/USDT:USDT → BTC\n"
        print(f"Line {i+1}: {line.strip()} → clean_symbol = r['symbol'].replace('/USDT:USDT', '')")
        changes += 1

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print(f"\n✅ Zmieniono {changes} linii")

