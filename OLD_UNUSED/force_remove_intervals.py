with open('handlers.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip_next = 0

for i, line in enumerate(lines):
    if skip_next > 0:
        skip_next -= 1
        continue
    
    # Usuń linię z interwałami 15m, 1h, 4h
    if "InlineKeyboardButton('⏱ 15m'" in line:
        # Usuń tę linię i następne 3 (całą grupę przycisków interwałów)
        print(f"Usuwam linię {i+1}: {line.strip()}")
        skip_next = 3  # Pomiń następne 3 linie
        continue
    
    # Usuń linię "Więcej wskaźników"
    if "Więcej wskaźników" in line:
        print(f"Usuwam linię {i+1}: {line.strip()}")
        continue
    
    new_lines.append(line)

with open('handlers.py', 'w') as f:
    f.writelines(new_lines)

print(f"✅ Usunięto niepotrzebne przyciski")

