#!/usr/bin/env python3
"""
Pattern Analyzer - analizuje ai_signals_history.json i tworzy learned_patterns.json
"""
import json
import logging
from datetime import datetime
from collections import defaultdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_patterns():
    """Analizuje sygnały i tworzy wzorce"""
    try:
        # Wczytaj historię
        with open('ai_signals_history.json') as f:
            history = json.load(f)
        
        logger.info(f"📊 Analyzing {len(history)} signals...")
        
        # Statystyki per symbol/timeframe
        patterns = defaultdict(lambda: {
            'total': 0,
            'verified': 0,
            'correct': 0,
            'accuracy': 0
        })
        
        for sig_id, sig in history.items():
            if sig.get('source') != 'ai_signals':
                continue
            
            symbol = sig.get('symbol', 'UNKNOWN')
            tf = sig.get('timeframe', 'UNKNOWN')
            key = f"{symbol}_{tf}"
            
            patterns[key]['total'] += 1
            
            if sig.get('verified'):
                patterns[key]['verified'] += 1
                if sig.get('correct'):
                    patterns[key]['correct'] += 1
        
        # Oblicz accuracy
        for key in patterns:
            p = patterns[key]
            if p['verified'] > 0:
                p['accuracy'] = round((p['correct'] / p['verified']) * 100, 1)
        
        # Top patterns (accuracy >= 60%)
        top_patterns = {k: v for k, v in patterns.items() 
                       if v['verified'] >= 3 and v['accuracy'] >= 60}
        
        # Zapisz
        learned = {
            'version': '1.0',
            'last_update': datetime.now().isoformat(),
            'patterns': dict(patterns),
            'top_patterns': top_patterns,
            'stats': {
                'total_signals': len(history),
                'total_patterns': len(patterns),
                'high_accuracy_patterns': len(top_patterns)
            }
        }
        
        with open('learned_patterns.json', 'w') as f:
            json.dump(learned, f, indent=2)
        
        logger.info(f"✅ Patterns saved:")
        logger.info(f"   • Total patterns: {len(patterns)}")
        logger.info(f"   • High accuracy (>=60%): {len(top_patterns)}")
        
        # Pokaż top 5
        sorted_patterns = sorted(top_patterns.items(), 
                                key=lambda x: x[1]['accuracy'], 
                                reverse=True)[:5]
        
        logger.info(f"\n🏆 TOP 5 PATTERNS:")
        for key, p in sorted_patterns:
            logger.info(f"   {key}: {p['accuracy']}% ({p['correct']}/{p['verified']})")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")

if __name__ == '__main__':
    analyze_patterns()
