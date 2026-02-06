with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING DISPLAY WITH CORRECT STRUCTURE ===\n")

old = """        # Extract data CORRECTLY from central_analyzer
        signal_data = analysis.get('signal', {})
        
        # Signal is a DICT with direction, confidence, etc
        if isinstance(signal_data, dict):
            signal = signal_data.get('direction', 'NEUTRAL')
            signal_confidence = signal_data.get('confidence', 0)
            entry = signal_data.get('entry', 0)
            tp1 = signal_data.get('tp1', 0)
            sl = signal_data.get('sl', 0)
            reasons = signal_data.get('reasons', [])
        else:
            signal = str(signal_data)
            signal_confidence = 0
            entry = 0
            tp1 = 0
            sl = 0
            reasons = []
        
        # Get indicators
        rsi = analysis.get('rsi', 0)
        ema_20 = analysis.get('ema_20', 0)
        ema_50 = analysis.get('ema_50', 0)
        volume_ratio = analysis.get('volume_ratio', 0)
        
        signal_emoji = {
            'LONG': '🟢',
            'SHORT': '🔴',
            'NEUTRAL': '⚪'
        }.get(signal.upper(), '⚪')
        
        # Build CLEAN text
        text = f\"\"\"📊 ANALIZA: {symbol.split('/')[0]}
        
{signal_emoji} Sygnał: {signal}
🎯 Pewność: {signal_confidence}%

📈 Wskaźniki:
• RSI: {rsi:.1f}
• EMA 20: ${ema_20:.6f}
• EMA 50: ${ema_50:.6f}
• Volume: {volume_ratio:.2f}x

💰 Poziomy:
• Entry: ${entry:.6f}
• TP: ${tp1:.6f}
• SL: ${sl:.6f}

⏱ {timeframe} | 🌐 {exchange.upper()}"""

new = """        # Extract data CORRECTLY from central_analyzer structure
        signal_data = analysis.get('signal', {})
        technical = analysis.get('technical', {})
        volume = analysis.get('volume', {})
        sentiment = analysis.get('sentiment', {})
        
        # Signal info
        signal = signal_data.get('direction', 'NEUTRAL')
        signal_confidence = signal_data.get('confidence', 0)
        entry = signal_data.get('entry', 0)
        tp1 = signal_data.get('tp1', 0)
        sl = signal_data.get('sl', 0)
        reasons = signal_data.get('reasons', [])
        
        # Technical indicators
        price = technical.get('price', 0)
        rsi_data = technical.get('rsi', {})
        rsi = rsi_data.get('14', 0) if isinstance(rsi_data, dict) else 0
        
        ema_data = technical.get('ema', {})
        ema_21 = ema_data.get('21', 0) if isinstance(ema_data, dict) else 0
        ema_50 = ema_data.get('50', 0) if isinstance(ema_data, dict) else 0
        
        macd_data = technical.get('macd', {})
        macd = macd_data.get('macd', 0) if isinstance(macd_data, dict) else 0
        
        # Volume
        volume_ratio = volume.get('ratio', 0)
        buy_pressure = volume.get('buy_pressure', 0)
        
        # Sentiment
        sentiment_label = sentiment.get('label', '⚪ Neutral')
        
        signal_emoji = {
            'LONG': '🟢',
            'SHORT': '🔴',
            'NEUTRAL': '⚪'
        }.get(signal.upper(), '⚪')
        
        # Build CLEAN text
        text = f\"\"\"📊 ANALIZA: {symbol.split('/')[0]}
        
{signal_emoji} Sygnał: {signal}
🎯 Pewność: {signal_confidence}%
{sentiment_label}

💰 Cena: ${price:,.2f}

📈 Wskaźniki:
• RSI(14): {rsi:.1f}
• EMA(21): ${ema_21:,.2f}
• EMA(50): ${ema_50:,.2f}
• MACD: {macd:.2f}

📊 Volume: {volume_ratio:.2f}x
💹 Buy Pressure: {buy_pressure:.1f}%

💵 Poziomy:
• Entry: ${entry:,.4f}
• Take Profit: ${tp1:,.4f}
• Stop Loss: ${sl:,.4f}

⏱ {timeframe} | 🌐 {exchange.upper()}"""

content = content.replace(old, new)
print("✅ Fixed display with correct structure")

with open('handlers.py', 'w') as f:
    f.write(content)

