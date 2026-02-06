#!/usr/bin/env python3
"""
MASTER LEARNING OPTIMIZER
Automatycznie dostosowuje filtry i progi na podstawie wyników
"""

import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from ai_signals_tracker import tracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('master_optimizer')

class MasterOptimizer:
    def __init__(self):
        self.config_file = 'optimizer_config.json'
        self.results_file = 'optimizer_results.json'
        self.load_config()
        
    def load_config(self):
        """Ładuj obecną konfigurację filtrów"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except:
            # Domyślna konfiguracja (obecne wartości)
            self.config = {
                'rsi_oversold': 30,
                'rsi_overbought': 70,
                'min_confidence': 50,
                'ema_200_filter': True,
                'volume_filter': True,
                'min_volume_ratio': 0.8,
                'last_optimized': None
            }
            self.save_config()
    
    def save_config(self):
        """Zapisz konfigurację"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def analyze_performance(self):
        """Analizuj wyniki i znajdź optymalne wartości"""
        logger.info("📊 Analyzing signal performance...")
        
        # Pobierz wszystkie sygnały z wynikami
        stats = {
            'total_signals': len(tracker.signals_db),
            'verified_24h': 0,
            'correct_24h': 0,
            'by_confidence': defaultdict(lambda: {'total': 0, 'correct': 0}),
            'by_direction': defaultdict(lambda: {'total': 0, 'correct': 0}),
        }
        
        for signal_id, signal in tracker.signals_db.items():
            # Sprawdź czy ma wyniki
            if signal_id in tracker.results_db:
                results = tracker.results_db[signal_id]
                
                if '24h' in results:
                    stats['verified_24h'] += 1
                    
                    confidence = signal.get('confidence', 0)
                    direction = signal.get('direction', 'NEUTRAL')
                    
                    # Pogrupuj po confidence (co 10%)
                    conf_bucket = (confidence // 10) * 10
                    stats['by_confidence'][conf_bucket]['total'] += 1
                    
                    # Pogrupuj po kierunku
                    stats['by_direction'][direction]['total'] += 1
                    
                    if results['24h'].get('correct'):
                        stats['correct_24h'] += 1
                        stats['by_confidence'][conf_bucket]['correct'] += 1
                        stats['by_direction'][direction]['correct'] += 1
        
        # Oblicz accuracy
        if stats['verified_24h'] > 0:
            stats['accuracy_24h'] = (stats['correct_24h'] / stats['verified_24h']) * 100
        else:
            stats['accuracy_24h'] = 0
        
        return stats
    
    def optimize_thresholds(self, stats):
        """Na podstawie statystyk dostosuj progi"""
        logger.info("🔧 Optimizing thresholds...")
        
        changes = []
        
        # 1. Confidence threshold
        # Znajdź najlepszy bucket confidence
        best_conf = 50
        best_acc = 0
        
        for conf, data in stats['by_confidence'].items():
            if data['total'] >= 10:  # Min 10 sygnałów
                acc = (data['correct'] / data['total']) * 100
                if acc > best_acc and acc > 60:
                    best_acc = acc
                    best_conf = conf
        
        if best_conf != self.config['min_confidence']:
            changes.append(f"min_confidence: {self.config['min_confidence']} → {best_conf}")
            self.config['min_confidence'] = best_conf
        
        # 2. RSI thresholds
        # Jeśli accuracy < 60%, spróbuj bardziej ekstremalnych wartości
        if stats['accuracy_24h'] < 60:
            if self.config['rsi_oversold'] > 25:
                changes.append(f"rsi_oversold: {self.config['rsi_oversold']} → 25")
                self.config['rsi_oversold'] = 25
            
            if self.config['rsi_overbought'] < 75:
                changes.append(f"rsi_overbought: {self.config['rsi_overbought']} → 75")
                self.config['rsi_overbought'] = 75
        
        # 3. Volume filter
        # Jeśli dużo NEUTRAL, obniż wymóg volume
        neutral_pct = (stats['by_direction']['NEUTRAL']['total'] / stats['total_signals'] * 100)
        
        if neutral_pct > 60 and self.config['min_volume_ratio'] > 0.5:
            changes.append(f"min_volume_ratio: {self.config['min_volume_ratio']} → 0.5")
            self.config['min_volume_ratio'] = 0.5
        
        # Zapisz zmiany
        if changes:
            self.config['last_optimized'] = datetime.now().isoformat()
            self.save_config()
            
            logger.info("✅ Applied optimizations:")
            for change in changes:
                logger.info(f"  • {change}")
        else:
            logger.info("✅ No changes needed - system is optimal")
        
        return changes
    
    def run_optimization(self):
        """Główna funkcja optymalizacji"""
        logger.info("="*60)
        logger.info("🧠 MASTER OPTIMIZER - Starting optimization cycle")
        logger.info("="*60)
        
        # 1. Analizuj wyniki
        stats = self.analyze_performance()
        
        logger.info(f"\n📊 PERFORMANCE STATS:")
        logger.info(f"  Total signals: {stats['total_signals']}")
        logger.info(f"  Verified 24h: {stats['verified_24h']}")
        logger.info(f"  Accuracy 24h: {stats['accuracy_24h']:.1f}%")
        
        logger.info(f"\n📈 By Direction:")
        for direction, data in stats['by_direction'].items():
            if data['total'] > 0:
                acc = (data['correct'] / data['total']) * 100
                logger.info(f"  {direction}: {acc:.1f}% ({data['correct']}/{data['total']})")
        
        logger.info(f"\n💡 By Confidence:")
        for conf, data in sorted(stats['by_confidence'].items()):
            if data['total'] > 0:
                acc = (data['correct'] / data['total']) * 100
                logger.info(f"  {conf}-{conf+10}%: {acc:.1f}% ({data['correct']}/{data['total']})")
        
        # 2. Optymalizuj
        if stats['verified_24h'] >= 50:  # Min 50 zweryfikowanych
            changes = self.optimize_thresholds(stats)
            
            # Zapisz wyniki
            result = {
                'timestamp': datetime.now().isoformat(),
                'stats': stats,
                'changes': changes,
                'new_config': self.config
            }
            
            # Append do historii
            history = []
            try:
                with open(self.results_file, 'r') as f:
                    history = json.load(f)
            except:
                pass
            
            history.append(result)
            
            with open(self.results_file, 'w') as f:
                json.dump(history[-10:], f, indent=2)  # Keep last 10
            
        else:
            logger.info(f"\n⏳ Not enough data yet ({stats['verified_24h']}/50 verified)")
            logger.info("   Waiting for more results...")
        
        logger.info("\n" + "="*60)
        logger.info("✅ Optimization cycle complete")
        logger.info("="*60)

if __name__ == '__main__':
    optimizer = MasterOptimizer()
    optimizer.run_optimization()
