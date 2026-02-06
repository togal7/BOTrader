with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== REMOVING DUPLICATE ALERTS BUTTONS ===\n")

# Znajdź wszystkie linie z '🔔 Alerty'
found_indices = []
for i, line in enumerate(lines):
    if '🔔 Alerty' in line and 'callback_data' in line:
        found_indices.append(i)
        print(f"Found at line {i+1}: {line.strip()[:60]}")

# Usuń duplikaty (zostaw tylko pierwszy)
if len(found_indices) > 1:
    print(f"\n⚠️ Found {len(found_indices)} duplicates - removing extras")
    # Usuń od tyłu żeby indeksy się nie zmieniały
    for idx in reversed(found_indices[1:]):
        del lines[idx]
        print(f"✅ Removed duplicate at line {idx+1}")

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Fixed!")

