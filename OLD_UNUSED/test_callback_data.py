# Symuluj callback data
test_data = [
    'ai_sig_BNB_30m',
    'ai_sig_ETH_30m',
    'ai_sig_BTC_15m'
]

for data in test_data:
    parts = data.replace('ai_sig_', '').split('_')
    base = parts[0]
    timeframe = parts[1] if len(parts) > 1 else '15m'
    
    # Jak w kodzie
    symbol = base + '/USDT:USDT'
    
    print(f"{data} → base={base}, symbol={symbol}")

