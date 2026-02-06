with open('handlers.py', 'r') as f:
    content = f.read()

print("=== UNIVERSAL FIX FOR SCANNER :USDT ===\n")

# Znajdź handle_scan i napraw w JEDNYM miejscu
# Szukaj gdzie tworzy keyboard z buttonami

old_button_code = """        for i, r in enumerate(top_results):
            keyboard.append([InlineKeyboardButton(f\"{i+1}. {r['symbol']} | {r['change']:.2f}% | RSI: {r['rsi']:.1f}\", callback_data=f\"analyze_{r['symbol']}_{interval}\")]) """

# To nie zadziała bo może być różny format...
# Muszę znaleźć DOKŁADNY kod

# Lepiej: znajdź gdzie tworzy button i dodaj display_symbol RAZ
import re

# Pattern: for i, r in enumerate(top_results):
#             keyboard.append([InlineKeyboardButton(
pattern = r"(for i, r in enumerate\(top_results\):)\s+(keyboard\.append\(\[InlineKeyboardButton\(f\".*?r\['symbol'\])"

def replacer(match):
    loop_line = match.group(1)
    button_line = match.group(2)
    
    # Dodaj display_symbol i zamień w button
    new_code = f"""{loop_line}
            display_symbol = r['symbol'].replace(':USDT', '')
            {button_line.replace("r['symbol']", "display_symbol")}"""
    
    return new_code

if re.search(pattern, content):
    content = re.sub(pattern, replacer, content)
    print("✅ Naprawiono przez regex")
else:
    print("⚠️ Pattern nie pasuje, próbuję manualnie...")
    
    # Manual fix - znajdź for i, r in enumerate(top_results)
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Jeśli to jest for i, r in enumerate(top_results):
        if 'for i, r in enumerate(top_results)' in line:
            # Sprawdź następną linię - jeśli ma keyboard.append
            if i+1 < len(lines) and 'keyboard.append' in lines[i+1]:
                # Dodaj display_symbol PRZED keyboard.append
                indent = len(lines[i+1]) - len(lines[i+1].lstrip())
                display_line = ' ' * indent + "display_symbol = r['symbol'].replace(':USDT', '')"
                new_lines.append(display_line)
                print(f"✅ Dodano display_symbol po linii {i+1}")
                
                # Zamień r['symbol'] na display_symbol w następnych 2 liniach
                if i+2 < len(lines):
                    for j in range(i+1, min(i+4, len(lines))):
                        if "r['symbol']" in lines[j]:
                            lines[j] = lines[j].replace("r['symbol']", "display_symbol")
                            print(f"✅ Zamieniono w linii {j+1}")
    
    content = '\n'.join(new_lines)

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ Universal scanner fix applied!")

