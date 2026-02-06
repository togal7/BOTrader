# Tworzymy nowy plik alert_scanner.py

scanner_code = """import asyncio
import logging
from datetime import datetime, timedelta
from database import db
from exchange_api import exchange_api
from ai_trader import ai_trader

logger = logging.getLogger(__name__)

class AlertScanner:
    def __init__(self, bot_application):
        self.app = bot_application
        self.running = False
        self.last_alerts = {}  # Anti-spam: {user_id: {symbol: timestamp}}
        
    async def start(self):
        \"\"\"Start background scanner\"\"\"
        self.running = True
        logger.info("🔔 Alert Scanner started")
        
        # Run scanner loop
        asyncio.create_task(self.scanner_loop())
    
    async def stop(self):
        \"\"\"Stop scanner\"\"\"
        self.running = False
        logger.info("🔔 Alert Scanner stopped")
    
    async def scanner_loop(self):
        \"\"\"Main scanner loop\"\"\"
        while self.running:
            try:
                # Get all users with active alerts
                all_users = db.get_all_users()
                
                for user_id, user_data in all_users.items():
                    try:
                        await self.scan_for_user(int(user_id), user_data)
                    except Exception as e:
                        logger.error(f"Error scanning for user {user_id}: {e}")
                
                # Wait before next scan (minimum 5 minutes to avoid API spam)
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Scanner loop error: {e}")
                await asyncio.sleep(60)
    
    async def scan_for_user(self, user_id, user_data):
        \"\"\"Scan market for one user's alerts\"\"\"
        settings = db.get_alert_settings(user_id)
        
        # Check if any alerts are enabled
        if not any([
            settings['oversold_enabled'],
            settings['overbought_enabled'],
            settings['big_gains_enabled'],
            settings['big_losses_enabled'],
            settings['ai_signals_enabled'],
            settings['volume_spike_enabled'],
            settings['macd_cross_enabled'],
            settings['ema_cross_enabled']
        ]):
            return  # No alerts enabled for this user
        
        # Check scan frequency
        last_scan = user_data.get('last_alert_scan')
        if last_scan:
            last_time = datetime.fromisoformat(last_scan)
            freq_minutes = self.get_frequency_minutes(settings['scan_frequency'])
            
            if datetime.now() - last_time < timedelta(minutes=freq_minutes):
                return  # Too soon to scan again
        
        # Update last scan time
        user_data['last_alert_scan'] = datetime.now().isoformat()
        db.update_user(user_id, user_data)
        
        # Get symbols to scan
        exchange = user_data.get('selected_exchange', 'mexc')
        symbols = await exchange_api.get_symbols(exchange)
        
        scan_range = min(settings['scan_range'], len(symbols))
        symbols_to_scan = list(symbols)[:scan_range]
        
        logger.info(f"Scanning {scan_range} symbols for user {user_id}")
        
        # Scan each symbol
        for symbol in symbols_to_scan:
            try:
                await self.check_symbol_alerts(user_id, symbol, exchange, settings)
            except Exception as e:
                logger.error(f"Error checking {symbol}: {e}")
                continue
"""

with open('alert_scanner.py', 'w') as f:
    f.write(scanner_code)

print("✅ Created alert_scanner.py - PART 1")

