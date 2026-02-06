with open('handlers.py', 'r') as f:
    lines = f.readlines()

# Linia 1553 (index 1552)
if len(lines) > 1552:
    line = lines[1552]
    print(f"Linia 1553: '{line}'")
    print(f"Spaces: {len(line) - len(line.lstrip())}")
    
    # Powinno być 12 spacji (3 poziomy wcięcia po 4)
    if 'clean_symbol' in line:
        lines[1552] = '            clean_symbol = r["symbol"].replace("/USDT:USDT", "")  # BTC/USDT:USDT → BTC\n'
        print("✅ Naprawiono indent (12 spacji)")

with open('handlers.py', 'w') as f:
    f.writelines(lines)

