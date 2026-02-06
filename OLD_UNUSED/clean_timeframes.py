with open('config.py', 'r') as f:
    lines = f.readlines()

# Znajdź TIMEFRAMES i usuń wszystko do końca bloku + śmieci
new_lines = []
skip = False
timeframes_done = False

for i, line in enumerate(lines):
    if 'TIMEFRAMES = {' in line and not timeframes_done:
        skip = True
        new_lines.append(line)
        continue
    
    if skip and not timeframes_done:
        new_lines.append(line)
        # Jeśli to zamykający } z '1Y'
        if "'1Y'" in line and '}' in lines[i+1] if i+1 < len(lines) else False:
            new_lines.append(lines[i+1])  # Dodaj }
            skip = False
            timeframes_done = True
            continue
    
    if not skip:
        new_lines.append(line)

with open('config.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Cleaned")

