"""
Alert Worker - Standalone process for scanning market and triggering alerts
Runs independently from main bot
"""

import asyncio
import logging
from database import Database
import sys
from datetime import datetime, timedelta
from alert_queue import alert_queue
from database import db
from exchange_api import exchange_api
from central_ai_analyzer import CentralAIAnalyzer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('alert_worker.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('alert_worker')

class AlertWorker:
    """Standalone alert scanner worker"""
    
    def __init__(self):
        self.db = Database()
        self.running = False
        self.analyzer = CentralAIAnalyzer()
        self.last_alert_time = {}  # {user_id: {symbol: timestamp}}
        logger.info("🔔 Alert Worker initialized")
    
    async def start(self):
        """Start the worker loop"""
        self.running = True
        logger.info("🚀 Alert Worker starting...")
        
        # Main loop
        asyncio.create_task(self.worker_loop())
        
        # Keep running
        while self.running:
            await asyncio.sleep(1)
    
    async def stop(self):
        """Stop the worker"""
        self.running = False
        logger.info("🛑 Alert Worker stopping...")
    
    async def worker_loop(self):
        """Main worker loop - scans all users"""
        while self.running:
            try:
                # Check for settings updates
                await self.check_settings_updates()
                
                # Get all users with alerts enabled
                users_to_scan = self.get_users_with_alerts()
                
                if not users_to_scan:
                    logger.info("No users with alerts enabled, waiting...")
                    await asyncio.sleep(60)
                    continue
                
                logger.info(f"📊 Scanning for {len(users_to_scan)} users with alerts")
                
                # Scan each user (with rate limiting)
                for user_id, user_data in users_to_scan.items():
                    try:
                        await self.scan_for_user(user_id, user_data)
                    except Exception as e:
                        logger.error(f"Error scanning user {user_id}: {e}")
                        continue
                    
                    # Small delay between users (rate limiting)
                    await asyncio.sleep(2)
                
                # Cleanup old completed alerts
                alert_queue.cleanup_old_completed(hours=24)
                
                # Wait before next full scan
                logger.info("✅ Scan cycle complete, waiting 5 minutes...")
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Worker loop error: {e}")
                await asyncio.sleep(60)
    
    async def check_settings_updates(self):
        """Check if any user updated their settings"""
        updates = alert_queue.get_settings_updates()
        
        if updates:
            logger.info(f"📥 Received {len(updates)} settings updates")
            # Settings are in DB, just log that we noticed the change
            for user_id in updates:
                logger.info(f"  User {user_id} settings updated")
    
    def get_users_with_alerts(self):
        """Get all users that have at least one alert enabled"""
        all_users = db.get_all_users()
        users_with_alerts = {}
        
        for user_id, user_data in all_users.items():
            settings = user_data.get('alert_settings', {})
            
            # Check if any alert is enabled
            enabled_count = sum(
                1 for key, value in settings.items() 
                if key.endswith('_enabled') and value == 1
            )
            
            if enabled_count > 0:
                users_with_alerts[user_id] = user_data
        
        return users_with_alerts
    
    async def scan_for_user(self, user_id, user_data):
        """Scan market for one user's alerts"""
        settings = user_data.get('alert_settings', {})
        
        # Check scan frequency
        last_scan = user_data.get('last_alert_scan')
        if last_scan:
            freq_minutes = self.get_frequency_minutes(settings.get('scan_frequency', '15m'))
            next_scan = datetime.fromisoformat(last_scan) + timedelta(minutes=freq_minutes)
            
            if datetime.now() < next_scan:
                return  # Too soon
        
        exchange = user_data.get('selected_exchange', 'mexc').lower()
        
        # Get symbols to scan
        try:
            symbols = await exchange_api.get_symbols(exchange)
        except Exception as e:
            logger.error(f"Failed to get symbols for {exchange}: {e}")
            return
        
        # Limit scan range (max 100 symbols per user)
        scan_range = min(settings.get('scan_range', 50), 100, len(symbols))
        symbols_to_scan = list(symbols)[:scan_range]
        
        logger.info(f"🔍 User {user_id}: Scanning {scan_range} symbols on {exchange}")
        
        # BATCH PROCESSING - scan in parallel batches of 20
        batch_size = 20
        for i in range(0, len(symbols_to_scan), batch_size):
            batch = symbols_to_scan[i:i+batch_size]
            
            # Process batch in parallel
            tasks = [
                self.check_symbol_alerts(user_id, symbol, exchange, settings)
                for symbol in batch
            ]
            
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # Small delay between batches
            await asyncio.sleep(1)
        
        # Update last scan time
        user_data['last_alert_scan'] = datetime.now().isoformat()
        db.update_user(user_id, user_data)
    
    def get_frequency_minutes(self, freq):
        """Convert frequency string to minutes"""
        freq_map = {
            '5m': 5,
            '15m': 15,
            '30m': 30,
            '1h': 60
        }
        return freq_map.get(freq, 15)
    
    async def check_symbol_alerts(self, user_id, symbol, exchange, settings):
        """Check all alert types for one symbol"""
        try:
            # Anti-spam check
            if not self.should_send_alert(user_id, symbol):
                return
            
            timeframe = settings.get('alert_timeframe', '1h')
            
            # Get ticker
            ticker = await exchange_api.get_ticker(symbol, exchange)
            if not ticker:
                return
            
            # Check each alert type
            alerts_to_send = []
            
            # 1. Big gains/losses
            if settings.get('big_gains_enabled') or settings.get('big_losses_enabled'):
                change_24h = ticker.get('percentage', 0)
                gain_threshold = settings.get('gain_threshold', 15)
                loss_threshold = settings.get('loss_threshold', 15)
                
                if settings.get('big_gains_enabled') and change_24h >= gain_threshold:
                    alerts_to_send.append({
                        'type': 'big_gain',
                        'symbol': symbol,
                        'message': f"🚀 DUŻY WZROST: {symbol}\n💰 Cena: ${ticker['last']}\n📈 Zmiana 24h: +{change_24h:.2f}%",
                        'timestamp': datetime.now().isoformat()
                    })
                
                if settings.get('big_losses_enabled') and change_24h <= -loss_threshold:
                    alerts_to_send.append({
                        'type': 'big_loss',
                        'symbol': symbol,
                        'message': f"📉 DUŻY SPADEK: {symbol}\n💰 Cena: ${ticker['last']}\n📉 Zmiana 24h: {change_24h:.2f}%",
                        'timestamp': datetime.now().isoformat()
                    })
            
            # 2. Sudden changes (requires OHLCV)
            if settings.get('sudden_change_enabled'):
                sudden_timeframe = settings.get('sudden_timeframe', '15m')
                sudden_threshold = settings.get('sudden_threshold', 5)
                
                try:
                    ohlcv = await exchange_api.get_ohlcv(symbol, sudden_timeframe, exchange)
                    if ohlcv and len(ohlcv) >= 2:
                        prev_close = ohlcv[-2][4]
                        curr_close = ohlcv[-1][4]
                        change_pct = ((curr_close - prev_close) / prev_close) * 100
                        
                        if abs(change_pct) >= sudden_threshold:
                            direction = "WZROST" if change_pct > 0 else "SPADEK"
                            alerts_to_send.append({
                                'type': 'sudden_change',
                                'symbol': symbol,
                                'message': f"⚡ NAGŁA ZMIANA: {symbol}\n💰 Cena: ${ticker['last']}\n⚡ {direction}: {abs(change_pct):.2f}% w {sudden_timeframe}\n📊 {prev_close:.6f} → {curr_close:.6f}",
                                'timestamp': datetime.now().isoformat()
                            })
                except Exception as e:
                    logger.debug(f"Sudden change check failed for {symbol}: {e}")
            
            # 3. RSI-based alerts (overbought/oversold)
            if settings.get('overbought_enabled') or settings.get('oversold_enabled'):
                try:
                    # Get full analysis for RSI
                    analysis = await self.analyzer.analyze(symbol, timeframe, exchange)
                    
                    if analysis and 'technical' in analysis:
                        rsi = analysis['technical'].get('rsi', {}).get('14')
                        
                        if rsi:
                            if settings.get('overbought_enabled') and rsi >= 70:
                                alerts_to_send.append({
                                    'type': 'overbought',
                                    'symbol': symbol,
                                    'message': f"🔴 WYKUPIENIE: {symbol}\n💰 Cena: ${ticker['last']}\n📊 RSI(14): {rsi:.1f}\n⚠️ Możliwa korekta",
                                    'timestamp': datetime.now().isoformat()
                                })
                            
                            if settings.get('oversold_enabled') and rsi <= 30:
                                alerts_to_send.append({
                                    'type': 'oversold',
                                    'symbol': symbol,
                                    'message': f"🟢 WYPRZEDANIE: {symbol}\n💰 Cena: ${ticker['last']}\n📊 RSI(14): {rsi:.1f}\n✅ Potencjalna okazja",
                                    'timestamp': datetime.now().isoformat()
                                })
                except Exception as e:
                    logger.debug(f"RSI check failed for {symbol}: {e}")
            
            # 4. AI signals
            if settings.get('ai_signals_enabled'):
                try:
                    analysis = await self.analyzer.analyze(symbol, timeframe, exchange)
                    
                    if analysis and 'signal' in analysis:
                        confidence = analysis['signal'].get('confidence', 0)
                        direction = analysis['signal'].get('direction')
                        min_confidence = settings.get('min_confidence', 70)
                        
                        if confidence >= min_confidence and direction in ['LONG', 'SHORT']:
                            alerts_to_send.append({
                                'type': 'ai_signal',
                                'symbol': symbol,
                                'message': f"🤖 SYGNAŁ AI: {symbol}\n🎯 Kierunek: {direction}\n💪 Pewność: {confidence}%\n💰 Cena: ${ticker['last']}",
                                'timestamp': datetime.now().isoformat()
                            })
                except Exception as e:
                    logger.debug(f"AI signal check failed for {symbol}: {e}")
            
            # Queue all alerts
            for alert_data in alerts_to_send:
                alert_queue.add_alert_to_send(user_id, alert_data)
                self.mark_alert_sent(user_id, symbol)
                logger.info(f"✅ Alert queued: {alert_data['type']} for user {user_id} - {symbol}")
        
        except Exception as e:
            logger.error(f"Error checking {symbol} for user {user_id}: {e}")
    
    def should_send_alert(self, user_id, symbol):
        """Anti-spam: max 1 alert per symbol per user per 15 minutes"""
        key = f"{user_id}_{symbol}"
        
        if key in self.last_alert_time:
            last_time = self.last_alert_time[key]
            if datetime.now() - last_time < timedelta(minutes=15):
                return False
        
        return True
    
    def mark_alert_sent(self, user_id, symbol):
        """Mark that alert was sent for this symbol"""
        key = f"{user_id}_{symbol}"
        self.last_alert_time[key] = datetime.now()

async def main():
    """Main entry point"""
    worker = AlertWorker()
    
    try:
        logger.info("=" * 60)
        logger.info("🔔 ALERT WORKER STARTING")
        logger.info("=" * 60)
        await worker.start()
    except KeyboardInterrupt:
        logger.info("\n⏹️  Keyboard interrupt received")
        await worker.stop()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
    finally:
        logger.info("👋 Alert Worker shutdown complete")

if __name__ == '__main__':
    asyncio.run(main())

