with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== FIXING ALL 3 ISSUES ===\n")

# ==========================================
# FIX 1: Linia 1123 - zmień r['symbol'] na display_symbol
# ==========================================
print("1. Fixing line 1123 - display_symbol in label...")

for i, line in enumerate(lines):
    if i == 1122:  # Linia 1123 (0-indexed)
        if "r['symbol']" in line and "label = f" in line:
            old_line = line
            # Zmień r['symbol'] na display_symbol i confidence na int(score)
            new_line = line.replace(
                "r['symbol']", 
                "display_symbol"
            ).replace(
                "r['confidence']",
                "int(r.get('score', r.get('confidence', 50)))"
            ).replace(
                "%\"",
                "%~\""
            )
            lines[i] = new_line
            print(f"   ✅ Fixed line 1123:")
            print(f"      OLD: {old_line.strip()}")
            print(f"      NEW: {new_line.strip()}")
            break

# ==========================================
# FIX 2: Callback show_cached_scan - sprawdź linie 1131-1132
# ==========================================
print("\n2. Fixing callback 'Powrót'...")

for i, line in enumerate(lines):
    if "'⬅️ Powrót', callback_data='ai_signals'" in line:
        old_line = line
        new_line = line.replace("'ai_signals'", "'show_cached_scan'")
        lines[i] = new_line
        print(f"   ✅ Fixed callback at line {i+1}:")
        print(f"      OLD: {old_line.strip()}")
        print(f"      NEW: {new_line.strip()}")

# ==========================================
# FIX 3: Keyboard w show_pair_analysis (linia ~1286)
# ==========================================
print("\n3. Fixing interval buttons in show_pair_analysis...")

# Znajdź keyboard w show_pair_analysis
in_show_pair = False
keyboard_start = -1

for i, line in enumerate(lines):
    if 'async def show_pair_analysis' in line:
        in_show_pair = True
    
    if in_show_pair and 'keyboard = [' in line:
        keyboard_start = i
        
        # Sprawdź czy to keyboard z interwałami (następne 10 linii)
        has_intervals = False
        for j in range(i, min(i+10, len(lines))):
            if '15m' in lines[j] or '1h' in lines[j] or '4h' in lines[j]:
                has_intervals = True
                break
        
        if has_intervals:
            print(f"   Found keyboard with intervals at line {i+1}")
            
            # Znajdź koniec keyboard (zamykający ])
            keyboard_end = -1
            bracket_count = 0
            for j in range(i, len(lines)):
                if '[' in lines[j]:
                    bracket_count += lines[j].count('[')
                if ']' in lines[j]:
                    bracket_count -= lines[j].count(']')
                if bracket_count == 0 and j > i:
                    keyboard_end = j
                    break
            
            if keyboard_end > 0:
                # Przygotuj nowy keyboard - tylko Odśwież i Powrót
                indent = '        '
                new_keyboard = [
                    f"{indent}keyboard = [\n",
                    f"{indent}    [InlineKeyboardButton('🔄 Odśwież analizę', callback_data=f'refresh_analysis_{{symbol}}_{{timeframe}}')],\n",
                    f"{indent}    [InlineKeyboardButton(back_label, callback_data=back_data)]\n",
                    f"{indent}]\n"
                ]
                
                # Zastąp stary keyboard
                lines[keyboard_start:keyboard_end+1] = new_keyboard
                print(f"   ✅ Replaced keyboard (lines {keyboard_start+1}-{keyboard_end+1})")
                print(f"      Removed: interval buttons (15m, 1h, 4h) + 'Więcej wskaźników'")
            
            break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("\n✅ ALL FIXES APPLIED!")

