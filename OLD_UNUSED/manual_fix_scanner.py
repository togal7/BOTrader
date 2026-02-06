with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== MANUAL FIX ===\n")

# Znajdź for r in top_results: (linia ~423)
for i, line in enumerate(lines):
    if 'for r in top_results:' in line and i > 400:
        print(f"Znaleziono loop w linii {i+1}")
        
        # Dodaj display_symbol ZARAZ PO for
        if 'display_symbol' not in lines[i+1]:
            indent = '            '
            lines.insert(i+1, f'{indent}display_symbol = r["symbol"].replace(":USDT", "")\n')
            print(f"✅ Dodano display_symbol w linii {i+2}")
        
        # Zamień r['symbol'] na display_symbol w następnych 3 liniach
        for j in range(i+1, min(i+5, len(lines))):
            if "r['symbol']" in lines[j]:
                old = lines[j]
                lines[j] = lines[j].replace("r['symbol']", "display_symbol")
                print(f"✅ Zamieniono w linii {j+1}:")
                print(f"   OLD: {old.strip()}")
                print(f"   NEW: {lines[j].strip()}")
        break

# Zmień progi RSI: 30 → 20, 70 → 80
print("\n2. Changing RSI thresholds...")

for i, line in enumerate(lines):
    if 'rsi < 30' in line:
        lines[i] = line.replace('rsi < 30', 'rsi < 20')
        print(f"✅ Changed line {i+1}: rsi < 30 → rsi < 20")
    
    if 'rsi > 70' in line:
        lines[i] = line.replace('rsi > 70', 'rsi > 80')
        print(f"✅ Changed line {i+1}: rsi > 70 → rsi > 80")

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("\n✅ DONE!")

