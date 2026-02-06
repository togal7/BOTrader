with open('alert_scanner.py', 'r') as f:
    lines = f.readlines()

print("=== FIXING SYNTAX ERROR ===\n")

# Znajdź linię 298
for i in range(295, 305):
    if i < len(lines):
        print(f"{i}: {lines[i].rstrip()}")

print("\nProblem: else bez if!")
print("Szukam niekompletnego bloku...\n")

# Znajdź i napraw
new_lines = []
skip_next_else = False

for i, line in enumerate(lines):
    # Jeśli to problematyczne else na linii 298
    if i == 297 and line.strip() == 'else:':
        print(f"❌ Usuwam błędne else na linii {i+1}")
        skip_next_else = True
        continue
    
    # Pomiń też następną linię (log wewnątrz else)
    if skip_next_else and 'logger.info' in line:
        print(f"❌ Usuwam następną linię: {line.strip()}")
        skip_next_else = False
        continue
    
    new_lines.append(line)

with open('alert_scanner.py', 'w') as f:
    f.writelines(new_lines)

print("\n✅ Fixed!")

