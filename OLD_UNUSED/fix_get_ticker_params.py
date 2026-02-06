with open('exchange_api.py', 'r') as f:
    content = f.read()

# Zamień definicję get_ticker (symbol first!)
old_def = """    async def get_ticker(self, exchange: str, symbol: str):
        \"\"\"Get ticker data\"\"\"
        try:
            ex = self.exchanges.get(exchange)"""

new_def = """    async def get_ticker(self, symbol: str, exchange: str):
        \"\"\"Get ticker data (symbol first for consistency)\"\"\"
        try:
            ex = self.exchanges.get(exchange)"""

content = content.replace(old_def, new_def)

with open('exchange_api.py', 'w') as f:
    f.write(content)

print("✅ Naprawiono get_ticker parametry!")

