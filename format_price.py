"""
Inteligentne formatowanie cen dla wszystkich nominałów
"""

def format_price(price, use_comma=True):
    """
    Format price intelligently based on size
    
    Args:
        price: float
        use_comma: bool - czy dodawać przecinki w dużych liczbach
    
    Returns:
        Formatted string
    """
    if price == 0:
        return "$0.00"
    
    # Duże liczby (>=1000): $89,612.30
    if price >= 1000:
        if use_comma:
            # Usuń .00 jeśli jest
            formatted = f"${price:,.2f}"
            if formatted.endswith('.00'):
                return formatted[:-3]
            return formatted
        else:
            return f"${price:.2f}"
    
    # Średnie (1-999): $156.45
    elif price >= 1:
        return f"${price:.2f}"
    
    # Małe (0.01-0.99): $0.45
    elif price >= 0.01:
        return f"${price:.2f}"
    
    # Bardzo małe (<0.01): $0.00002135
    else:
        # Pokaż do pierwszych 3 znaczących cyfr po zerach
        str_price = f"{price:.12f}"
        # Usuń trailing zera
        str_price = str_price.rstrip('0')
        # Jeśli kończy się na . - dodaj 0
        if str_price.endswith('.'):
            str_price += '0'
        return f"${str_price}"

