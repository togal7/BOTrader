with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== MANUAL FIX - SCANNER MENU ===\n")

# Znajdź scan_extremes_menu (około linii 311)
for i, line in enumerate(lines):
    if 'async def scan_extremes_menu' in line:
        print(f"Znaleziono menu w linii {i+1}")
        
        # Znajdź przyciski (następne 20 linii)
        for j in range(i, min(i+30, len(lines))):
            # Zmień callback z 'scan_gainers' na 'scan_select_gainers'
            if "'scan_gainers'" in lines[j]:
                lines[j] = lines[j].replace("'scan_gainers'", "'scan_select_gainers'")
                print(f"✅ Fixed gainers in line {j+1}")
            
            if "'scan_losers'" in lines[j]:
                lines[j] = lines[j].replace("'scan_losers'", "'scan_select_losers'")
                print(f"✅ Fixed losers in line {j+1}")
            
            if "'scan_rsi_oversold'" in lines[j]:
                lines[j] = lines[j].replace("'scan_rsi_oversold'", "'scan_select_rsi_oversold'")
                print(f"✅ Fixed rsi_oversold in line {j+1}")
            
            if "'scan_rsi_overbought'" in lines[j]:
                lines[j] = lines[j].replace("'scan_rsi_overbought'", "'scan_select_rsi_overbought'")
                print(f"✅ Fixed rsi_overbought in line {j+1}")
            
            if "'scan_volume'" in lines[j]:
                lines[j] = lines[j].replace("'scan_volume'", "'scan_select_volume'")
                print(f"✅ Fixed volume in line {j+1}")
        
        break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Menu callbacks fixed!")

