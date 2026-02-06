with open('exchange_api.py', 'r') as f:
    content = f.read()

print("=== FILTERING ONLY ACTIVE FUTURES ===\n")

# W get_symbols, po sprawdzeniu market['linear']
old_check = """                # For MEXC: check if it's linear perpetual
                if market.get('linear') and market.get('contract'):
                    symbols.append(symbol)"""

new_check = """                # For MEXC: check if it's linear perpetual AND active
                if market.get('linear') and market.get('contract') and market.get('active', True):
                    symbols.append(symbol)"""

if old_check in content:
    content = content.replace(old_check, new_check)
    print("✅ Added 'active' filter")
else:
    print("⚠️ Pattern not found, trying alternative...")
    
    # Alternatywnie - znajdź gdzie dodaje symbol
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Jeśli to linia z market.get('linear')
        if "market.get('linear')" in line and "symbols.append" in lines[i+1] if i+1 < len(lines) else False:
            # Dodaj and market.get('active', True)
            new_lines[-1] = line.replace(
                "market.get('contract'):",
                "market.get('contract') and market.get('active', True):"
            )
            print(f"✅ Added active filter in line {i+1}")
    
    content = '\n'.join(new_lines)

with open('exchange_api.py', 'w') as f:
    f.write(content)

print("✅ Exchange API now filters only ACTIVE futures!")

