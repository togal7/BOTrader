with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING MULTIPLE TP LEVELS ===\n")

old = """        # Signal info
        signal = signal_data.get('direction', 'NEUTRAL')
        signal_confidence = signal_data.get('confidence', 0)
        entry = signal_data.get('entry', 0)
        tp1 = signal_data.get('tp1', 0)
        sl = signal_data.get('sl', 0)
        reasons = signal_data.get('reasons', [])"""

new = """        # Signal info
        signal = signal_data.get('direction', 'NEUTRAL')
        signal_confidence = signal_data.get('confidence', 0)
        entry = signal_data.get('entry', 0)
        tp1 = signal_data.get('tp1', 0)
        tp2 = signal_data.get('tp2', 0)
        tp3 = signal_data.get('tp3', 0)
        sl = signal_data.get('sl', 0)
        rr_ratio = signal_data.get('rr_ratio', 0)
        reasons = signal_data.get('reasons', [])"""

old_display = """💵 Poziomy:
• Entry: ${entry:,.4f}
• Take Profit: ${tp1:,.4f}
• Stop Loss: ${sl:,.4f}

⏱ {timeframe} | 🌐 {exchange.upper()}"""

new_display = """💵 Poziomy tradingowe:
• Entry: ${entry:,.6f}
• TP1: ${tp1:,.6f} (konserwatywny)
• TP2: ${analysis.get('signal', {}).get('tp2', 0):,.6f} (średni)
• TP3: ${analysis.get('signal', {}).get('tp3', 0):,.6f} (agresywny)
• Stop Loss: ${sl:,.6f}

⏱ {timeframe} | 🌐 {exchange.upper()}"""

new_text = """📊 ANALIZA: {symbol.split('/')[0]}
        
{signal_emoji} Sygnał: {signal}
🎯 Pewność: {signal_confidence}%
{sentiment_label}

💰 Cena: ${price:,.6f}

📈 Wskaźniki:
• RSI(14): {rsi:.1f}
• EMA(21): ${ema_21:,.6f}
• EMA(50): ${ema_50:,.6f}
• MACD: {macd:.2f}

📊 Volume: {volume_ratio:.2f}x
💹 Buy Pressure: {buy_pressure:.1f}%

💵 Poziomy tradingowe:
• Entry: ${entry:.6f}
• TP1 (33%): ${tp1:.6f}
• TP2 (66%): ${signal_data.get('tp2', 0):.6f}
• TP3 (100%): ${signal_data.get('tp3', 0):.6f}
• Stop Loss: ${sl:.6f}

⏱ {timeframe} | 🌐 {exchange.upper()}"""

content = content.replace(old, new)
print("✅ Added TP1, TP2, TP3")

with open('handlers.py', 'w') as f:
    f.write(content)

