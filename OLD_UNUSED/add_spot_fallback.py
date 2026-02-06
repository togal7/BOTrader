with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING FUTURES → SPOT FALLBACK ===\n")

# Znajdź miejsce gdzie próbujemy fallback timeframes i dodaj PRZED nim fallback na SPOT
old_fallback = """        if not analysis:
            # SMART FALLBACK - próbuj inne timeframe'y jeśli brak danych
            fallback_timeframes = ['15m', '1h', '4h', '1d']"""

new_fallback = """        if not analysis:
            # STEP 1: Jeśli FUTURES nie działa, spróbuj SPOT (ta sama para może być starsza na spot)
            if exchange == 'mexc' and ':USDT' in symbol:
                # To jest FUTURES, spróbuj SPOT
                spot_symbol = symbol.replace(':USDT', '')  # BTC/USDT:USDT → BTC/USDT
                logger.info(f"Futures failed, trying SPOT: {spot_symbol}")
                
                try:
                    analysis = await central_analyzer.analyze_pair_full(
                        exchange=exchange,
                        symbol=spot_symbol,
                        timeframe=timeframe,
                        context=context
                    )
                    
                    if analysis:
                        analysis['fallback_info'] = {
                            'original_market': 'FUTURES',
                            'used_market': 'SPOT',
                            'original_symbol': symbol,
                            'used_symbol': spot_symbol,
                            'reason': f"⚠️ Para {symbol} jest nowa na FUTURES lub brak danych.\\n✅ Znaleziono dane na rynku SPOT."
                        }
                        symbol = spot_symbol  # Update symbol dla display
                except Exception as e:
                    logger.error(f"SPOT fallback failed: {e}")
            
            # STEP 2: Jeśli nadal brak analizy, próbuj inne timeframe'y
            if not analysis:
                # SMART FALLBACK - próbuj inne timeframe'y jeśli brak danych
                fallback_timeframes = ['15m', '1h', '4h', '1d']"""

content = content.replace(old_fallback, new_fallback)
print("✅ Added FUTURES → SPOT fallback (Step 1)")

# Teraz update display logic dla fallback_info
old_fallback_display = """    # Check if fallback was used
    fallback_info = analysis.get('fallback_info')
    fallback_warning = ""
    
    if fallback_info:
        fallback_warning = f\"\"\"
⚠️ ZMIANA INTERWAŁU:
{fallback_info['reason']}

✅ Użyto zamiast: {fallback_info['used_tf']}

═══════════════════════════════════
\"\"\""""

new_fallback_display = """    # Check if fallback was used
    fallback_info = analysis.get('fallback_info')
    fallback_warning = ""
    
    if fallback_info:
        # Check if it's market fallback (FUTURES → SPOT) or timeframe fallback
        if 'used_market' in fallback_info:
            # Market fallback
            fallback_warning = f\"\"\"
📍 ZMIANA RYNKU:
{fallback_info['reason']}

🔄 {fallback_info['original_market']} → {fallback_info['used_market']}
📊 Symbol: {fallback_info['used_symbol']}

═══════════════════════════════════
\"\"\"
        elif 'used_tf' in fallback_info:
            # Timeframe fallback
            fallback_warning = f\"\"\"
⚠️ ZMIANA INTERWAŁU:
{fallback_info['reason']}

✅ Użyto zamiast: {fallback_info['used_tf']}

═══════════════════════════════════
\"\"\""""

content = content.replace(old_fallback_display, new_fallback_display)
print("✅ Updated fallback display logic")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ DONE!")
print("\nTERAZ:")
print("1. Bot próbuje FUTURES (jeśli wybrane)")
print("2. Jeśli brak danych → próbuje SPOT tej samej pary")
print("3. Jeśli nadal brak → próbuje inne timeframe'y")
print("4. Wyjaśnia użytkownikowi co i dlaczego zmienił")

