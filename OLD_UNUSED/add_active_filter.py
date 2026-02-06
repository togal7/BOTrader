with open('exchange_api.py', 'r') as f:
    content = f.read()

print("=== ADDING ACTIVE FILTER ===\n")

# W get_symbols, dodaj filtr active
# Znajdź gdzie dodaje symbole do listy

old_code = """                # For MEXC: check if it's linear perpetual
                if market.get('linear') and market.get('contract'):
                    symbols.append(symbol)"""

new_code = """                # For MEXC: check if it's linear perpetual AND active
                if market.get('linear') and market.get('contract'):
                    # Skip inactive contracts (TESLA, NVIDIA, stocks)
                    if not market.get('active', True):
                        continue
                    symbols.append(symbol)"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ Added active filter")
else:
    print("⚠️ Pattern not found, trying alternative...")
    
    # Szukaj linii z symbols.append
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Jeśli to linia tuż przed symbols.append
        if 'symbols.append(symbol)' in line and i > 0:
            # Sprawdź czy nie ma już filtra active
            if 'active' not in lines[i-1]:
                # Wstaw filtr PRZED append
                indent = len(line) - len(line.lstrip())
                new_lines.insert(-1, ' ' * indent + "if not market.get('active', True):")
                new_lines.insert(-1, ' ' * indent + "    continue")
                print(f"✅ Added active filter before line {i+1}")
    
    content = '\n'.join(new_lines)

with open('exchange_api.py', 'w') as f:
    f.write(content)

print("\n✅ Active filter added!")

