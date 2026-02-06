"""
A/B Testing Framework - Testuje różne strategie równocześnie
Automatycznie wybiera najlepszą na podstawie wyników
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging
import random

logger = logging.getLogger(__name__)

AB_TESTS_DB = 'ab_tests.json'

class ABTestingFramework:
    """Manages A/B testing of different trading strategies"""
    
    def __init__(self):
        self.tests = self._load_tests()
        self.active_test = None
    
    def _load_tests(self):
        """Load A/B test data"""
        if os.path.exists(AB_TESTS_DB):
            try:
                with open(AB_TESTS_DB, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading A/B tests: {e}")
        return {
            'active_tests': [],
            'completed_tests': [],
            'current_winner': None
        }
    
    def _save_tests(self):
        """Save A/B test data"""
        with open(AB_TESTS_DB, 'w') as f:
            json.dump(self.tests, f, indent=2)
    
    def create_test(
        self, 
        test_name: str,
        variants: List[Dict],
        traffic_split: Optional[List[float]] = None,
        min_samples: int = 50
    ) -> str:
        """
        Create a new A/B test
        
        Args:
            test_name: Name of test (e.g., "RSI_Threshold_Test")
            variants: List of variant configs, e.g.:
                [
                    {'name': 'A', 'rsi_buy': 30, 'rsi_sell': 70},
                    {'name': 'B', 'rsi_buy': 35, 'rsi_sell': 65}
                ]
            traffic_split: % of signals for each variant (default: equal split)
            min_samples: Minimum samples before declaring winner
        
        Returns: test_id
        """
        test_id = f"{test_name}_{int(datetime.now().timestamp())}"
        
        if traffic_split is None:
            traffic_split = [1.0 / len(variants)] * len(variants)
        
        test = {
            'test_id': test_id,
            'test_name': test_name,
            'created_at': datetime.now().isoformat(),
            'status': 'active',
            'variants': variants,
            'traffic_split': traffic_split,
            'min_samples': min_samples,
            'results': {v['name']: {'signals': [], 'correct': 0, 'total': 0} for v in variants}
        }
        
        self.tests['active_tests'].append(test)
        self._save_tests()
        
        logger.info(f"✅ Created A/B test: {test_name}")
        
        return test_id
    
    def assign_variant(self, test_id: str) -> Optional[Dict]:
        """
        Assign a variant for this signal based on traffic split
        
        Returns: Variant config or None
        """
        test = self._get_test(test_id)
        
        if not test or test['status'] != 'active':
            return None
        
        # Random assignment based on traffic split
        rand = random.random()
        cumulative = 0
        
        for i, variant in enumerate(test['variants']):
            cumulative += test['traffic_split'][i]
            if rand <= cumulative:
                return variant
        
        # Fallback to first variant
        return test['variants'][0]
    
    def record_test_result(
        self,
        test_id: str,
        variant_name: str,
        signal_id: str,
        was_correct: bool
    ):
        """Record result for a specific variant"""
        
        test = self._get_test(test_id)
        
        if not test:
            return
        
        # Update results
        if variant_name not in test['results']:
            test['results'][variant_name] = {'signals': [], 'correct': 0, 'total': 0}
        
        test['results'][variant_name]['signals'].append(signal_id)
        test['results'][variant_name]['total'] += 1
        
        if was_correct:
            test['results'][variant_name]['correct'] += 1
        
        # Check if we have enough samples to declare winner
        min_samples = test.get('min_samples', 50)
        
        total_samples = sum(r['total'] for r in test['results'].values())
        
        if total_samples >= min_samples:
            self._evaluate_test(test_id)
        
        self._save_tests()
    
    def _evaluate_test(self, test_id: str):
        """Evaluate test and declare winner if statistically significant"""
        
        test = self._get_test(test_id)
        
        if not test:
            return
        
        # Calculate accuracy for each variant
        variant_stats = {}
        
        for variant_name, results in test['results'].items():
            total = results['total']
            correct = results['correct']
            
            if total > 0:
                accuracy = (correct / total) * 100
                variant_stats[variant_name] = {
                    'accuracy': accuracy,
                    'total': total,
                    'correct': correct
                }
        
        # Find winner (highest accuracy with enough samples)
        winner = max(variant_stats.items(), key=lambda x: x[1]['accuracy'])
        
        winner_name = winner[0]
        winner_accuracy = winner[1]['accuracy']
        
        # Check if statistically significant (>5% difference from second best)
        sorted_variants = sorted(variant_stats.items(), key=lambda x: x[1]['accuracy'], reverse=True)
        
        if len(sorted_variants) > 1:
            second_best_accuracy = sorted_variants[1][1]['accuracy']
            difference = winner_accuracy - second_best_accuracy
            
            if difference > 5.0:  # 5% threshold
                # Declare winner!
                test['status'] = 'completed'
                test['winner'] = winner_name
                test['completed_at'] = datetime.now().isoformat()
                test['final_stats'] = variant_stats
                
                # Move to completed tests
                self.tests['active_tests'] = [t for t in self.tests['active_tests'] if t['test_id'] != test_id]
                self.tests['completed_tests'].append(test)
                
                # Update current winner
                self.tests['current_winner'] = {
                    'test_name': test['test_name'],
                    'variant': winner_name,
                    'config': next(v for v in test['variants'] if v['name'] == winner_name),
                    'accuracy': winner_accuracy
                }
                
                logger.info(f"🏆 A/B Test '{test['test_name']}' WINNER: {winner_name} ({winner_accuracy:.2f}% accuracy)")
                
                self._save_tests()
    
    def _get_test(self, test_id: str) -> Optional[Dict]:
        """Get test by ID"""
        for test in self.tests['active_tests']:
            if test['test_id'] == test_id:
                return test
        
        for test in self.tests['completed_tests']:
            if test['test_id'] == test_id:
                return test
        
        return None
    
    def get_active_tests(self) -> List[Dict]:
        """Get all active tests"""
        return self.tests.get('active_tests', [])
    
    def get_current_winner(self) -> Optional[Dict]:
        """Get current winning strategy"""
        return self.tests.get('current_winner')
    
    def get_test_stats(self, test_id: str) -> Dict:
        """Get statistics for a specific test"""
        
        test = self._get_test(test_id)
        
        if not test:
            return {}
        
        stats = {
            'test_name': test['test_name'],
            'status': test['status'],
            'variants': []
        }
        
        for variant_name, results in test['results'].items():
            total = results['total']
            correct = results['correct']
            accuracy = (correct / total * 100) if total > 0 else 0
            
            stats['variants'].append({
                'name': variant_name,
                'total_signals': total,
                'correct': correct,
                'accuracy': round(accuracy, 2)
            })
        
        # Sort by accuracy
        stats['variants'] = sorted(stats['variants'], key=lambda x: x['accuracy'], reverse=True)
        
        return stats
    
    def create_default_tests(self):
        """Create some default A/B tests to start with"""
        
        # Test 1: RSI Thresholds
        self.create_test(
            test_name='RSI_Thresholds',
            variants=[
                {'name': 'Conservative', 'rsi_buy': 25, 'rsi_sell': 75},
                {'name': 'Standard', 'rsi_buy': 30, 'rsi_sell': 70},
                {'name': 'Aggressive', 'rsi_buy': 35, 'rsi_sell': 65}
            ],
            min_samples=30
        )
        
        # Test 2: Volume Threshold
        self.create_test(
            test_name='Volume_Threshold',
            variants=[
                {'name': 'Low', 'volume_min': 1.2},
                {'name': 'Medium', 'volume_min': 1.5},
                {'name': 'High', 'volume_min': 2.0}
            ],
            min_samples=30
        )
        
        # Test 3: Confidence Calculation Method
        self.create_test(
            test_name='Confidence_Method',
            variants=[
                {'name': 'Conservative', 'base_multiplier': 0.8},
                {'name': 'Standard', 'base_multiplier': 1.0},
                {'name': 'Optimistic', 'base_multiplier': 1.2}
            ],
            min_samples=30
        )
        
        logger.info("✅ Created 3 default A/B tests")

# Global instance
ab_tester = ABTestingFramework()

