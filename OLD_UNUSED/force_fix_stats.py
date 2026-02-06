with open('handlers.py', 'r') as f:
    lines = f.readlines()

# Znajdź admin_stats_menu (linia ~690)
for i, line in enumerate(lines):
    if 'async def admin_stats_menu' in line:
        print(f"Znaleziono w linii {i+1}")
        
        # Następne 5 linii - znajdź all_users = db.get_all_users()
        for j in range(i, min(i+10, len(lines))):
            if 'all_users = db.get_all_users()' in lines[j]:
                print(f"Znaleziono get_all_users w linii {j+1}")
                
                # Zamień następne 2 linie
                old_line = lines[j]
                
                # Nowe 3 linie
                indent = '    '
                new_lines = [
                    f'{indent}all_users_dict = db.get_all_users()\n',
                    f'{indent}all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict\n',
                ]
                
                # Zastąp
                lines[j:j+1] = new_lines
                print(f"✅ Zastąpiono w linii {j+1}")
                break
        break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("✅ Force fixed!")

