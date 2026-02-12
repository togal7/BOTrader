"""
Volume Profile & Point of Control (POC)
Analizuje rozkład volumenu po poziomach cenowych
"""
import numpy as np
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class VolumeProfile:
    """Volume Profile z POC, VWAP i Volume Delta"""
    
    def __init__(self, bins: int = 50):
        self.bins = bins  # Ile poziomów cenowych
    
    def analyze(self, ohlcv: List, timeframe: str = '4h') -> Dict:
        """
        Główna analiza Volume Profile
        
        Returns:
            {
                'poc': float,  # Point of Control - cena z max volumenem
                'value_area_high': float,  # 70% volumenu - góra
                'value_area_low': float,   # 70% volumenu - dół
                'vwap': float,  # Volume Weighted Average Price
                'volume_delta': float,  # Buying pressure - selling pressure
                'profile': [...],  # Histogram volumenu po cenach
                'bias': 'LONG' | 'SHORT' | 'NEUTRAL'
            }
        """
        if not ohlcv or len(ohlcv) < 20:
            return self._empty_result()
        
        try:
            closes = np.array([x[4] for x in ohlcv])
            volumes = np.array([x[5] for x in ohlcv])
            highs = np.array([x[2] for x in ohlcv])
            lows = np.array([x[3] for x in ohlcv])
            opens = np.array([x[1] for x in ohlcv])
            
            # 1. POC - Point of Control
            poc, profile = self._calculate_poc(closes, volumes)
            
            # 2. Value Area (70% volumenu)
            va_high, va_low = self._calculate_value_area(profile, closes, volumes)
            
            # 3. VWAP
            vwap = np.sum(closes * volumes) / np.sum(volumes)
            
            # 4. Volume Delta (buying vs selling pressure)
            volume_delta = self._calculate_volume_delta(opens, closes, highs, lows, volumes)
            
            # 5. Bias based on price vs POC/VWAP
            current_price = closes[-1]
            bias = self._determine_bias(current_price, poc, vwap, volume_delta)
            
            return {
                'poc': float(poc),
                'value_area_high': float(va_high),
                'value_area_low': float(va_low),
                'vwap': float(vwap),
                'volume_delta': float(volume_delta),
                'profile': profile,
                'current_vs_poc': 'above' if current_price > poc else 'below',
                'current_vs_vwap': 'above' if current_price > vwap else 'below',
                'bias': bias,
                'confidence': self._calculate_confidence(current_price, poc, vwap, volume_delta)
            }
            
        except Exception as e:
            logger.error(f"Volume Profile error: {e}")
            return self._empty_result()
    
    def _calculate_poc(self, closes: np.ndarray, volumes: np.ndarray) -> Tuple[float, List]:
        """Znajdź POC - cenę z największym volumenem"""
        price_min = closes.min()
        price_max = closes.max()
        
        # Podziel zakres cen na bins
        bins = np.linspace(price_min, price_max, self.bins)
        
        # Histogram volumenu
        volume_per_bin = np.zeros(self.bins - 1)
        
        for price, vol in zip(closes, volumes):
            bin_idx = np.digitize(price, bins) - 1
            if 0 <= bin_idx < len(volume_per_bin):
                volume_per_bin[bin_idx] += vol
        
        # POC = bin z max volumenem
        poc_idx = np.argmax(volume_per_bin)
        poc = (bins[poc_idx] + bins[poc_idx + 1]) / 2
        
        profile = [
            {'price': (bins[i] + bins[i+1])/2, 'volume': volume_per_bin[i]}
            for i in range(len(volume_per_bin))
        ]
        
        return poc, profile
    
    def _calculate_value_area(self, profile: List, closes: np.ndarray, volumes: np.ndarray) -> Tuple[float, float]:
        """Znajdź Value Area (70% całkowitego volumenu)"""
        total_volume = volumes.sum()
        target_volume = total_volume * 0.7
        
        # Sortuj profile po volumenie
        sorted_profile = sorted(profile, key=lambda x: x['volume'], reverse=True)
        
        accumulated_volume = 0
        value_area_prices = []
        
        for entry in sorted_profile:
            accumulated_volume += entry['volume']
            value_area_prices.append(entry['price'])
            if accumulated_volume >= target_volume:
                break
        
        va_high = max(value_area_prices) if value_area_prices else closes.max()
        va_low = min(value_area_prices) if value_area_prices else closes.min()
        
        return va_high, va_low
    
    def _calculate_volume_delta(self, opens: np.ndarray, closes: np.ndarray, 
                                highs: np.ndarray, lows: np.ndarray, 
                                volumes: np.ndarray) -> float:
        """
        Volume Delta = Buying Volume - Selling Volume
        Pozytywna = więcej kupujących, negatywna = więcej sprzedających
        """
        buying_volume = 0
        selling_volume = 0
        
        for i in range(len(closes)):
            # Jeśli close > open = świeczka zielona (buying)
            if closes[i] > opens[i]:
                buying_volume += volumes[i]
            # Jeśli close < open = świeczka czerwona (selling)
            elif closes[i] < opens[i]:
                selling_volume += volumes[i]
            # Jeśli równe, podziel 50/50
            else:
                buying_volume += volumes[i] / 2
                selling_volume += volumes[i] / 2
        
        total_volume = volumes.sum()
        delta_ratio = (buying_volume - selling_volume) / total_volume if total_volume > 0 else 0
        
        return delta_ratio  # Range: -1 (all selling) to +1 (all buying)
    
    def _determine_bias(self, current_price: float, poc: float, vwap: float, delta: float) -> str:
        """Określ bias na podstawie pozycji ceny i Volume Delta"""
        score = 0
        
        # Price > POC = bullish
        if current_price > poc:
            score += 1
        else:
            score -= 1
        
        # Price > VWAP = bullish
        if current_price > vwap:
            score += 1
        else:
            score -= 1
        
        # Positive delta = bullish
        if delta > 0.1:
            score += 2
        elif delta < -0.1:
            score -= 2
        
        if score >= 2:
            return 'LONG'
        elif score <= -2:
            return 'SHORT'
        else:
            return 'NEUTRAL'
    
    def _calculate_confidence(self, price: float, poc: float, vwap: float, delta: float) -> int:
        """Confidence 0-100 based on alignment"""
        confidence = 50
        
        # Price near POC = high confidence support/resistance
        distance_to_poc = abs(price - poc) / poc
        if distance_to_poc < 0.01:  # within 1%
            confidence += 20
        
        # Strong Volume Delta = high confidence
        if abs(delta) > 0.3:
            confidence += 15
        
        # Price above both POC and VWAP = strong bullish
        if price > poc and price > vwap:
            confidence += 15
        elif price < poc and price < vwap:
            confidence += 15
        
        return min(100, confidence)
    
    def _empty_result(self) -> Dict:
        return {
            'poc': 0,
            'value_area_high': 0,
            'value_area_low': 0,
            'vwap': 0,
            'volume_delta': 0,
            'bias': 'NEUTRAL',
            'confidence': 0
        }

