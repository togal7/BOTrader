"""
CENTRALNA FUNKCJA ZAPISU SYGNAŁÓW
Używana przez: handlers.py, bot_learning.py, ultra_learning_generator.py
"""
from ai_signals_tracker import tracker
import logging

logger = logging.getLogger('signal_saver')

def save_analysis_result(result: dict, symbol: str, exchange: str, timeframe: str, source: str = "unknown"):
    """
    JEDNA funkcja do zapisu WSZYSTKICH sygnałów
    
    Args:
        result: Wynik z central_analyzer.analyze_pair_full()
        symbol: Para np. BTC/USDT:USDT
        exchange: Giełda (mexc, binance)
        timeframe: 5m, 15m, 1h, 4h
        source: handlers/bot_learning/ultra_learning/alert
    
    Returns:
        signal_id lub None
    """
    if not result:
        return None
    
    # Zapisuj TYLKO sygnały z confidence >= 50
    confidence = result.get('signal', {}).get('confidence', 0) if isinstance(result.get('signal'), dict) else result.get('confidence', 0)
    if confidence < 50:
        return None
    
    try:
        # Truncate ai_response do 1000 znaków (limit SQLite)
        ai_resp = str(result.get('ai_reasoning', ''))[:1000]
        
        signal_id = tracker.record_signal(
            symbol=symbol,
            exchange=exchange,
            timeframe=timeframe,
            signal=result.get('signal', 'WAIT'),
            confidence=confidence,
            price=result.get('entry_price', 0),
            indicators=result.get('indicators', {}),
            ai_response=ai_resp
        )
        
        logger.info(f"💾 Saved signal: {symbol} {result.get('signal')} {confidence}% from {source}")
        return signal_id
        
    except Exception as e:
        logger.error(f"❌ Save failed {symbol}: {e}")
        return None

