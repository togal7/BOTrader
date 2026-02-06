import asyncio
import logging
from datetime import datetime, timedelta
from database import db
from exchange_api import exchange_api
from central_ai_analyzer import central_analyzer

logger = logging.getLogger(__name__)

class AlertScanner:
    def __init__(self, bot_application):
        self.app = bot_application
        self.running = False
        self.last_alerts = {}  # Anti-spam: {user_id: {symbol: timestamp}}
        
    async def start(self):
        """Start background scanner"""
        self.running = True
        logger.info("🔔 Alert Scanner started")
        
        # Run scanner loop
        asyncio.create_task(self.scanner_loop())
    
    async def stop(self):
        """Stop scanner"""
        self.running = False
        logger.info("🔔 Alert Scanner stopped")
    
    async def scanner_loop(self):
        """Main scanner loop"""
        while self.running:
            try:
                # Get all users with active alerts
                all_users = db.get_all_users()
                
                for user_id, user_data in list(all_users.items()):
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
        """Scan market for one user's alerts"""
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
        
        # Anti-spam check
        if not self.should_send_alert(user_id, symbol):
            return
        
        timeframe = settings.get('alert_timeframe', settings.get('scan_timeframe', '1h'))
        
        # Get ticker
        ticker = await exchange_api.get_ticker(symbol, exchange)
        if not ticker:
            return
        
        current_price = ticker.get('last', 0)
        change_24h = ticker.get('percentage', 0)
        
        # Check price change alerts
        if settings['big_gains_enabled'] and change_24h > settings['gain_threshold']:
            await self.send_alert(
                user_id, 'big_gain', symbol,
                f"🚀 DUŻY WZROST: {symbol.replace(':USDT', '')}\n"
                f"💰 Cena: ${current_price}\n"
                f"📈 Zmiana 24h: +{change_24h:.2f}%"
            )
            # Removed return - continue checking other alerts
        
        if settings['big_losses_enabled'] and change_24h < -settings['loss_threshold']:
            await self.send_alert(
                user_id, 'big_loss', symbol,
                f"📉 DUŻY SPADEK: {symbol.replace(':USDT', '')}\n"
                f"💰 Cena: ${current_price}\n"
                f"📉 Zmiana 24h: {change_24h:.2f}%"
            )
            # Removed return - continue checking other alerts
        
        # Check sudden price changes (on custom timeframe)
        if settings.get('sudden_change_enabled', 0):
            try:
                sudden_tf = settings.get('sudden_timeframe', '15m')
                sudden_threshold = settings.get('sudden_threshold', 5)
                
                # Get OHLCV for sudden timeframe
                ohlcv = await exchange_api.get_ohlcv(symbol, exchange, sudden_tf)
                
                if ohlcv and len(ohlcv) >= 2:
                    # Compare current price with price from previous candle
                    current_close = ohlcv[-1][4]
                    previous_close = ohlcv[-2][4]
                    
                    # Calculate % change
                    sudden_change = ((current_close - previous_close) / previous_close) * 100
                    
                    # Check if exceeds threshold
                    if abs(sudden_change) >= sudden_threshold:
                        direction = "WZROST" if sudden_change > 0 else "SPADEK"
                        emoji = "🚀" if sudden_change > 0 else "📉"
                        
                        await self.send_alert(
                            user_id, 'sudden_change', symbol,
                            f"{emoji} NAGŁA ZMIANA: {symbol.replace(':USDT', '')}\n"
                            f"💰 Cena: ${current_price}\n"
                            f"⚡ {direction}: {abs(sudden_change):.2f}% w {sudden_tf}\n"
                            f"📊 {previous_close:.6f} → {current_close:.6f}"
                        )
                        # Continue checking other alerts (no return)
                        
            except Exception as e:
                logger.error(f"Sudden change check error for {symbol}: {e}")
        
        # For technical indicators, we need OHLCV data
        if any([
            settings['oversold_enabled'],
            settings['overbought_enabled'],
            settings['volume_spike_enabled'],
            settings['macd_cross_enabled'],
            settings['ema_cross_enabled'],
            settings['ai_signals_enabled']
        ]):
            # Get full analysis
            try:
                analysis = await central_analyzer.analyze_pair_full(symbol, exchange, timeframe)
                
                if not analysis:
                    return
                
                # Check RSI alerts
                rsi = analysis.get('rsi')
                if rsi:
                    if settings['oversold_enabled'] and rsi < 20:
                        await self.send_alert(
                            user_id, 'oversold', symbol,
                            f"🔥 OVERSOLD: {symbol.replace(':USDT', '')}\n"
                            f"💰 Cena: ${current_price}\n"
                            f"📊 RSI: {rsi:.1f} (OVERSOLD!)\n"
                            f"⏱ {timeframe} | 🌐 {exchange.upper()}"
                        )
                        return
                    
                    if settings['overbought_enabled'] and rsi > 80:
                        await self.send_alert(
                            user_id, 'overbought', symbol,
                            f"💎 OVERBOUGHT: {symbol.replace(':USDT', '')}\n"
                            f"💰 Cena: ${current_price}\n"
                            f"📊 RSI: {rsi:.1f} (OVERBOUGHT!)\n"
                            f"⏱ {timeframe} | 🌐 {exchange.upper()}"
                        )
                        return
                
                # Check Volume Spike
                if settings['volume_spike_enabled']:
                    volume_ratio = analysis.get('volume_ratio', 0)
                    if volume_ratio > settings['volume_multiplier']:
                        await self.send_alert(
                            user_id, 'volume_spike', symbol,
                            f"🔥 VOLUME SPIKE: {symbol.replace(':USDT', '')}\n"
                            f"💰 Cena: ${current_price}\n"
                            f"📊 Volume: {volume_ratio:.1f}x średniej\n"
                            f"⏱ {timeframe} | 🌐 {exchange.upper()}"
                        )
                        return
                
                # Check AI Signals
                if settings['ai_signals_enabled']:
                    confidence = analysis.get('confidence', 0)
                    signal = analysis.get('signal', 'NEUTRAL')
                    
                    if confidence >= settings['min_confidence'] and signal != 'NEUTRAL':
                        await self.send_alert(
                            user_id, 'ai_signal', symbol,
                            f"🤖 SYGNAŁ AI {signal}: {symbol.replace(':USDT', '')}\n"
                            f"💰 Cena: ${current_price}\n"
                            f"🎯 Confidence: {confidence}%\n"
                            f"📊 RSI: {rsi:.1f}\n"
                            f"⏱ {timeframe} | 🌐 {exchange.upper()}"
                        )
                        return
                
            except Exception as e:
                logger.error(f"Analysis error for {symbol}: {e}")
                return

    
    def should_send_alert(self, user_id, symbol):
        """Anti-spam: check if we can send alert for this symbol"""
        
        if user_id not in self.last_alerts:
            self.last_alerts[user_id] = {}
        
        # Check last alert time for this symbol
        last_time = self.last_alerts[user_id].get(symbol)
        
        if last_time:
            # Don't send same alert for same symbol within 1 hour
            if datetime.now() - last_time < timedelta(hours=1):
                return False
        
        return True
    
    async def send_alert(self, user_id, alert_type, symbol, message):
        """Send alert notification to user"""
        
        try:
            # Save to history
            db.add_alert_history(user_id, alert_type, symbol, message)
            
            # Update anti-spam tracker
            if user_id not in self.last_alerts:
                self.last_alerts[user_id] = {}
            self.last_alerts[user_id][symbol] = datetime.now()
            
            # Send Telegram message with button
            # Check if user wants notifications
            settings = db.get_alert_settings(user_id)
            notifications_on = settings.get("notifications_enabled", 1)
            
            if notifications_on:
                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                timeframe = settings.get("alert_timeframe", "1h")
                symbol_encoded = symbol.replace("/", "_").replace(":", "_")
                keyboard = [
                    [InlineKeyboardButton(f"📊 Analiza {symbol.split('/')[0]} ({timeframe})", callback_data=f"analyze_{symbol_encoded}_{timeframe}")],
                    [InlineKeyboardButton("📜 Historia", callback_data="alerts_history")]
                ]
                
                await self.app.bot.send_message(
                    chat_id=user_id,
                    text=f"🔔 ALERT\n\n{message}",
                    
                reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode=None

            )
            
            logger.info(f"✅ Sent {alert_type} alert to {user_id}: {symbol}")
            
        except Exception as e:
            logger.error(f"Error sending alert to {user_id}: {e}")


# Global instance (will be initialized in bot.py)
alert_scanner = None
