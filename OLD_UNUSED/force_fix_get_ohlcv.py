with open('exchange_api.py', 'r') as f:
    lines = f.readlines()

# Znajdź linię z def get_ohlcv
for i, line in enumerate(lines):
    if 'async def get_ohlcv' in line:
        print(f"Znaleziono w linii {i+1}: {line.strip()}")
        # Zamień
        lines[i] = '    async def get_ohlcv(self, symbol: str, exchange: str, timeframe: str = "15m", limit: int = 100):\n'
        print(f"Zmieniono na: {lines[i].strip()}")
        break

with open('exchange_api.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Wymuszono poprawkę!")

