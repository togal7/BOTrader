"""
Timeframe Validator - sprawdza czy giełda obsługuje dany interwał
"""

import logging

logger = logging.getLogger(__name__)

# Timeframes obsługiwane przez każdą giełdę
SUPPORTED_TIMEFRAMES = {
    'mexc': ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M'],
    'binance': ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '12h', '1d', '3d', '1w', '1M'],
    'bybit': ['1m', '3m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']
}

# Fallback timeframes (najpopularniejsze, obsługiwane wszędzie)
UNIVERSAL_TIMEFRAMES = ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M']

def is_timeframe_supported(exchange, timeframe):
    """
    Sprawdza czy giełda obsługuje dany timeframe
    
    Args:
        exchange: Nazwa giełdy ('mexc', 'binance', 'bybit')
        timeframe: Interwał czasowy (np. '3m', '12h')
    
    Returns:
        bool: True jeśli obsługiwany
    """
    exchange = exchange.lower()
    
    if exchange not in SUPPORTED_TIMEFRAMES:
        logger.warning(f"Unknown exchange: {exchange}, assuming support")
        return True
    
    return timeframe in SUPPORTED_TIMEFRAMES[exchange]

def get_fallback_timeframe(exchange, timeframe):
    """
    Zwraca najbliższy obsługiwany timeframe dla giełdy
    
    Args:
        exchange: Nazwa giełdy
        timeframe: Nieobsługiwany timeframe
    
    Returns:
        str: Najbliższy obsługiwany timeframe
    """
    exchange = exchange.lower()
    
    if exchange not in SUPPORTED_TIMEFRAMES:
        return '1h'  # Default fallback
    
    supported = SUPPORTED_TIMEFRAMES[exchange]
    
    # Mapowanie na minuty dla porównania
    timeframe_to_minutes = {
        '1m': 1, '3m': 3, '5m': 5, '15m': 15, '30m': 30,
        '1h': 60, '4h': 240, '12h': 720,
        '1d': 1440, '3d': 4320, '5d': 7200,
        '1w': 10080, '1M': 43200, '6M': 259200, '1Y': 525600
    }
    
    target_minutes = timeframe_to_minutes.get(timeframe, 60)
    
    # Znajdź najbliższy obsługiwany
    closest = min(supported, key=lambda x: abs(timeframe_to_minutes.get(x, 60) - target_minutes))
    
    return closest

def get_supported_timeframes_message(exchange):
    """
    Zwraca ładny message z obsługiwanymi timeframes
    
    Args:
        exchange: Nazwa giełdy
    
    Returns:
        str: Sformatowana wiadomość
    """
    exchange = exchange.lower()
    
    if exchange not in SUPPORTED_TIMEFRAMES:
        return "Obsługiwane interwały: standardowe"
    
    supported = SUPPORTED_TIMEFRAMES[exchange]
    
    # Grupuj
    minutes = [tf for tf in supported if 'm' in tf and len(tf) <= 3]
    hours = [tf for tf in supported if 'h' in tf]
    days = [tf for tf in supported if 'd' in tf]
    weeks = [tf for tf in supported if 'w' in tf]
    months = [tf for tf in supported if 'M' in tf]
    
    parts = []
    if minutes:
        parts.append(f"Minuty: {', '.join(minutes)}")
    if hours:
        parts.append(f"Godziny: {', '.join(hours)}")
    if days:
        parts.append(f"Dni: {', '.join(days)}")
    if weeks:
        parts.append(f"Tygodnie: {', '.join(weeks)}")
    if months:
        parts.append(f"Miesiące: {', '.join(months)}")
    
    return "\n".join(parts)

logger.info("✅ Timeframe Validator loaded")

