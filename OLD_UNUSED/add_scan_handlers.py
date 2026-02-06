with open('handlers.py', 'r') as f:
    lines = f.readlines()

# Znajdź elif data.startswith('scan_'): (linia 175)
for i, line in enumerate(lines):
    if "elif data.startswith('scan_'):" in line and i > 170 and i < 180:
        print(f"Znaleziono handler w linii {i+1}")
        
        # Zastąp następne 3 linie
        old_block_end = i + 3
        
        new_block = """    elif data.startswith('scan_select_'):
        # Wybór typu skanowania -> pokaż menu rozmiaru
        scan_type = data.replace('scan_select_', '')
        await scan_size_menu(query, user_id, user, scan_type)
        return
    
    elif data.startswith('scan_') and '_' in data and data != 'scan_extremes':
        # scan_TYPE_SIZE (np. scan_gainers_50)
        parts = data.replace('scan_', '').rsplit('_', 1)
        if len(parts) == 2:
            scan_type = f'scan_{parts[0]}'
            size_str = parts[1]
            size = int(size_str) if size_str.isdigit() else 9999
            await handle_scan(query, user_id, user, scan_type, size)
        return
"""
        
        # Usuń stare linie i wstaw nowe
        del lines[i:old_block_end]
        lines.insert(i, new_block)
        
        print(f"✅ Replaced handler block at line {i+1}")
        break

# Zmień definicję handle_scan
for i, line in enumerate(lines):
    if 'async def handle_scan(query, user_id, user, scan_type):' in line:
        lines[i] = 'async def handle_scan(query, user_id, user, scan_type, scan_size=50):\n'
        print(f"✅ Updated handle_scan signature at line {i+1}")
        break

# Dodaj limit w pętli
for i, line in enumerate(lines):
    if 'for symbol in list(futures_symbols):' in line and i > 330:
        # Dodaj limit PRZED pętlą
        indent = '        '
        new_lines = [
            f'{indent}scan_limit = min(scan_size, len(futures_symbols))\n',
            f'{indent}logger.info(f"Scanning {{scan_limit}}/{{len(futures_symbols)}} futures")\n',
            f'{indent}\n',
            f'{indent}for symbol in list(futures_symbols)[:scan_limit]:\n'
        ]
        
        lines[i:i+1] = new_lines
        print(f"✅ Added scan limit at line {i+1}")
        break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("\n✅ All handlers added!")

