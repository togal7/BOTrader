with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== FIXING :USDT IN SCANNER RESULTS ===\n")

# Znajdź gdzie wyświetla wyniki skanera (po top_results = results[:10])
for i, line in enumerate(lines):
    if 'for i, r in enumerate(top_results)' in line:
        print(f"Znaleziono loop w linii {i+1}")
        
        # W następnych 10 liniach znajdź gdzie używa r['symbol']
        for j in range(i+1, min(i+15, len(lines))):
            if "text += f" in lines[j] and ("r['symbol']" in lines[j] or "display_symbol" in lines[j]):
                old_line = lines[j]
                
                # Sprawdź czy już ma display_symbol
                if "display_symbol" not in lines[j-1]:
                    # Dodaj display_symbol przed tą linią
                    indent = ' ' * (len(old_line) - len(old_line.lstrip()))
                    new_display = f"{indent}display_symbol = r['symbol'].replace(':USDT', '')\n"
                    lines.insert(j, new_display)
                    print(f"✅ Dodano display_symbol w linii {j+1}")
                
                # Zamień r['symbol'] na display_symbol w text
                if "r['symbol']" in lines[j+1]:
                    lines[j+1] = lines[j+1].replace("r['symbol']", "display_symbol")
                    print(f"✅ Zamieniono r['symbol'] → display_symbol w linii {j+2}")
                
                break
        break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Scanner display fixed!")

