"""
Quick Timeframe Buttons - dodaje przyciski pod każdą analizą
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_quick_timeframe_buttons(symbol, exchange, current_timeframe=None):
    """
    Generuje przyciski do szybkiej analizy na innych interwałach
    
    Args:
        symbol: Para np. 'BTC/USDT'
        exchange: Giełda np. 'mexc'
        current_timeframe: Aktualny timeframe (będzie disabled)
    
    Returns:
        InlineKeyboardMarkup z przyciskami
    """
    
    # Wszystkie dostępne timeframes
    timeframes = ['1m', '5m', '15m', '30m', '1h', '2h', '4h', '12h', '1d', '3d', '5d', '1w', '2w']
    
    # Symbol do callback (replace / with _)
    safe_symbol = symbol.replace('/', '_')
    
    # Buduj keyboard w rows
    keyboard = []
    
    # Row 1: Minuty
    row1 = []
    for tf in ['1m', '5m', '15m', '30m']:
        if tf == current_timeframe:
            row1.append(InlineKeyboardButton(f"• {tf} •", callback_data="noop"))
        else:
            row1.append(InlineKeyboardButton(tf, callback_data=f"analyze_{safe_symbol}_{exchange}_{tf}"))
    keyboard.append(row1)
    
    # Row 2: Godziny (krótkie)
    row2 = []
    for tf in ['1h', '2h', '4h']:
        if tf == current_timeframe:
            row2.append(InlineKeyboardButton(f"• {tf} •", callback_data="noop"))
        else:
            row2.append(InlineKeyboardButton(tf, callback_data=f"analyze_{safe_symbol}_{exchange}_{tf}"))
    keyboard.append(row2)
    
    # Row 3: Godziny (długie)
    row3 = []
    for tf in ['12h', '1d', '3d']:
        if tf == current_timeframe:
            row3.append(InlineKeyboardButton(f"• {tf} •", callback_data="noop"))
        else:
            row3.append(InlineKeyboardButton(tf, callback_data=f"analyze_{safe_symbol}_{exchange}_{tf}"))
    keyboard.append(row3)
    
    # Row 4: Tygodnie
    row4 = []
    for tf in ['5d', '1w', '2w']:
        if tf == current_timeframe:
            row4.append(InlineKeyboardButton(f"• {tf} •", callback_data="noop"))
        else:
            row4.append(InlineKeyboardButton(tf, callback_data=f"analyze_{safe_symbol}_{exchange}_{tf}"))
    keyboard.append(row4)
    
    # Row 5: Back button
    keyboard.append([
        InlineKeyboardButton("« Powrót", callback_data=f"pair_menu_{safe_symbol}_{exchange}")
    ])
    
    return InlineKeyboardMarkup(keyboard)

