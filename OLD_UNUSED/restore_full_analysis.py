with open('handlers.py', 'r') as f:
    content = f.read()

print("=== RESTORING FULL PROFESSIONAL ANALYSIS ===\n")

# Znajdź show_ai_analysis (profesjonalna wersja)
import re
match = re.search(r'(async def show_ai_analysis.*?)(?=\nasync def |\nclass )', content, re.DOTALL)

if match:
    full_analysis_function = match.group(1)
    print(f"✅ Znaleziono show_ai_analysis ({len(full_analysis_function)} znaków)")
    
    # Zamień analyze_from_alert na TAKI SAM format
    new_analyze = """async def analyze_from_alert(query, user_id, user, symbol, timeframe):
    \"\"\"Show FULL professional analysis (same as AI Signals)\"\"\"
    try:
        await query.answer()
        await query.edit_message_text('⏳ Analizuję...')
        
        exchange = user.get('selected_exchange', 'mexc')
        
        # Use the SAME function as AI Signals
        from central_ai_analyzer import central_analyzer
        analysis = await central_analyzer.analyze_pair_full(symbol, exchange, timeframe)
        
        if not analysis:
            await query.edit_message_text(
                f"❌ Nie udało się przeanalizować {symbol}",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_history')
                ]])
            )
            return
        
        # Format using show_ai_analysis style
        signal_data = analysis.get('signal', {})
        technical = analysis.get('technical', {})
        volume = analysis.get('volume', {})
        sentiment_data = analysis.get('sentiment', {})
        structure = analysis.get('structure', {})
        
        signal = signal_data.get('direction', 'NEUTRAL')
        confidence = signal_data.get('confidence', 0)
        entry = signal_data.get('entry', 0)
        tp1 = signal_data.get('tp1', 0)
        tp2 = signal_data.get('tp2', 0)
        tp3 = signal_data.get('tp3', 0)
        sl = signal_data.get('sl', 0)
        rr_ratio = signal_data.get('rr_ratio', 0)
        reasons = signal_data.get('reasons', [])
        
        price = technical.get('price', 0)
        rsi_data = technical.get('rsi', {})
        rsi = rsi_data.get('14', 0) if isinstance(rsi_data, dict) else 0
        
        ema_data = technical.get('ema', {})
        ema_9 = ema_data.get('9', 0)
        ema_21 = ema_data.get('21', 0)
        
        macd_data = technical.get('macd', {})
        macd = macd_data.get('macd', 0)
        
        change_24h = technical.get('change_24h', 0)
        
        volume_ratio = volume.get('ratio', 0)
        buy_pressure = volume.get('buy_pressure', 0)
        sell_pressure = volume.get('sell_pressure', 0)
        
        sentiment_label = sentiment_data.get('label', '⚪ Neutral')
        sentiment_score = sentiment_data.get('score', 0)
        sentiment_signals = sentiment_data.get('signals', [])
        
        support = structure.get('support', [])
        resistance = structure.get('resistance', [])
        
        # Signal emoji and text
        signal_emoji = {'LONG': '🟢', 'SHORT': '🔴', 'NEUTRAL': '⚪'}.get(signal, '⚪')
        signal_text = {'LONG': 'KUP', 'SHORT': 'SPRZEDAJ', 'NEUTRAL': 'CZEKAJ'}.get(signal, 'CZEKAJ')
        
        from datetime import datetime
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # BUILD FULL PROFESSIONAL TEXT (like AI Signals)
        text = f\"\"\"{'🟢' if signal == 'LONG' else '🔴' if signal == 'SHORT' else '⚪'} ANALIZA - {symbol.split('/')[0]}

==============================
🎯 SYGNAŁ: {signal_text} ({confidence}%)
==============================

💰 CENA: ${price:.6f}
📊 Zmiana 24h: {change_24h:+.2f}%
⏱ Timeframe: {timeframe} | 🌐 {exchange.upper()} | 🕐 {current_time}

🎯 POZIOMY TRADINGOWE:
\"\"\"
        
        if signal != 'NEUTRAL':
            text += f\"\"\"• Entry: ${entry:.6f}
• TP1 (33%): ${tp1:.6f} ({((tp1-entry)/entry*100):+.2f}%)
• TP2 (66%): ${tp2:.6f} ({((tp2-entry)/entry*100):+.2f}%)
• TP3 (100%): ${tp3:.6f} ({((tp3-entry)/entry*100):+.2f}%)
• Stop Loss: ${sl:.6f} ({((sl-entry)/entry*100):.2f}%)
• Risk/Reward: 1:{rr_ratio:.2f}
\"\"\"
        else:
            text += f\"\"\"⚠️ Brak wyraźnego kierunku - podajemy range:
• Cena: ${price:.6f}
• Upside target: ${tp1:.6f} ({((tp1-price)/price*100):+.2f}%)
• Downside target: ${tp2:.6f} ({((tp2-price)/price*100):.2f}%)

💡 Rekomendacja: Poczekaj na wyraźniejszy sygnał!
\"\"\"
        
        text += f\"\"\"

📈 SENTYMENT RYNKU:
{sentiment_label} ({sentiment_score}/100)

🔧 WSKAŹNIKI TECHNICZNE:
• RSI(14): {rsi:.1f}
• EMA(9): ${ema_9:.2f}
• EMA(21): ${ema_21:.2f}
• MACD: {macd:.2f}

📊 WOLUMEN:
• Ratio: {volume_ratio:.2f}x średniej
• Buying pressure: {buy_pressure:.0f}%
• Selling pressure: {sell_pressure:.0f}%
\"\"\"
        
        if support and resistance:
            text += f\"\"\"

📍 WSPARCIE/OPÓR:
• Wsparcie: ${support[0]:.4f}
• Opór: ${resistance[0]:.4f}
\"\"\"
        
        if reasons:
            text += f\"\"\"

🤖 ANALIZA AI:
\"\"\"
            for reason in reasons[:3]:
                text += f\"• {reason}\\n\"
        
        text += f\"\"\"

==============================
🤖 PODSUMOWANIE AI
==============================

📊 {signal_text} ({confidence}%). RSI na poziomie {rsi:.0f}. Cena wynosi ${price:.6f}.

==============================

⚠️ WAŻNE - ZASTRZEŻENIE PRAWNE:

Bot BOTrader dostarcza informacje edukacyjne. To NIE JEST porada finansowa.

Handel kryptowalutami wiąże się z wysokim ryzykiem.
• Nie gwarantujemy zysków ani trafności sygnałów
• Wszystkie decyzje na własną odpowiedzialność
• Zawsze przeprowadzaj własną analizę
• Inwestuj tylko środki, których utratę możesz zaakceptować

==============================
\"\"\"
        
        # Quick intervals at bottom
        intervals = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
        keyboard = []
        symbol_encoded = symbol.replace('/', '_').replace(':', '_')
        
        row = []
        for i, tf in enumerate(intervals):
            emoji_btn = '✅' if tf == timeframe else '⏱'
            row.append(InlineKeyboardButton(f'{emoji_btn} {tf}', callback_data=f'analyze_{symbol_encoded}_{tf}'))
            if len(row) == 3:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        
        keyboard.append([
            InlineKeyboardButton('📜 Historia', callback_data='alerts_history'),
            InlineKeyboardButton('🏠 Menu', callback_data='back_main')
        ])
        
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        
    except Exception as e:
        logger.error(f"Error in analyze_from_alert: {e}")
        import traceback
        traceback.print_exc()
        
        await query.edit_message_text(
            f"❌ Błąd: {e}",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_history')
            ]])
        )

"""
    
    # Zamień starą funkcję
    pattern = r'async def analyze_from_alert\(.*?\n(?=async def |class |# ====)'
    content = re.sub(pattern, new_analyze, content, flags=re.DOTALL)
    print("✅ Replaced analyze_from_alert with FULL analysis")
    
    with open('handlers.py', 'w') as f:
        f.write(content)
else:
    print("❌ Nie znaleziono show_ai_analysis")

