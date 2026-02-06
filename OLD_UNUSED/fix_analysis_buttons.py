with open('handlers.py', 'r') as f:
    content = f.read()

# ==========================================
# 1. Znajdź show_pair_analysis - przyciski w środku
# ==========================================

# Znajdź sekcję z przyciskami
old_buttons = """        # Buttons - context-aware back button
        clean_symbol = symbol.replace('/USDT:USDT', '').replace(':USDT', '').replace('/USDT', '')
        
        # Determine back button based on context
        if context == 'ai_signal':
            back_data = 'show_cached_scan'
            back_label = '⬅️ Wróć do sygnałów'
        elif context == 'scan_extreme':
            back_data = f'scan_{user.get("last_scan_type", "gainers")}'
            back_label = '⬅️ Wróć do skanera'
        elif context == 'search':
            back_data = 'back_main'
            back_label = '⬅️ Menu główne'
        else:
            back_data = 'back_main'
            back_label = '⬅️ Menu główne'
        
        keyboard = [
            [InlineKeyboardButton('🔄 Odśwież analizę', callback_data=f'analyze_{clean_symbol}_{timeframe}')],
            [
                InlineKeyboardButton('⏱ 15m', callback_data=f'analyze_{clean_symbol}_15m'),
                InlineKeyboardButton('⏱ 1h', callback_data=f'analyze_{clean_symbol}_1h'),
                InlineKeyboardButton('⏱ 4h', callback_data=f'analyze_{clean_symbol}_4h')
            ],
            [InlineKeyboardButton('📊 Więcej wskaźników', callback_data=f'details_{clean_symbol}_{timeframe}')],
            [InlineKeyboardButton(back_label, callback_data=back_data)]
        ]"""

# Nowe przyciski - tylko Odśwież i Powrót
new_buttons = """        # Buttons - context-aware back button
        
        # Determine back button based on context
        if context == 'ai_signal':
            back_data = 'show_cached_scan'
            back_label = '⬅️ Wróć do sygnałów'
        elif context == 'scan_extreme':
            back_data = f'scan_{user.get("last_scan_type", "gainers")}'
            back_label = '⬅️ Wróć do skanera'
        elif context == 'search':
            back_data = 'back_main'
            back_label = '⬅️ Menu główne'
        else:
            back_data = 'back_main'
            back_label = '⬅️ Menu główne'
        
        # Przycisk Odśwież używa PEŁNEGO symbolu (z :USDT)
        keyboard = [
            [InlineKeyboardButton('🔄 Odśwież analizę', callback_data=f'refresh_analysis_{symbol}_{timeframe}')],
            [InlineKeyboardButton(back_label, callback_data=back_data)]
        ]"""

content = content.replace(old_buttons, new_buttons)

print("✅ Usunięto przyciski interwałów i 'Więcej wskaźników'")

# ==========================================
# 2. Dodaj handler dla refresh_analysis
# ==========================================

# Znajdź miejsce na nowy callback
insert_before = """    elif data == 'show_cached_scan':
        await show_cached_scan(query, user_id, user)
        return"""

new_refresh = """
    
    elif data.startswith('refresh_analysis_'):
        # refresh_analysis_SYMBOL_TIMEFRAME
        parts = data.replace('refresh_analysis_', '').split('_')
        # Symbol może zawierać _ więc łączymy wszystko oprócz ostatniego
        timeframe = parts[-1]
        symbol = '_'.join(parts[:-1])
        exchange = user.get('selected_exchange', 'mexc').lower()
        
        # Symbol już ma pełny format (BTC/USDT:USDT)
        logger.info(f"refresh_analysis: {symbol}, tf={timeframe}")
        
        await show_pair_analysis(query, user_id, user, symbol, exchange, timeframe, 'ai_signal')
        return"""

content = content.replace(insert_before, new_refresh + '\n' + insert_before)

print("✅ Dodano handler refresh_analysis")

with open('handlers.py', 'w') as f:
    f.write(content)

