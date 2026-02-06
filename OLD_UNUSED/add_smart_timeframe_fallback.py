with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING SMART TIMEFRAME FALLBACK ===\n")

# Znajdź show_pair_analysis i dodaj logikę fallback
old_error_handling = """        if not analysis:
            await query.edit_message_text(
                f"❌ Nie udało się przeanalizować {symbol}","""

new_error_handling = """        if not analysis:
            # SMART FALLBACK - próbuj inne timeframe'y jeśli brak danych
            fallback_timeframes = ['15m', '1h', '4h', '1d']
            
            # Usuń aktualny timeframe z fallback
            if timeframe in fallback_timeframes:
                fallback_timeframes.remove(timeframe)
            
            # Próbuj alternatywne timeframe'y
            for alt_tf in fallback_timeframes:
                logger.info(f"Trying fallback timeframe: {alt_tf}")
                analysis = await central_analyzer.analyze_pair_full(
                    exchange=exchange,
                    symbol=symbol,
                    timeframe=alt_tf,
                    context=context
                )
                
                if analysis:
                    # SUKCES - wyjaśnij użytkownikowi
                    reason = ""
                    if timeframe in ['1m', '3m', '5m']:
                        reason = f"⚠️ Zbyt krótki interwał ({timeframe}) - para może być nowa lub brak wystarczających danych."
                    elif timeframe in ['1w', '1M']:
                        reason = f"⚠️ Zbyt długi interwał ({timeframe}) - para może nie mieć wystarczającej historii."
                    else:
                        reason = f"⚠️ Brak danych dla interwału {timeframe} - para może być nowa lub nieaktywna."
                    
                    # Dodaj info na początku analizy
                    analysis['fallback_info'] = {
                        'original_tf': timeframe,
                        'used_tf': alt_tf,
                        'reason': reason
                    }
                    
                    timeframe = alt_tf  # Update dla dalszej części
                    break
            
            if not analysis:
                await query.edit_message_text(
                    f"❌ Nie udało się przeanalizować {symbol}\\n\\n"
                    f"Próbowano interwałów: {timeframe}, {', '.join(fallback_timeframes)}\\n\\n"
                    f"Możliwe przyczyny:\\n"
                    f"• Para zbyt nowa (brak historii)\\n"
                    f"• Nieaktywna para (brak wolumenu)\\n"
                    f"• Problem z giełdą\\n\\n"
                    f"Spróbuj innej pary lub giełdy.","""

content = content.replace(old_error_handling, new_error_handling)
print("✅ Added smart fallback logic")

# Teraz dodaj wyświetlanie info o fallback w format_analysis_report
# Znajdź początek format_analysis_report
old_report_start = """def format_analysis_report(analysis, lang='pl'):
    \"\"\"Format analysis into beautiful Telegram message\"\"\"
    
    signal = analysis['signal']"""

new_report_start = """def format_analysis_report(analysis, lang='pl'):
    \"\"\"Format analysis into beautiful Telegram message\"\"\"
    
    # Check if fallback was used
    fallback_info = analysis.get('fallback_info')
    fallback_warning = ""
    
    if fallback_info:
        fallback_warning = f\"\"\"
⚠️ ZMIANA INTERWAŁU:
{fallback_info['reason']}

✅ Użyto zamiast: {fallback_info['used_tf']}

═══════════════════════════════════
\"\"\"
    
    signal = analysis['signal']"""

content = content.replace(old_report_start, new_report_start)
print("✅ Added fallback warning display")

# Dodaj fallback_warning do final text
old_final = """    text = f\"\"\"
⚪ SYGNAŁ AI - {signal['symbol']}

{direction_emoji} {direction_label}"""

new_final = """    text = f\"\"\"{fallback_warning}
⚪ SYGNAŁ AI - {signal['symbol']}

{direction_emoji} {direction_label}"""

content = content.replace(old_final, new_final)
print("✅ Added fallback warning to output")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ DONE!")

