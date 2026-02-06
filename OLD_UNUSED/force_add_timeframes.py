with open('config.py', 'r') as f:
    lines = f.readlines()

# Znajdź TIMEFRAMES
for i, line in enumerate(lines):
    if "TIMEFRAMES = {" in line:
        print(f"Znaleziono TIMEFRAMES w linii {i+1}")
        
        # Znajdź koniec dict (})
        end_line = i
        for j in range(i, len(lines)):
            if '}' in lines[j] and 'TIMEFRAMES' not in lines[j]:
                end_line = j
                break
        
        # Nowy dict
        new_timeframes = [
            "TIMEFRAMES = {\n",
            "    '1m': {'label': '1 minuta'},\n",
            "    '5m': {'label': '5 minut'},\n",
            "    '15m': {'label': '15 minut'},\n",
            "    '30m': {'label': '30 minut'},\n",
            "    '1h': {'label': '1 godzina'},\n",
            "    '4h': {'label': '4 godziny'},\n",
            "    '12h': {'label': '12 godzin'},\n",
            "    '1d': {'label': '1 dzień'},\n",
            "    '3d': {'label': '3 dni'},\n",
            "    '5d': {'label': '5 dni'},\n",
            "    '1w': {'label': '1 tydzień'},\n",
            "    '2w': {'label': '2 tygodnie'},\n",
            "    '1M': {'label': '1 miesiąc'},\n",
            "    '3M': {'label': '3 miesiące'},\n",
            "    '6M': {'label': '6 miesięcy'},\n",
            "    '1Y': {'label': '1 rok'}\n",
            "}\n"
        ]
        
        # Zastąp stare nowym
        lines[i:end_line+1] = new_timeframes
        print(f"✅ Zastąpiono linie {i+1}-{end_line+1}")
        print(f"✅ Dodano 9 nowych interwałów")
        break

with open('config.py', 'w') as f:
    f.writelines(lines)

