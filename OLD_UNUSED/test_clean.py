# Test clean
test_symbols = [
    'BTC/USDT:USDT',
    'ETH/USDT:USDT', 
    'ADA/USDT:USDT',
    'BYTE/USDT:USDT'
]

for s in test_symbols:
    clean = s.replace('/USDT:USDT', '')
    print(f"{s} → {clean}")

