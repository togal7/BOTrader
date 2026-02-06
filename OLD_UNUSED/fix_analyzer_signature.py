with open('central_ai_analyzer.py', 'r') as f:
    lines = f.readlines()

# Znajdź definicję
for i, line in enumerate(lines):
    if 'async def analyze_pair_full' in line:
        print(f"Znaleziono w linii {i+1}: {line.strip()}")
        
        # Zamień (sprawdź obecną)
        if 'exchange, symbol,' in line or 'exchange: str, symbol:' in line:
            # Stara kolejność: (exchange, symbol, timeframe)
            lines[i] = '    async def analyze_pair_full(self, symbol: str, exchange: str, timeframe: str = "15m", context: str = "general"):\n'
            print(f"✅ Zamieniono na: symbol, exchange, timeframe")
        break

with open('central_ai_analyzer.py', 'w') as f:
    f.writelines(lines)

