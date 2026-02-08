"""
Portfolio Manager - Core logic for tracking trading positions
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

PORTFOLIO_FILE = 'portfolio.json'

class PortfolioManager:
    """Manages user trading positions and portfolio stats"""
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load portfolio data from JSON"""
        if os.path.exists(PORTFOLIO_FILE):
            try:
                with open(PORTFOLIO_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading portfolio: {e}")
                return {}
        return {}
    
    def _save_data(self):
        """Save portfolio data to JSON"""
        try:
            with open(PORTFOLIO_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving portfolio: {e}")
    
    def add_position(
        self,
        user_id: int,
        symbol: str,
        position_type: str,  # LONG or SHORT
        entry: float,
        size: float,
        leverage: int = 1,
        tp1: Optional[float] = None,
        tp2: Optional[float] = None,
        tp3: Optional[float] = None,
        sl: Optional[float] = None
    ) -> str:
        """
        Add new position to portfolio
        Returns: position_id
        """
        user_id_str = str(user_id)
        
        # Initialize user data if needed
        if user_id_str not in self.data:
            self.data[user_id_str] = {
                'positions': {},
                'stats': {
                    'total_trades': 0,
                    'winning_trades': 0,
                    'losing_trades': 0,
                    'win_rate': 0,
                    'total_realized_pnl': 0,
                    'best_trade': 0,
                    'worst_trade': 0
                }
            }
        
        # Generate position ID
        pos_id = f"pos_{user_id}_{int(datetime.now().timestamp())}"
        
        # Calculate liquidation price
        liq_price = self._calculate_liquidation(entry, leverage, position_type)
        
        # Create position
        position = {
            'id': pos_id,
            'symbol': symbol,
            'type': position_type,
            'entry': entry,
            'size': size,
            'leverage': leverage,
            'tp1': tp1,
            'tp2': tp2,
            'tp3': tp3,
            'sl': sl,
            'liquidation': liq_price,
            'status': 'open',
            'opened_at': datetime.now().isoformat(),
            'closed_at': None,
            'close_price': None,
            'realized_pnl': None,
            'hit_targets': []  # Track which TPs were hit
        }
        
        self.data[user_id_str]['positions'][pos_id] = position
        self._save_data()
        
        logger.info(f"✅ Added position {pos_id} for user {user_id}")
        return pos_id
    
    def _calculate_liquidation(self, entry: float, leverage: int, pos_type: str) -> float:
        """Calculate liquidation price"""
        if leverage == 1:
            return 0  # No liquidation for spot
        
        # Simplified liquidation calculation (100% - maintenance margin)
        # Real exchanges use more complex formulas
        liq_distance = (100 / leverage) * 0.9  # 90% of max distance
        
        if pos_type == 'LONG':
            return entry * (1 - liq_distance / 100)
        else:  # SHORT
            return entry * (1 + liq_distance / 100)
    
    def calculate_pnl(
        self,
        position: Dict,
        current_price: float
    ) -> Dict:
        """
        Calculate PnL for position
        Returns: {pnl_usd, pnl_pct, status}
        """
        entry = position['entry']
        size = position['size']
        leverage = position['leverage']
        pos_type = position['type']
        
        # Calculate price change
        if pos_type == 'LONG':
            price_change_pct = ((current_price - entry) / entry) * 100
        else:  # SHORT
            price_change_pct = ((entry - current_price) / entry) * 100
        
        # Apply leverage
        pnl_pct = price_change_pct * leverage
        pnl_usd = (size * pnl_pct) / 100
        
        # Determine status
        if pnl_pct > 0:
            status = 'profit'
        elif pnl_pct < 0:
            status = 'loss'
        else:
            status = 'breakeven'
        
        # Check liquidation
        liq = position.get('liquidation', 0)
        if liq > 0:
            if pos_type == 'LONG' and current_price <= liq:
                status = 'liquidated'
                pnl_usd = -size  # Total loss
                pnl_pct = -100
            elif pos_type == 'SHORT' and current_price >= liq:
                status = 'liquidated'
                pnl_usd = -size
                pnl_pct = -100
        
        return {
            'pnl_usd': pnl_usd,
            'pnl_pct': pnl_pct,
            'status': status
        }
    
    def get_open_positions(self, user_id: int) -> List[Dict]:
        """Get all open positions for user"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return []
        
        positions = self.data[user_id_str]['positions']
        return [p for p in positions.values() if p['status'] == 'open']
    
    def get_position(self, user_id: int, pos_id: str) -> Optional[Dict]:
        """Get specific position"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return None
        
        return self.data[user_id_str]['positions'].get(pos_id)
    
    def close_position(
        self,
        user_id: int,
        pos_id: str,
        close_price: float,
        reason: str = 'manual'
    ) -> Dict:
        """
        Close position and update stats
        Returns: {success, pnl_usd, pnl_pct}
        """
        user_id_str = str(user_id)
        
        position = self.get_position(user_id, pos_id)
        if not position:
            return {'success': False, 'error': 'Position not found'}
        
        if position['status'] != 'open':
            return {'success': False, 'error': 'Position already closed'}
        
        # Calculate final PnL
        pnl_data = self.calculate_pnl(position, close_price)
        
        # Update position
        position['status'] = 'closed'
        position['closed_at'] = datetime.now().isoformat()
        position['close_price'] = close_price
        position['realized_pnl'] = pnl_data['pnl_usd']
        position['close_reason'] = reason
        
        # Update stats
        stats = self.data[user_id_str]['stats']
        stats['total_trades'] += 1
        stats['total_realized_pnl'] += pnl_data['pnl_usd']
        
        if pnl_data['pnl_usd'] > 0:
            stats['winning_trades'] += 1
            if pnl_data['pnl_usd'] > stats['best_trade']:
                stats['best_trade'] = pnl_data['pnl_usd']
        else:
            stats['losing_trades'] += 1
            if pnl_data['pnl_usd'] < stats['worst_trade']:
                stats['worst_trade'] = pnl_data['pnl_usd']
        
        # Recalculate win rate
        if stats['total_trades'] > 0:
            stats['win_rate'] = (stats['winning_trades'] / stats['total_trades']) * 100
        
        self._save_data()
        
        logger.info(f"✅ Closed position {pos_id}: PnL ${pnl_data['pnl_usd']:.2f}")
        
        return {
            'success': True,
            'pnl_usd': pnl_data['pnl_usd'],
            'pnl_pct': pnl_data['pnl_pct']
        }
    
    def get_stats(self, user_id: int) -> Dict:
        """Get portfolio statistics"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_realized_pnl': 0,
                'best_trade': 0,
                'worst_trade': 0
            }
        
        return self.data[user_id_str]['stats']
    
    def delete_position(self, user_id: int, pos_id: str) -> bool:
        """Delete position (for cleanup/mistakes)"""
        user_id_str = str(user_id)
        
        if user_id_str not in self.data:
            return False
        
        if pos_id in self.data[user_id_str]['positions']:
            del self.data[user_id_str]['positions'][pos_id]
            self._save_data()
            return True
        
        return False

# Global instance
portfolio = PortfolioManager()

