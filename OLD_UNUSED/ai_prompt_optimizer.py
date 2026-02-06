"""
AI Prompt Optimizer - Automatycznie ulepsza prompt DeepSeek
Na podstawie najlepszych historycznych sygnałów (few-shot learning)
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

PROMPT_HISTORY_DB = 'prompt_optimization_history.json'
MAX_EXAMPLES = 5  # Maksymalna liczba przykładów w few-shot

class AIPromptOptimizer:
    """Optimizes AI prompts based on successful predictions"""
    
    def __init__(self):
        self.optimization_history = self._load_history()
        self.base_system_prompt = self._get_base_system_prompt()
    
    def _load_history(self):
        """Load optimization history"""
        if os.path.exists(PROMPT_HISTORY_DB):
            try:
                with open(PROMPT_HISTORY_DB, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading prompt history: {e}")
        return {
            'optimizations': [],
            'best_examples': [],
            'last_updated': None
        }
    
    def _save_history(self):
        """Save optimization history"""
        self.optimization_history['last_updated'] = datetime.now().isoformat()
        with open(PROMPT_HISTORY_DB, 'w') as f:
            json.dump(self.optimization_history, f, indent=2)
    
    def _get_base_system_prompt(self) -> str:
        """Base system prompt for DeepSeek"""
        return """You are an elite cryptocurrency trading analyst with 15+ years of experience.

Your expertise:
- Pattern recognition (chart patterns, candlestick formations)
- Multi-indicator synthesis (RSI, EMA, MACD, Volume, Bollinger Bands)
- Market psychology and sentiment analysis
- Risk-reward optimization
- Multi-timeframe analysis

Your goal: Provide ACTIONABLE predictions for cryptocurrency price movements with:
- Specific price targets and probabilities
- Precise time windows (not vague "soon")
- Clear stop-loss levels
- Risk factor identification
- Multi-indicator reasoning

You MUST provide concrete, measurable predictions that can be verified."""
    
    def find_best_examples(self, signals_db: Dict, results_db: Dict, timeframe='24h', limit=5) -> List[Dict]:
        """
        Find the best performing signals to use as examples
        
        Returns: List of top performing signals with full context
        """
        logger.info(f"🔍 Finding best examples from {len(signals_db)} signals...")
        
        scored_signals = []
        
        for signal_id, signal in signals_db.items():
            if signal_id not in results_db or timeframe not in results_db[signal_id]:
                continue
            
            result = results_db[signal_id][timeframe]
            
            # Score based on:
            # 1. Correctness (most important)
            # 2. Confidence (prefer high confidence correct signals)
            # 3. Price change magnitude (bigger moves = better examples)
            
            if result['correct']:
                confidence = signal.get('confidence', 50)
                price_change = abs(result['price_change_pct'])
                
                # Score formula: correct signals only, weighted by confidence and magnitude
                score = confidence * (1 + price_change / 10)
                
                scored_signals.append({
                    'signal_id': signal_id,
                    'score': score,
                    'signal': signal,
                    'result': result
                })
        
        # Sort by score and get top N
        top_signals = sorted(scored_signals, key=lambda x: x['score'], reverse=True)[:limit]
        
        logger.info(f"✅ Found {len(top_signals)} best examples")
        
        return top_signals
    
    def create_few_shot_examples(self, best_signals: List[Dict]) -> str:
        """
        Create few-shot learning examples from best signals
        
        Format: Show successful prediction examples to AI
        """
        if not best_signals:
            return ""
        
        examples = "\n\nHere are examples of your most ACCURATE past predictions:\n\n"
        
        for i, sig_data in enumerate(best_signals, 1):
            signal = sig_data['signal']
            result = sig_data['result']
            
            symbol = signal.get('symbol', 'UNKNOWN')
            signal_type = signal.get('signal', 'HOLD')
            entry_price = signal.get('entry_price', 0)
            confidence = signal.get('confidence', 50)
            
            ind = signal.get('indicators', {})
            rsi = ind.get('rsi', 50)
            ema_cross = ind.get('ema_cross', False)
            macd_signal = ind.get('macd_signal', 'neutral')
            volume_ratio = ind.get('volume_ratio', 1.0)
            
            actual_price = result.get('current_price', entry_price)
            price_change = result.get('price_change_pct', 0)
            
            examples += f"""EXAMPLE {i}:
Symbol: {symbol}
Entry Price: ${entry_price}
Indicators:
  - RSI: {rsi}
  - EMA Cross: {'Yes' if ema_cross else 'No'}
  - MACD: {macd_signal}
  - Volume: {volume_ratio:.2f}x average

Your Prediction:
  Signal: {signal_type}
  Confidence: {confidence}%

Actual Result (24h later):
  Price: ${actual_price}
  Change: {price_change:+.2f}%
  Outcome: ✅ CORRECT

