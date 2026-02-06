with open('handlers.py', 'r') as f:
    content = f.read()

print("=== USING FULL ANALYSIS DATA ===\n")

# Znajdź i wymień wyświetlanie
old = """        # Format analysis result - BETTER extraction
        signal_data = analysis.get('signal', 'NEUTRAL')
        
        # Signal może być dict lub string
        if isinstance(signal_data, dict):
            signal = signal_data.get('direction', 'NEUTRAL')
        else:
            signal = str(signal_data) if signal_data else 'NEUTRAL'
        
        # Get all indicators - try multiple keys
        confidence = analysis.get('confidence', analysis.get('score', 0))
        rsi = analysis.get('rsi', analysis.get('rsi_14', 0))
        
        # Get more details
        macd = analysis.get('macd', {})
        ema_cross = analysis.get('ema_cross', 'N/A')
        volume_ratio = analysis.get('volume_ratio', 0)
        
        signal_emoji = {
            'LONG': '🟢',
            'SHORT': '🔴',
            'NEUTRAL': '⚪'
        }.get(signal.upper() if signal else 'NEUTRAL', '⚪')
        
        text = f\"\"\"📊 ANALIZA: {symbol.split('/')[0]}
        
{signal_emoji} Sygnał: {signal}
🎯 Pewność: {confidence}%
📈 RSI: {rsi:.1f}
📊 Volume: {volume_ratio:.1f}x
⏱ Interwał: {timeframe}
🌐 Giełda: {exchange.upper()}"""

new = """        # DEBUG: Print what we got
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

content = content.replace(old, new)
print("✅ Using full analysis data with DEBUG")

with open('handlers.py', 'w') as f:
    f.write(content)

