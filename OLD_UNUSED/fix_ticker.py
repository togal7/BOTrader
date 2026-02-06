with open('exchange_api.py', 'r') as f:
    lines = f.readlines()

# Znajdź linię z "ticker = ex.fetch_ticker(symbol)"
for i, line in enumerate(lines):
    if 'ticker = ex.fetch_ticker(symbol)' in line:
        # Zamień tę linię na poprawioną wersję
        indent = line[:len(line) - len(line.lstrip())]
        lines[i] = f'{indent}# Konwertuj symbol futures do spot\n{indent}            symbol_for_api = symbol.replace(":USDT", "") if ":USDT" in symbol else symbol\n{indent}            ticker = ex.fetch_ticker(symbol_for_api)\n'
        print(f'✅ Naprawiono linię {i+1}')
        break

with open('exchange_api.py', 'w') as f:
    f.writelines(lines)
