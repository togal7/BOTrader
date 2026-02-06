"""
Alert Queue - Communication between Main Bot and Alert Worker
Simple file-based queue using JSON
"""

import json
import os
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

class AlertQueue:
    """Simple file-based queue for alert communication"""
    
    def __init__(self, queue_dir='alert_queue'):
        self.queue_dir = Path(queue_dir)
        self.queue_dir.mkdir(exist_ok=True)
        
        # Subdirectories
        self.pending_dir = self.queue_dir / 'pending'
        self.processing_dir = self.queue_dir / 'processing'
        self.completed_dir = self.queue_dir / 'completed'
        
        for d in [self.pending_dir, self.processing_dir, self.completed_dir]:
            d.mkdir(exist_ok=True)
    
    def add_alert_to_send(self, user_id, alert_data):
        """
        Add alert to queue to be sent by main bot
        
        Args:
            user_id: User ID to send alert to
            alert_data: {
                'type': 'big_gain' | 'overbought' | etc,
                'symbol': 'BTC/USDT',
                'message': 'Alert message text',
                'timestamp': ISO datetime
            }
        """
        alert_id = f"alert_{user_id}_{datetime.now().timestamp()}"
        filepath = self.pending_dir / f"{alert_id}.json"
        
        data = {
            'user_id': user_id,
            'alert_data': alert_data,
            'created_at': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"✅ Alert queued: {alert_id}")
            return alert_id
        except Exception as e:
            logger.error(f"Failed to queue alert: {e}")
            return None
    
    def get_pending_alerts(self, limit=10):
        """
        Get pending alerts to send (called by main bot)
        
        Returns:
            List of (filepath, alert_data) tuples
        """
        pending_files = sorted(self.pending_dir.glob('*.json'))[:limit]
        alerts = []
        
        for filepath in pending_files:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                alerts.append((filepath, data))
            except Exception as e:
                logger.error(f"Failed to read {filepath}: {e}")
                continue
        
        return alerts
    
    def mark_alert_processing(self, filepath):
        """Move alert to processing directory"""
        try:
            new_path = self.processing_dir / filepath.name
            filepath.rename(new_path)
            return new_path
        except Exception as e:
            logger.error(f"Failed to mark processing: {e}")
            return filepath
    
    def mark_alert_completed(self, filepath, success=True):
        """Move alert to completed directory"""
        try:
            new_path = self.completed_dir / filepath.name
            filepath.rename(new_path)
            logger.info(f"Alert completed: {filepath.name}")
        except Exception as e:
            logger.error(f"Failed to mark completed: {e}")
    
    def cleanup_old_completed(self, hours=24):
        """Remove completed alerts older than X hours"""
        from datetime import timedelta
        cutoff = datetime.now() - timedelta(hours=hours)
        
        for filepath in self.completed_dir.glob('*.json'):
            try:
                mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                if mtime < cutoff:
                    filepath.unlink()
                    logger.info(f"Cleaned up old alert: {filepath.name}")
            except Exception as e:
                logger.error(f"Cleanup error: {e}")
    
    def add_settings_update(self, user_id, settings):
        """
        Signal that user settings changed (for worker to reload)
        
        Args:
            user_id: User ID
            settings: New alert settings dict
        """
        filepath = self.queue_dir / 'settings_updates.json'
        
        try:
            # Read existing
            if filepath.exists():
                with open(filepath, 'r') as f:
                    updates = json.load(f)
            else:
                updates = {}
            
            # Add update
            updates[str(user_id)] = {
                'settings': settings,
                'updated_at': datetime.now().isoformat()
            }
            
            # Write back
            with open(filepath, 'w') as f:
                json.dump(updates, f, indent=2)
            
            logger.info(f"Settings update queued for user {user_id}")
        except Exception as e:
            logger.error(f"Failed to queue settings update: {e}")
    
    def get_settings_updates(self):
        """Get all pending settings updates (called by worker)"""
        filepath = self.queue_dir / 'settings_updates.json'
        
        try:
            if not filepath.exists():
                return {}
            
            with open(filepath, 'r') as f:
                updates = json.load(f)
            
            # Clear file after reading
            filepath.unlink()
            
            return updates
        except Exception as e:
            logger.error(f"Failed to get settings updates: {e}")
            return {}
    
    def get_stats(self):
        """Get queue statistics"""
        return {
            'pending': len(list(self.pending_dir.glob('*.json'))),
            'processing': len(list(self.processing_dir.glob('*.json'))),
            'completed': len(list(self.completed_dir.glob('*.json')))
        }

# Global instance
alert_queue = AlertQueue()

