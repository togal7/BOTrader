with open('config.py', 'r') as f:
    lines = f.readlines()

print("=== FIXING DUPLICATE TIMEFRAMES ===\n")

# Znajdź OBA TIMEFRAMES i usuń pierwszy (stary format bez 'label')
first_tf = -1
second_tf = -1

for i, line in enumerate(lines):
    if 'TIMEFRAMES = {' in line:
        if first_tf == -1:
            first_tf = i
            print(f"First TIMEFRAMES at line {i+1}")
        else:
            second_tf = i
            print(f"Second TIMEFRAMES at line {i+1}")
            break

if first_tf >= 0 and second_tf >= 0:
    # Usuń pierwszy blok (od first_tf do zamykającego })
    end_first = first_tf
    for i in range(first_tf, len(lines)):
        if '}' in lines[i] and 'TIMEFRAMES' not in lines[i]:
            end_first = i
            break
    
    print(f"Removing lines {first_tf+1} to {end_first+1}")
    del lines[first_tf:end_first+1]
    
    print("✅ Removed old TIMEFRAMES")

# Teraz dodaj nowe interwały do pozostałego TIMEFRAMES
new_lines = []
in_timeframes = False

for i, line in enumerate(new_lines if new_lines else lines):
    if 'TIMEFRAMES = {' in line:
        in_timeframes = True
        new_lines.append(line)
        continue
    
    if in_timeframes and '}' in line:
        # Wstaw nowe przed }
        new_lines.append("    '12h': {'label': '12 godzin'},\n")
        new_lines.append("    '3d': {'label': '3 dni'},\n")
        new_lines.append("    '5d': {'label': '5 dni'},\n")
        new_lines.append("    '1w': {'label': '1 tydzień'},\n")
        new_lines.append("    '2w': {'label': '2 tygodnie'},\n")
        new_lines.append("    '1M': {'label': '1 miesiąc'},\n")
        new_lines.append("    '3M': {'label': '3 miesiące'},\n")
        new_lines.append("    '6M': {'label': '6 miesięcy'},\n")
        new_lines.append("    '1Y': {'label': '1 rok'}\n")
        new_lines.append(line)
        in_timeframes = False
        print("✅ Added 9 new timeframes")
        continue
    
    new_lines.append(line)

# Jeśli nie przetwarzaliśmy jeszcze (bo lines zostały wcześniej nadpisane)
if not new_lines:
    new_lines = lines

with open('config.py', 'w') as f:
    f.writelines(new_lines)

print("\n✅ Fixed!")

