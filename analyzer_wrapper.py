"""
Wrapper dla Central AI Analyzer - dodaje tracking i learning
"""

import logging
from central_ai_analyzer import central_analyzer

logger = logging.getLogger(__name__)

try:
    from ai_signals_tracker import tracker
    from master_learning_system import master_learning
    LEARNING_AVAILABLE = True
    logger.info("✅ Learning modules loaded")
except ImportError as e:
    LEARNING_AVAILABLE = False
    logger.warning(f"⚠️ Learning modules not available: {e}")

class AnalyzerWithLearning:
    """Wrapper that adds learning to central_analyzer"""
    
    def __init__(self):
        self.analyzer = central_analyzer
        logger.info("🔧 AnalyzerWithLearning initialized")
        
    def __getattr__(self, name):
        """Przekieruj wszystkie inne metody do oryginalnego analyzera"""
        attr = getattr(self.analyzer, name)
        
        # Jeśli to metoda analyze_pair_full - owijamy w tracking
        if name == 'analyze_pair_full' and callable(attr):
            logger.debug("Wrapping analyze_pair_full with tracking")
            return self._wrap_analyze_pair_full(attr)
        
        return attr
    
    def _wrap_analyze_pair_full(self, original_method):
        """Wrapper dla analyze_pair_full z tracking"""
        
        async def wrapped(*args, **kwargs):
            logger.info(f"🎯 Wrapper intercept: analyze_pair_full")
            
            # Wywołaj oryginalną metodę
            result = await original_method(*args, **kwargs)
            
            # Track signal
            if LEARNING_AVAILABLE and result:
                logger.info("💡 Attempting to track signal...")
                try:
                    # Wyciągnij symbol z args/kwargs
                    symbol = args[0] if len(args) > 0 else kwargs.get('symbol', 'UNKNOWN')
                    exchange = args[1] if len(args) > 1 else kwargs.get('exchange', 'mexc')
                    timeframe = args[2] if len(args) > 2 else kwargs.get('timeframe', '1h')
                    
                    signal_id = tracker.record_signal(
                        symbol=symbol,
                        exchange=exchange,
                        timeframe=timeframe,
                        signal=result.get('signal', 'WAIT'),
                        confidence=result.get('confidence', 0),
                        price=result.get('price', 0),
                        indicators=result.get('indicators', {}),
                        ai_response=result.get('ai_analysis', ''),
                        user_id=None
                    )
                    logger.info(f"📊 Tracked signal: {signal_id}")
                    result['signal_id'] = signal_id
                    
                except Exception as e:
                    logger.error(f"Tracking error: {e}")
                    import traceback
                    traceback.print_exc()
            
            return result
        
        return wrapped
    
    async def analyze(self, symbol, exchange, timeframe, user_id=None):
        """Analyze with automatic tracking"""
        logger.info(f"🎯 Wrapper.analyze called for {symbol}")
        
        result = await self.analyzer.analyze(symbol, exchange, timeframe, user_id)
        
        if LEARNING_AVAILABLE and result:
            logger.info("💡 Attempting to track...")
            try:
                signal_id = tracker.record_signal(
                    symbol=symbol,
                    exchange=exchange,
                    timeframe=timeframe,
                    signal=result.get('signal', 'WAIT'),
                    confidence=result.get('confidence', 0),
                    price=result.get('price', 0),
                    indicators=result.get('indicators', {}),
                    ai_response=result.get('ai_analysis', ''),
                    user_id=user_id
                )
                logger.info(f"📊 Tracked: {signal_id}")
                result['signal_id'] = signal_id
            except Exception as e:
                logger.error(f"Track error: {e}")
        
        return result

analyzer_with_learning = AnalyzerWithLearning()
analyze = analyzer_with_learning.analyze

logger.info("✅ Analyzer Wrapper ready")

