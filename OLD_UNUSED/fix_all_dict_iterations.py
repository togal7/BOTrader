with open('alert_scanner.py', 'r') as f:
    lines = f.readlines()

print("=== FIXING ALL DICT ITERATIONS ===\n")

changed = 0
for i, line in enumerate(lines):
    # Znajdź wszystkie .items() bez list()
    if '.items():' in line and 'list(' not in line and 'for ' in line:
        # Dodaj list()
        old_line = line
        # Znajdź .items()
        line = line.replace('.items():', 'list(TEMP).items():')
        # Znajdź nazwę dicta
        import re
        match = re.search(r'for .* in (\w+)\.items\(\):', old_line)
        if match:
            dict_name = match.group(1)
            line = line.replace('list(TEMP)', f'list({dict_name}')
            lines[i] = line
            changed += 1
            print(f"Line {i+1}: {old_line.strip()[:60]}")
            print(f"      → {line.strip()[:60]}\n")

with open('alert_scanner.py', 'w') as f:
    f.writelines(lines)

print(f"✅ Changed {changed} iterations")

