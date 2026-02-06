with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING SIGNAL DICT PROPERLY ===\n")

old = """        # DEBUG: Print what we got
        logger.info(f"Analysis result keys: {list(analysis.keys())}")
        logger.info(f"Analysis: {analysis}")
        
        # Extract data from central_analyzer format
        signal = analysis.get('signal', 'NEUTRAL')
        confidence = analysis.get('confidence', 0)
        rsi = analysis.get('rsi', 0)
        
        # Additional indicators
        ema_20 = analysis.get('ema_20', 0)
        ema_50 = analysis.get('ema_50', 0)
        volume_ratio = analysis.get('volume_ratio', 0)
        macd_data = analysis.get('macd', {})
        
        signal_emoji = {
            'LONG': '🟢',
            'SHORT': '🔴',
            'NEUTRAL': '⚪'
        }.get(str(signal).upper(), '⚪')
        
        # Build detailed text
        text = f\"\"\"📊 ANALIZA: {symbol.split('/')[0]}
        
{signal_emoji} Sygnał: {signal}
🎯 Pewność: {confidence}%

📈 Wskaźniki:
• RSI: {rsi:.1f}
• EMA 20: ${ema_20:.4f}
• EMA 50: ${ema_50:.4f}
• Volume: {volume_ratio:.2f}x

⏱ Interwał: {timeframe}
🌐 Giełda: {exchange.upper()}"""

new = """        # Extract data CORRECTLY from central_analyzer
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

content = content.replace(old, new)
print("✅ Fixed signal dict extraction")

with open('handlers.py', 'w') as f:
    f.write(content)

