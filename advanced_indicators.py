"""
Zaawansowane wskaźniki: Ichimoku, VWAP, Volume Delta
"""
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class AdvancedIndicators:
    """Ichimoku Cloud + dodatkowe wskaźniki"""
    
    @staticmethod
    def calculate_ichimoku(highs: List[float], lows: List[float], closes: List[float]) -> Dict:
        """
        Ichimoku Cloud
        
        Returns:
            {
                'tenkan_sen': float,  # Conversion Line (9)
                'kijun_sen': float,   # Base Line (26)
                'senkou_span_a': float,  # Leading Span A
                'senkou_span_b': float,  # Leading Span B
                'chikou_span': float,    # Lagging Span
                'cloud_color': 'bullish' | 'bearish',
                'price_vs_cloud': 'above' | 'in' | 'below',
                'signal': 'LONG' | 'SHORT' | 'NEUTRAL'
            }
        """
        if len(highs) < 52:
            return {'signal': 'NEUTRAL', 'confidence': 0}
        
        try:
            highs = np.array(highs)
            lows = np.array(lows)
            closes = np.array(closes)
            
            # Tenkan-sen (Conversion Line): (9-period high + 9-period low) / 2
            tenkan_sen = (highs[-9:].max() + lows[-9:].min()) / 2
            
            # Kijun-sen (Base Line): (26-period high + 26-period low) / 2
            kijun_sen = (highs[-26:].max() + lows[-26:].min()) / 2
            
            # Senkou Span A (Leading Span A): (Tenkan + Kijun) / 2, shifted 26 forward
            senkou_span_a = (tenkan_sen + kijun_sen) / 2
            
            # Senkou Span B (Leading Span B): (52-period high + 52-period low) / 2, shifted 26 forward
            senkou_span_b = (highs[-52:].max() + lows[-52:].min()) / 2
            
            # Chikou Span (Lagging Span): Current close, shifted 26 back
            chikou_span = closes[-1] if len(closes) >= 26 else closes[-1]
            
            # Cloud color
            cloud_color = 'bullish' if senkou_span_a > senkou_span_b else 'bearish'
            
            # Price vs Cloud
            current_price = closes[-1]
            cloud_top = max(senkou_span_a, senkou_span_b)
            cloud_bottom = min(senkou_span_a, senkou_span_b)
            
            if current_price > cloud_top:
                price_vs_cloud = 'above'
                signal = 'LONG'
            elif current_price < cloud_bottom:
                price_vs_cloud = 'below'
                signal = 'SHORT'
            else:
                price_vs_cloud = 'in'
                signal = 'NEUTRAL'
            
            # TK Cross (Tenkan cross Kijun)
            tk_cross = 'bullish' if tenkan_sen > kijun_sen else 'bearish'
            
            # Confidence
            confidence = 50
            if signal == 'LONG' and cloud_color == 'bullish' and tk_cross == 'bullish':
                confidence = 80
            elif signal == 'SHORT' and cloud_color == 'bearish' and tk_cross == 'bearish':
                confidence = 80
            
            return {
                'tenkan_sen': float(tenkan_sen),
                'kijun_sen': float(kijun_sen),
                'senkou_span_a': float(senkou_span_a),
                'senkou_span_b': float(senkou_span_b),
                'chikou_span': float(chikou_span),
                'cloud_color': cloud_color,
                'price_vs_cloud': price_vs_cloud,
                'tk_cross': tk_cross,
                'signal': signal,
                'confidence': confidence
            }
            
        except Exception as e:
            logger.error(f"Ichimoku calculation error: {e}")
            return {'signal': 'NEUTRAL', 'confidence': 0}
    
    @staticmethod
    def calculate_atr_trailing_stop(highs: List[float], lows: List[float], 
                                     closes: List[float], multiplier: float = 2.0) -> Dict:
        """
        ATR Trailing Stop Loss
        multiplier = 2.0 dla konserwatywnego, 1.5 dla agresywnego
        """
        if len(highs) < 14:
            return {'stop_long': 0, 'stop_short': 0}
        
        # ATR(14)
        tr_list = []
        for i in range(1, len(closes)):
            high = highs[i]
            low = lows[i]
            prev_close = closes[i-1]
            
            tr = max(
                high - low,
                abs(high - prev_close),
                abs(low - prev_close)
            )
            tr_list.append(tr)
        
        atr = np.mean(tr_list[-14:]) if len(tr_list) >= 14 else np.mean(tr_list)
        
        current_price = closes[-1]
        
        return {
            'atr': float(atr),
            'stop_long': float(current_price - (atr * multiplier)),
            'stop_short': float(current_price + (atr * multiplier)),
            'multiplier': multiplier
        }

