with open('bot.py', 'r') as f:
    lines = f.readlines()

print("Removing AlertScanner from bot.py...")

new_lines = []
skip_block = False

for i, line in enumerate(lines):
    line_num = i + 1
    
    # Skip AlertScanner import
    if 'AlertScanner' in line and 'import' in line:
        print(f"Line {line_num}: Removing import: {line.strip()}")
        new_lines.append('    # Alert scanning moved to alert_worker.py\n')
        continue
    
    # Skip AlertScanner initialization
    if 'scanner = AlertScanner' in line:
        print(f"Line {line_num}: Removing scanner init: {line.strip()}")
        new_lines.append('    # Alert Scanner now runs as separate process (alert_worker.py)\n')
        skip_block = True
        continue
    
    # Skip scanner.start()
    if skip_block and 'scanner.start()' in line:
        print(f"Line {line_num}: Removing scanner.start(): {line.strip()}")
        skip_block = False
        continue
    
    new_lines.append(line)

with open('bot.py', 'w') as f:
    f.writelines(new_lines)

print("✅ AlertScanner removed!")

