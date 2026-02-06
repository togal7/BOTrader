"""
AI Signals Tracker - System zbierania i weryfikacji sygnałów AI
Zapisuje każdy sygnał i sprawdza jego trafność po określonym czasie
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

SIGNALS_DB_FILE = 'ai_signals_history.json'
RESULTS_DB_FILE = 'ai_signals_results.json'

class AISignalsTracker:
    """Tracks AI signals and their outcomes"""
    
    def __init__(self):
        self.signals_db = self._load_db(SIGNALS_DB_FILE)
        self.results_db = self._load_db(RESULTS_DB_FILE)
    
    def _load_db(self, filename):
        """Load database from JSON file"""
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading {filename}: {e}")
                return {}
        return {}
    
    def _save_db(self, data, filename):
        """Save database to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving {filename}: {e}")
    
    def record_signal(
        self,
        symbol: str,
        exchange: str,
        timeframe: str,
        signal: str,
        confidence: int,
        price: float,
        indicators: Dict,
        ai_response: str,
        user_id: int = None,
        source: str = 'unknown',
        ai_mode: str = 'unknown'
    ) -> str:
        """
        Record a new AI signal
        
        Returns: signal_id for tracking
        """
        timestamp = datetime.now().isoformat()
        signal_id = f"{symbol}_{exchange}_{int(time.time())}"
        
        signal_data = {
            'signal_id': signal_id,
            'timestamp': timestamp,
            'symbol': symbol,
            'exchange': exchange,
            'timeframe': timeframe,
            'signal': signal,  # BUY/SELL/HOLD/WAIT
            'confidence': confidence,
            'entry_price': price,
            'source': source,  # manual, auto, extreme, search, callback
            'ai_mode': ai_mode,  # fast, accurate, auto
            'indicators': {
                'rsi': indicators.get('rsi', 0),
                'ema_cross': indicators.get('ema_cross', False),
                'macd_signal': indicators.get('macd_signal', 'neutral'),
                'macd_histogram': indicators.get('macd_histogram', 0),
                'volume_ratio': indicators.get('volume_ratio', 1.0),
                'bollinger_position': indicators.get('bollinger_position', 'middle')
            },
            'ai_full_response': ai_response[:1000],  # Pierwsze 1000 znaków
            'user_id': user_id,
            'checked_24h': False,
            'checked_48h': False,
            'checked_7d': False
        }
        
        # Zapisz do bazy
        self.signals_db[signal_id] = signal_data
        self._save_db(self.signals_db, SIGNALS_DB_FILE)
        
        logger.info(f"✅ Recorded signal: {signal_id} - {signal} @ ${price}")
        
        return signal_id
    
    def check_signal_outcome(self, signal_id: str, current_price: float, hours_elapsed: int):
        """
        Check if signal was correct after X hours
        
        Args:
            signal_id: ID sygnału
            current_price: Aktualna cena
            hours_elapsed: Ile godzin minęło (24, 48, 168)
        """
        if signal_id not in self.signals_db:
            return
        
        signal = self.signals_db[signal_id]
        entry_price = signal.get('entry', signal.get('entry_price', 0))
        signal_type = signal['signal']
        
        # Oblicz zmianę ceny
        price_change_pct = ((current_price - entry_price) / entry_price) * 100
        
        # Określ czy sygnał był trafny
        correct = False
        if signal_type == 'BUY' and price_change_pct > 0:
            correct = True
        elif signal_type == 'SELL' and price_change_pct < 0:
            correct = True
        elif signal_type in ['HOLD', 'WAIT'] and abs(price_change_pct) < 2:
            correct = True
        
        # Zapisz wynik
        result_key = f"{hours_elapsed}h"
        
        if signal_id not in self.results_db:
            self.results_db[signal_id] = {}
        
        self.results_db[signal_id][result_key] = {
            'timestamp': datetime.now().isoformat(),
            'current_price': current_price,
            'entry_price': entry_price,
            'price_change_pct': round(price_change_pct, 2),
            'correct': correct,
            'confidence': signal['confidence']
        }
        
        # Oznacz jako sprawdzone
        if hours_elapsed == 24:
            signal['checked_24h'] = True
        elif hours_elapsed == 48:
            signal['checked_48h'] = True
        elif hours_elapsed == 168:  # 7 dni
            signal['checked_7d'] = True
        
        self._save_db(self.signals_db, SIGNALS_DB_FILE)
        self._save_db(self.results_db, RESULTS_DB_FILE)
        
        logger.info(f"✅ Checked {signal_id} after {hours_elapsed}h: {'✅ CORRECT' if correct else '❌ WRONG'}")
    
    def get_signals_to_check(self, hours: int) -> List[Dict]:
        """
        Get signals that need to be checked after X hours
        
        Args:
            hours: 24, 48, or 168 (7 days)
        """
        to_check = []
        now = datetime.now()
        
        check_key = {
            24: 'checked_24h',
            48: 'checked_48h',
            168: 'checked_7d'
        }.get(hours)
        
        if not check_key:
            return []
        
        for signal_id, signal in self.signals_db.items():
            if signal.get(check_key, False):
                continue  # Already checked
            
            signal_time = datetime.fromisoformat(signal['timestamp'])
            elapsed = (now - signal_time).total_seconds() / 3600
            
            if elapsed >= hours:
                to_check.append(signal)
        
        return to_check
    
    def get_accuracy_stats(self, timeframe: str = '24h') -> Dict:
        """
        Calculate accuracy statistics
        
        Args:
            timeframe: '24h', '48h', or '7d'
        """
        total = 0
        correct = 0
        by_signal = {'BUY': {'total': 0, 'correct': 0}, 
                     'SELL': {'total': 0, 'correct': 0},
                     'HOLD': {'total': 0, 'correct': 0},
                     'WAIT': {'total': 0, 'correct': 0}}
        
        for signal_id, results in self.results_db.items():
            if timeframe not in results:
                continue
            
            result = results[timeframe]
            signal_data = self.signals_db.get(signal_id, {})
            signal_type = signal_data.get('direction', 'NEUTRAL')
            
            total += 1
            signal_data = self.signals_db[signal_id].get('signal', {})
            signal_type = signal_data.get('direction', 'NEUTRAL') if isinstance(signal_data, dict) else signal_data
            
            if result['correct']:
                correct += 1
                by_signal[signal_type]['correct'] += 1
        
        accuracy = (correct / total * 100) if total > 0 else 0
        
        stats = {
            'timeframe': timeframe,
            'total_signals': total,
            'correct_signals': correct,
            'accuracy_pct': round(accuracy, 2),
            'by_signal_type': {}
        }
        
        for sig_type, counts in by_signal.items():
            if counts['total'] > 0:
                acc = (counts['correct'] / counts['total']) * 100
                stats['by_signal_type'][sig_type] = {
                    'total': counts['total'],
                    'correct': counts['correct'],
                    'accuracy_pct': round(acc, 2)
                }
        
        return stats
    
    def export_for_analysis(self, output_file: str = 'ai_analysis_export.json'):
        """
        Export all data for external analysis
        """
        export_data = {
            'generated_at': datetime.now().isoformat(),
            'total_signals': len(self.signals_db),
            'signals': self.signals_db,
            'results': self.results_db,
            'stats_24h': self.get_accuracy_stats('24h'),
            'stats_48h': self.get_accuracy_stats('48h'),
            'stats_7d': self.get_accuracy_stats('7d')
        }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"✅ Exported data to {output_file}")
        return output_file

# Global instance
tracker = AISignalsTracker()

