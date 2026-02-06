with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== FIXING START TEXT ===\n")

# Znajdź async def start_command
for i, line in enumerate(lines):
    if 'async def start_command' in line:
        print(f"Found start_command at line {i+1}")
        
        # Następne ~30 linii - znajdź text = 
        for j in range(i, min(i+50, len(lines))):
            if 'text = f"""' in lines[j] or 'text = """' in lines[j]:
                print(f"Found text at line {j+1}")
                
                # Zastąp następne ~15 linii (cały blok tekstu)
                new_text = [
                    '    text = f"""👋 Witaj w BOTrader!\n',
                    '\n',
                    'Status: {sub_status}\n',
                    '🆔 ID: {user_id}\n',
                    '\n',
                    '✨ Co możesz zrobić:\n',
                    '🔍 Analiza AI - szczegółowa analiza pary\n',
                    '📊 Skaner Ekstremów - wzrosty, spadki, RSI\n',
                    '🎯 Sygnały AI - automatyczne sygnały\n',
                    '🔔 Alerty - powiadomienia o okazjach\n',
                    '⚙️ Ustawienia - giełda, interwał, język"""\n'
                ]
                
                # Znajdź koniec bloku tekstu (następne """)
                end_idx = j
                for k in range(j+1, len(lines)):
                    if '"""' in lines[k] and 'text = ' not in lines[k]:
                        end_idx = k
                        break
                
                # Zastąp
                lines[j:end_idx+1] = new_text
                print(f"✅ Replaced lines {j+1} to {end_idx+1}")
                break
        break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Fixed!")

