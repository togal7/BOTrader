import asyncio
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from chart_generator import chart_gen

async def test():
    # Generate realistic OHLCV data
    dates = pd.date_range(end=datetime.now(), periods=100, freq='1h')
    
    base = 95000
    prices = []
    for i in range(100):
        noise = np.random.randn() * 100
        prices.append(base + noise + i * 5)
    
    df = pd.DataFrame({
        'open': [p + np.random.randn() * 50 for p in prices],
        'high': [p + abs(np.random.randn() * 100) for p in prices],
        'low': [p - abs(np.random.randn() * 100) for p in prices],
        'close': prices,
        'volume': [1000000 + np.random.randn() * 100000 for _ in range(100)],
    }, index=dates)
    
    print("📊 Generating chart...")
    
    # Generate chart
    img = await chart_gen.generate_signal_chart(
        symbol='BTC/USDT',
        timeframe='1h',
        ohlcv_data=df,
        entry_price=95500,
        position_type='LONG',
        tp_levels=[96000, 97000, 98000],
        sl_price=94500,
        liquidation_price=93000,
    )
    
    # Save
    with open('test_chart.png', 'wb') as f:
        f.write(img)
    
    print("✅ Chart saved: test_chart.png")
    import os
    print(f"   Size: {os.path.getsize('test_chart.png') / 1024:.1f} KB")

asyncio.run(test())