---
"""
        
        examples += "\nUse these examples as reference for high-quality predictions. Match this level of accuracy.\n"
        
        return examples
    
    def create_adaptive_instructions(self, pattern_insights: Dict) -> str:
        """
        Create adaptive instructions based on learned patterns
        
        Args:
            pattern_insights: Insights from PatternLearningEngine
        """
        instructions = "\n\nADAPTIVE ANALYSIS GUIDELINES (learned from data):\n\n"
        
        # RSI thresholds
        optimal_thresholds = pattern_insights.get('optimal_thresholds', {})
        
        if 'rsi_buy_threshold' in optimal_thresholds:
            rsi_buy = optimal_thresholds['rsi_buy_threshold']
            instructions += f"• RSI BUY signals are most accurate around {rsi_buy} (not just <30)\n"
        
        if 'rsi_sell_threshold' in optimal_thresholds:
            rsi_sell = optimal_thresholds['rsi_sell_threshold']
            instructions += f"• RSI SELL signals are most accurate around {rsi_sell} (not just >70)\n"
        
        # Volume importance
        if 'volume_ratio_threshold' in optimal_thresholds:
            vol = optimal_thresholds['volume_ratio_threshold']
            instructions += f"• Volume ratio above {vol}x significantly increases accuracy\n"
        
        # Best combinations
        best_combos = pattern_insights.get('best_combinations', [])
        if best_combos:
            instructions += f"\nHIGH-ACCURACY PATTERNS ({len(best_combos)} discovered):\n"
            for combo in best_combos[:3]:  # Top 3
                pattern = combo.get('pattern', '')
                win_rate = combo.get('win_rate', 0)
                instructions += f"• {pattern}: {win_rate}% win rate\n"
        
        # Indicator analysis
        ind_analysis = pattern_insights.get('indicator_patterns', {})
        if ind_analysis:
            instructions += "\nINDICATOR INSIGHTS:\n"
            for ind_name, data in ind_analysis.items():
                power = data.get('predictive_power', 0)
                if power > 5:  # Only significant ones
                    instructions += f"• {ind_name}: High predictive power (weight this heavily)\n"
        
        return instructions
    
    def build_optimized_prompt(
        self, 
        best_examples: List[Dict],
        pattern_insights: Dict,
        symbol: str,
        indicators: Dict,
        data: Dict
    ) -> Tuple[str, str]:
        """
        Build optimized system + user prompt with few-shot examples
        
        Returns: (system_prompt, user_prompt)
        """
        # System prompt = base + few-shot examples + adaptive instructions
        system_prompt = self.base_system_prompt
        
        # Add few-shot examples
        few_shot = self.create_few_shot_examples(best_examples)
        system_prompt += few_shot
        
        # Add adaptive instructions
        adaptive = self.create_adaptive_instructions(pattern_insights)
        system_prompt += adaptive
        
        # User prompt (technical analysis request)
        price = data.get('last', 0)
        rsi = indicators.get('rsi', 50)
        ema_cross = indicators.get('ema_cross', False)
        ema_age = indicators.get('ema_cross_age_hours', 0)
        macd_signal = indicators.get('macd_signal', 'neutral')
        macd_hist = indicators.get('macd_histogram', 0)
        volume_ratio = indicators.get('volume_ratio', 1.0)
        bb_position = indicators.get('bollinger_position', 'middle')
        
        ema_status = "FRESH Golden Cross" if ema_cross and ema_age < 2 else \
                    "Mature Golden Cross" if ema_cross else "No cross"
        
        user_prompt = f"""ANALYSIS TASK:
Symbol: {symbol}
Current Price: ${price}

TECHNICAL INDICATORS:
- RSI: {rsi:.1f} (oversold <30, overbought >70)
- EMA Cross: {ema_status} (age: {ema_age:.1f}h)
- MACD: {macd_signal} (histogram: {macd_hist:.2f})
- Volume: {volume_ratio:.2f}x average (1.0 = normal)
- Bollinger Bands: Price at {bb_position}

REQUIRED OUTPUT FORMAT:
1. Direction: [BUY/SELL/HOLD]
2. Confidence: [number 0-100]
3. Price Target 1: $X (probability Y%, timeframe: Z minutes)
4. Price Target 2: $X (probability Y%, timeframe: Z minutes)
5. Stop Loss: $X
6. Valid Until: [X hours from now]
7. Key Risks: [list 2-3 specific risks]
8. Reasoning: [2-3 sentences with specific indicator references]

Be SPECIFIC with numbers, times, and probabilities. Match the accuracy level of the examples above."""

        return system_prompt, user_prompt
    
    def track_prompt_performance(
        self, 
        prompt_version: str,
        signal_id: str,
        was_correct: bool,
        confidence: int
    ):
        """Track how well this prompt version performed"""
        
        self.optimization_history['optimizations'].append({
            'timestamp': datetime.now().isoformat(),
            'prompt_version': prompt_version,
            'signal_id': signal_id,
            'was_correct': was_correct,
            'confidence': confidence
        })
        
        self._save_history()
    
    def get_optimization_stats(self) -> Dict:
        """Get statistics about prompt optimization performance"""
        
        optimizations = self.optimization_history.get('optimizations', [])
        
        if not optimizations:
            return {
                'total_predictions': 0,
                'accuracy': 0,
                'avg_confidence': 0
            }
        
        total = len(optimizations)
        correct = sum(1 for o in optimizations if o.get('was_correct', False))
        avg_conf = sum(o.get('confidence', 0) for o in optimizations) / total if total > 0 else 0
        
        return {
            'total_predictions': total,
            'accuracy': round((correct / total * 100), 2) if total > 0 else 0,
            'avg_confidence': round(avg_conf, 2),
            'optimizations_count': len(set(o.get('prompt_version') for o in optimizations))
        }

# Global instance
prompt_optimizer = AIPromptOptimizer()

