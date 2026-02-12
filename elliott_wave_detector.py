"""
Elliott Wave Theory (EWT) Detector
Wykrywa fale impulsowe (1-2-3-4-5) i korekty (ABC)
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ElliottWaveDetector:
    """Detektor fal Elliotta z walidacją reguł"""
    
    def __init__(self):
        self.fib_levels = {
            'retracement': [0.236, 0.382, 0.5, 0.618, 0.786],
            'extension': [1.0, 1.272, 1.618, 2.0, 2.618]
        }
    
    def detect_waves(self, ohlcv: List, timeframe: str = '1h') -> Dict:
        """
        Główna funkcja wykrywania fal
        
        Returns:
            {
                'wave_type': 'impulse' | 'correction' | 'unknown',
                'current_wave': 1-5 | 'A' | 'B' | 'C',
                'pivot_points': [...],
                'fib_levels': {...},
                'confidence': 0-100,
                'bias': 'LONG' | 'SHORT' | 'NEUTRAL'
            }
        """
        if not ohlcv or len(ohlcv) < 50:
            return self._empty_result()
        
        try:
            # 1. Znajdź pivot points (swing highs/lows)
            pivots = self._find_pivots(ohlcv)
            
            if len(pivots) < 5:
                return self._empty_result()
            
            # 2. Spróbuj dopasować impuls (5 fal)
            impulse = self._detect_impulse(pivots, ohlcv)
            
            if impulse['valid']:
                return impulse
            
            # 3. Spróbuj dopasować korekcję (ABC)
            correction = self._detect_correction(pivots, ohlcv)
            
            if correction['valid']:
                return correction
            
            return self._empty_result()
            
        except Exception as e:
            logger.error(f"EWT detection error: {e}")
            return self._empty_result()
    
    def _find_pivots(self, ohlcv: List, window: int = 5) -> List[Dict]:
        """Znajdź swing highs i lows (pivot points)"""
        highs = [x[2] for x in ohlcv]  # high
        lows = [x[3] for x in ohlcv]   # low
        closes = [x[4] for x in ohlcv]
        
        pivots = []
        
        for i in range(window, len(ohlcv) - window):
            # Swing High
            if highs[i] == max(highs[i-window:i+window+1]):
                pivots.append({
                    'type': 'high',
                    'price': highs[i],
                    'index': i,
                    'timestamp': ohlcv[i][0]
                })
            
            # Swing Low
            elif lows[i] == min(lows[i-window:i+window+1]):
                pivots.append({
                    'type': 'low',
                    'price': lows[i],
                    'index': i,
                    'timestamp': ohlcv[i][0]
                })
        
        return pivots
    
    def _detect_impulse(self, pivots: List[Dict], ohlcv: List) -> Dict:
        """
        Wykryj impuls 5-falowy (1-2-3-4-5)
        Reguły:
        - F2 nie schodzi poniżej start F1
        - F3 > F1 (najdłuższa)
        - F4 nie wchodzi w F1
        """
        if len(pivots) < 6:
            return {'valid': False}
        
        # Weź ostatnie 6 pivotów (potencjalne 5 fal)
        recent = pivots[-6:]
        
        # Sprawdź czy jest alternatywny pattern (high-low-high-low-high-low)
        pattern = [p['type'] for p in recent]
        
        # Uptrend impulse: low-high-low-high-low-high
        if pattern == ['low', 'high', 'low', 'high', 'low', 'high']:
            return self._validate_impulse_up(recent, ohlcv)
        
        # Downtrend impulse: high-low-high-low-high-low
        elif pattern == ['high', 'low', 'high', 'low', 'high', 'low']:
            return self._validate_impulse_down(recent, ohlcv)
        
        return {'valid': False}
    
    def _validate_impulse_up(self, pivots: List[Dict], ohlcv: List) -> Dict:
        """Waliduj impuls wzrostowy"""
        # pivots: [0=low, 1=high, 2=low, 3=high, 4=low, 5=high]
        # Fale: F1=(0→1), F2=(1→2), F3=(2→3), F4=(3→4), F5=(4→5)
        
        f1_start = pivots[0]['price']
        f1_end = pivots[1]['price']
        f2_end = pivots[2]['price']
        f3_end = pivots[3]['price']
        f4_end = pivots[4]['price']
        f5_end = pivots[5]['price']
        
        f1_size = f1_end - f1_start
        f3_size = f3_end - f2_end
        
        # Reguła 1: F2 nie poniżej F1 start
        if f2_end < f1_start:
            return {'valid': False}
        
        # Reguła 2: F3 > F1
        if f3_size <= f1_size:
            return {'valid': False}
        
        # Reguła 3: F4 nie wchodzi w F1
        if f4_end < f1_end:
            return {'valid': False}
        
        # Oblicz Fibonacci levels
        fib_f2 = self._calc_fib_retracement(f1_start, f1_end, f2_end)
        fib_f4 = self._calc_fib_retracement(f2_end, f3_end, f4_end)
        
        # Sprawdź czy F5 completed
        current_price = ohlcv[-1][4]
        f5_target = f1_start + (f1_size * 1.618)  # 161.8% extension
        
        if current_price >= f5_target * 0.95:
            current_wave = 5
            bias = 'SHORT'  # F5 kończy się, spodziewaj się korekty
        elif current_price > f4_end:
            current_wave = 5
            bias = 'LONG'
        elif abs(current_price - f4_end) < (f3_end - f2_end) * 0.1:
            current_wave = 4
            bias = 'LONG'  # F4 kończy się, kupuj pullback
        else:
            current_wave = 3
            bias = 'LONG'
        
        return {
            'valid': True,
            'wave_type': 'impulse',
            'direction': 'UP',
            'current_wave': current_wave,
            'pivots': pivots,
            'fib_levels': {
                'f2_retrace': fib_f2,
                'f4_retrace': fib_f4,
                'f5_target': f5_target
            },
            'confidence': 75,
            'bias': bias,
            'reasoning': f"Impulse UP - Wave {current_wave}, F3 > F1 validated"
        }
    
    def _validate_impulse_down(self, pivots: List[Dict], ohlcv: List) -> Dict:
        """Waliduj impuls spadkowy (analogia do UP)"""
        # pivots: [0=high, 1=low, 2=high, 3=low, 4=high, 5=low]
        
        f1_start = pivots[0]['price']
        f1_end = pivots[1]['price']
        f2_end = pivots[2]['price']
        f3_end = pivots[3]['price']
        f4_end = pivots[4]['price']
        f5_end = pivots[5]['price']
        
        f1_size = abs(f1_end - f1_start)
        f3_size = abs(f3_end - f2_end)
        
        # Reguły analogicznie
        if f2_end > f1_start or f3_size <= f1_size or f4_end > f1_end:
            return {'valid': False}
        
        current_price = ohlcv[-1][4]
        
        return {
            'valid': True,
            'wave_type': 'impulse',
            'direction': 'DOWN',
            'current_wave': 5,
            'confidence': 70,
            'bias': 'SHORT'
        }
    
    def _detect_correction(self, pivots: List[Dict], ohlcv: List) -> Dict:
        """Wykryj korekcję ABC"""
        if len(pivots) < 4:
            return {'valid': False}
        
        recent = pivots[-4:]
        pattern = [p['type'] for p in recent]
        
        # ABC up correction: high-low-high-low
        if pattern == ['high', 'low', 'high', 'low']:
            a_start = recent[0]['price']
            a_end = recent[1]['price']
            b_end = recent[2]['price']
            c_end = recent[3]['price']
            
            # B retrace 50-61.8% A
            fib_b = self._calc_fib_retracement(a_start, a_end, b_end)
            
            if 0.5 <= fib_b <= 0.618:
                return {
                    'valid': True,
                    'wave_type': 'correction',
                    'direction': 'DOWN',
                    'current_wave': 'C',
                    'confidence': 65,
                    'bias': 'SHORT',
                    'reasoning': f"ABC correction, B retrace {fib_b:.1%}"
                }
        
        return {'valid': False}
    
    def _calc_fib_retracement(self, start: float, end: float, current: float) -> float:
        """Oblicz % retracement Fibonacci"""
        move = abs(end - start)
        retrace = abs(current - end)
        return retrace / move if move > 0 else 0
    
    def _empty_result(self) -> Dict:
        return {
            'valid': False,
            'wave_type': 'unknown',
            'current_wave': None,
            'confidence': 0,
            'bias': 'NEUTRAL'
        }

