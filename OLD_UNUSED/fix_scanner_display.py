with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== FIXING SCANNER DISPLAY ===\n")

# Znajdź handle_scan - sekcję z wyświetlaniem wyników
for i, line in enumerate(lines):
    # Szukaj linii gdzie formatuje wyniki (po "top_results = results[:10]")
    if 'for i, r in enumerate(top_results)' in line or 'for r in top_results' in line:
        print(f"Znaleziono formatowanie wyników w linii {i+1}")
        
        # Szukaj następnych 15 linii gdzie jest r['symbol']
        for j in range(i, min(i+15, len(lines))):
            if "r['symbol']" in lines[j] and 'text +=' in lines[j]:
                old_line = lines[j]
                
                # Dodaj display_symbol przed tą linią
                indent = '        '
                new_lines = [
                    f"{indent}display_symbol = r['symbol'].replace(':USDT', '')\n",
                    old_line.replace("r['symbol']", "display_symbol")
                ]
                
                lines[j:j+1] = new_lines
                print(f"✅ Dodano display_symbol w linii {j+1}")
                print(f"   OLD: {old_line.strip()}")
                print(f"   NEW: {new_lines[1].strip()}")
                break
        
        # Teraz znajdź callback (InlineKeyboardButton z analyze_)
        for j in range(i, min(i+20, len(lines))):
            if 'InlineKeyboardButton' in lines[j] and 'callback_data=' in lines[j]:
                old_line = lines[j]
                
                # Zamień callback z r['symbol'] na clean_symbol
                if "r['symbol']" in lines[j]:
                    # Dodaj clean_symbol przed buttonem
                    indent = '            '
                    clean_line = f"{indent}clean_symbol = r['symbol'].replace('/USDT:USDT', '').replace(':USDT', '')\n"
                    
                    # Zamień r['symbol'] w callback
                    new_button = old_line.replace("r['symbol']", "clean_symbol")
                    
                    lines[j:j+1] = [clean_line, new_button]
                    print(f"\n✅ Naprawiono callback w linii {j+1}")
                    print(f"   OLD: {old_line.strip()}")
                    print(f"   NEW: {new_button.strip()}")
                    break
        break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Scanner display fixed!")

