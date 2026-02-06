"""
Dynamic Weights System - Automatycznie dostosowuje wagi wskaźników
Na podstawie ich rzeczywistej skuteczności w przewidywaniu
"""

import json
import os
from datetime import datetime
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

WEIGHTS_DB = 'indicator_weights.json'

# Default weights (początkowe, równe dla wszystkich)
DEFAULT_WEIGHTS = {
    'rsi': 0.20,
    'ema_cross': 0.20,
    'macd': 0.15,
    'volume': 0.15,
    'bollinger': 0.15,
    'price_action': 0.15
}

class DynamicWeightsSystem:
    """Manages and updates indicator weights based on performance"""
    
    def __init__(self):
        self.weights = self._load_weights()
        self.performance_history = []
    
    def _load_weights(self):
        """Load current weights"""
        if os.path.exists(WEIGHTS_DB):
            try:
                with open(WEIGHTS_DB, 'r') as f:
                    data = json.load(f)
                    return data.get('weights', DEFAULT_WEIGHTS)
            except Exception as e:
                logger.error(f"Error loading weights: {e}")
        return DEFAULT_WEIGHTS.copy()
    
    def _save_weights(self):
        """Save updated weights"""
        data = {
            'weights': self.weights,
            'last_updated': datetime.now().isoformat(),
            'performance_history': self.performance_history[-100:]  # Last 100 updates
        }
        
        with open(WEIGHTS_DB, 'w') as f:
            json.dump(data, f, indent=2)
    
    def calculate_indicator_impact(self, signals_db: Dict, results_db: Dict, timeframe='24h') -> Dict:
        """
        Calculate which indicators had the most impact on successful predictions
        
        Returns: Dict with indicator performance scores
        """
        logger.info("📊 Calculating indicator impact...")
        
        indicator_stats = {
            'rsi': {'correct_when_strong': 0, 'total_strong_signals': 0},
            'ema_cross': {'correct_when_present': 0, 'total_with_cross': 0},
            'macd': {'correct_when_aligned': 0, 'total_aligned': 0},
            'volume': {'correct_when_high': 0, 'total_high_volume': 0},
            'bollinger': {'correct_at_bands': 0, 'total_at_bands': 0}
        }
        
        for signal_id, signal in signals_db.items():
            if signal_id not in results_db or timeframe not in results_db[signal_id]:
                continue
            
            result = results_db[signal_id][timeframe]
            was_correct = result['correct']
            
            ind = signal.get('indicators', {})
            signal_type = signal.get('signal')
            
            # RSI analysis
            rsi = ind.get('rsi', 50)
            rsi_strong = (rsi < 30 and signal_type == 'BUY') or (rsi > 70 and signal_type == 'SELL')
            if rsi_strong:
                indicator_stats['rsi']['total_strong_signals'] += 1
                if was_correct:
                    indicator_stats['rsi']['correct_when_strong'] += 1
            
            # EMA Cross analysis
            ema_cross = ind.get('ema_cross', False)
            if ema_cross:
                indicator_stats['ema_cross']['total_with_cross'] += 1
                if was_correct:
                    indicator_stats['ema_cross']['correct_when_present'] += 1
            
            # MACD analysis
            macd_signal = ind.get('macd_signal', 'neutral')
            macd_aligned = (macd_signal == 'bullish' and signal_type == 'BUY') or \
                          (macd_signal == 'bearish' and signal_type == 'SELL')
            if macd_aligned:
                indicator_stats['macd']['total_aligned'] += 1
                if was_correct:
                    indicator_stats['macd']['correct_when_aligned'] += 1
            
            # Volume analysis
            vol_ratio = ind.get('volume_ratio', 1.0)
            high_volume = vol_ratio > 1.5
            if high_volume:
                indicator_stats['volume']['total_high_volume'] += 1
                if was_correct:
                    indicator_stats['volume']['correct_when_high'] += 1
            
            # Bollinger Bands analysis
            bb_pos = ind.get('bollinger_position', 'middle')
            at_bands = bb_pos in ['lower', 'upper']
            if at_bands:
                indicator_stats['bollinger']['total_at_bands'] += 1
                if was_correct:
                    indicator_stats['bollinger']['correct_at_bands'] += 1
        
        # Calculate accuracy for each indicator
        impact_scores = {}
        for indicator, stats in indicator_stats.items():
            total_key = [k for k in stats.keys() if k.startswith('total_')][0]
            correct_key = [k for k in stats.keys() if k.startswith('correct_')][0]
            
            total = stats[total_key]
            correct = stats[correct_key]
            
            if total >= 10:  # Minimum 10 samples
                accuracy = (correct / total) * 100
                impact_scores[indicator] = {
                    'accuracy': round(accuracy, 2),
                    'samples': total,
                    'impact_score': accuracy / 100  # Normalized to 0-1
                }
            else:
                impact_scores[indicator] = {
                    'accuracy': 0,
                    'samples': total,
                    'impact_score': 0.5  # Default neutral
                }
        
        return impact_scores
    
    def update_weights(self, impact_scores: Dict):
        """
        Update weights based on indicator performance
        Uses exponential moving average for smooth transitions
        """
        logger.info("⚙️ Updating weights based on performance...")
        
        # Learning rate - jak szybko adaptujemy (0.1 = 10% change per update)
        LEARNING_RATE = 0.15
        
        # Calculate new weights
        total_impact = sum(score['impact_score'] for score in impact_scores.values())
        
        if total_impact == 0:
            logger.warning("No impact data - keeping current weights")
            return
        
        new_weights = {}
        for indicator, score_data in impact_scores.items():
            if indicator not in self.weights:
                continue
            
            # Target weight based on performance
            target_weight = score_data['impact_score'] / total_impact
            
            # Current weight
            current_weight = self.weights[indicator]
            
            # Smooth transition (EMA)
            new_weight = current_weight * (1 - LEARNING_RATE) + target_weight * LEARNING_RATE
            
            new_weights[indicator] = round(new_weight, 4)
        
        # Normalize to sum to 1.0
        total = sum(new_weights.values())
        if total > 0:
            new_weights = {k: round(v / total, 4) for k, v in new_weights.items()}
        
        # Log changes
        for indicator in new_weights:
            old = self.weights.get(indicator, 0)
            new = new_weights[indicator]
            change = ((new - old) / old * 100) if old > 0 else 0
            
            if abs(change) > 5:  # Only log significant changes
                logger.info(f"  {indicator}: {old:.4f} → {new:.4f} ({change:+.1f}%)")
        
        # Update
        self.weights = new_weights
        
        # Save history
        self.performance_history.append({
            'timestamp': datetime.now().isoformat(),
            'weights': new_weights.copy(),
            'impact_scores': impact_scores
        })
        
        self._save_weights()
        
        logger.info("✅ Weights updated")
    
    def get_current_weights(self) -> Dict:
        """Get current indicator weights"""
        return self.weights.copy()
    
    def calculate_weighted_confidence(self, indicators: Dict, base_confidence: float) -> float:
        """
        Calculate weighted confidence based on indicator strengths
        
        Args:
            indicators: Dict with indicator values
            base_confidence: Base confidence from analysis (0-100)
        
        Returns: Adjusted confidence (0-100)
        """
        # Score każdego wskaźnika (0-1)
        indicator_scores = {}
        
        # RSI score
        rsi = indicators.get('rsi', 50)
        if rsi < 30:
            indicator_scores['rsi'] = 1.0  # Strong oversold
        elif rsi > 70:
            indicator_scores['rsi'] = 1.0  # Strong overbought
        elif 30 <= rsi <= 40 or 60 <= rsi <= 70:
            indicator_scores['rsi'] = 0.7  # Moderate
        else:
            indicator_scores['rsi'] = 0.3  # Weak signal
        
        # EMA Cross score
        ema_cross = indicators.get('ema_cross', False)
        ema_age = indicators.get('ema_cross_age_hours', 100)
        if ema_cross and ema_age < 4:
            indicator_scores['ema_cross'] = 1.0  # Fresh cross
        elif ema_cross and ema_age < 12:
            indicator_scores['ema_cross'] = 0.6  # Recent cross
        else:
            indicator_scores['ema_cross'] = 0.2  # No cross or old
        
        # MACD score
        macd_signal = indicators.get('macd_signal', 'neutral')
        macd_hist = abs(indicators.get('macd_histogram', 0))
        if macd_signal in ['bullish', 'bearish'] and macd_hist > 0.5:
            indicator_scores['macd'] = 1.0  # Strong signal
        elif macd_signal in ['bullish', 'bearish']:
            indicator_scores['macd'] = 0.6  # Moderate
        else:
            indicator_scores['macd'] = 0.3  # Weak
        
        # Volume score
        vol_ratio = indicators.get('volume_ratio', 1.0)
        if vol_ratio > 2.0:
            indicator_scores['volume'] = 1.0  # Very high
        elif vol_ratio > 1.5:
            indicator_scores['volume'] = 0.8  # High
        elif vol_ratio > 1.2:
            indicator_scores['volume'] = 0.5  # Above average
        else:
            indicator_scores['volume'] = 0.3  # Normal/low
        
        # Bollinger score
        bb_pos = indicators.get('bollinger_position', 'middle')
        if bb_pos in ['lower', 'upper']:
            indicator_scores['bollinger'] = 0.9  # At bands
        elif bb_pos in ['below_middle', 'above_middle']:
            indicator_scores['bollinger'] = 0.5  # Between
        else:
            indicator_scores['bollinger'] = 0.3  # Middle
        
        # Price action (can be added later)
        indicator_scores['price_action'] = 0.5  # Neutral for now
        
        # Calculate weighted score
        weighted_score = 0
        for indicator, score in indicator_scores.items():
            weight = self.weights.get(indicator, 0)
            weighted_score += score * weight
        
        # Adjust confidence (weighted_score is 0-1)
        # If indicators align well (high weighted_score), boost confidence
        # If indicators are weak, reduce confidence
        
        adjustment_factor = weighted_score  # 0-1
        
        # Apply adjustment
        adjusted_confidence = base_confidence * (0.7 + 0.6 * adjustment_factor)
        
        # Cap at 95
        adjusted_confidence = min(adjusted_confidence, 95)
        
        logger.info(f"⚖️ Weighted confidence: {base_confidence:.0f} → {adjusted_confidence:.0f} (factor: {adjustment_factor:.2f})")
        
        return round(adjusted_confidence, 1)
    
    def get_weights_report(self) -> str:
        """Generate human-readable weights report"""
        report = "⚖️ CURRENT INDICATOR WEIGHTS:\n\n"
        
        sorted_weights = sorted(self.weights.items(), key=lambda x: x[1], reverse=True)
        
        for indicator, weight in sorted_weights:
            percentage = weight * 100
            bar_length = int(percentage / 5)  # 20 chars = 100%
            bar = '█' * bar_length + '░' * (20 - bar_length)
            
            report += f"{indicator:15} {bar} {percentage:5.1f}%\n"
        
        return report

# Global instance
weights_system = DynamicWeightsSystem()

