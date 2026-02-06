
scanner_code_part2 = """
    
    def get_frequency_minutes(self, freq):
        \"\"\"Convert frequency string to minutes\"\"\"
        freq_map = {
            '5m': 5,
            '15m': 15,
            '30m': 30,
            '1h': 60
        }
        return freq_map.get(freq, 15)
    
    async def check_symbol_alerts(self, user_id, symbol, exchange, settings):
        \"\"\"Check all alert types for one symbol\"\"\"
        
        # Anti-spam check
        if not self.should_send_alert(user_id, symbol):
            return
        
        timeframe = settings['scan_timeframe']
        
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
                f"🚀 DUŻY WZROST: {symbol.replace(':USDT', '')}\\n"
                f"💰 Cena: ${current_price}\\n"
                f"📈 Zmiana 24h: +{change_24h:.2f}%"
            )
            return
        
        if settings['big_losses_enabled'] and change_24h < -settings['loss_threshold']:
            await self.send_alert(
                user_id, 'big_loss', symbol,
                f"📉 DUŻY SPADEK: {symbol.replace(':USDT', '')}\\n"
                f"💰 Cena: ${current_price}\\n"
                f"📉 Zmiana 24h: {change_24h:.2f}%"
            )
            return
        
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
                analysis = await ai_trader.analyze_pair_full(symbol, exchange, timeframe)
                
                if not analysis:
                    return
                
                # Check RSI alerts
                rsi = analysis.get('rsi')
                if rsi:
                    if settings['oversold_enabled'] and rsi < 20:
                        await self.send_alert(
                            user_id, 'oversold', symbol,
                            f"🔥 OVERSOLD: {symbol.replace(':USDT', '')}\\n"
                            f"💰 Cena: ${current_price}\\n"
                            f"📊 RSI: {rsi:.1f} (OVERSOLD!)\\n"
                            f"⏱ {timeframe} | 🌐 {exchange.upper()}"
                        )
                        return
                    
                    if settings['overbought_enabled'] and rsi > 80:
                        await self.send_alert(
                            user_id, 'overbought', symbol,
                            f"💎 OVERBOUGHT: {symbol.replace(':USDT', '')}\\n"
                            f"💰 Cena: ${current_price}\\n"
                            f"📊 RSI: {rsi:.1f} (OVERBOUGHT!)\\n"
                            f"⏱ {timeframe} | 🌐 {exchange.upper()}"
                        )
                        return
                
                # Check Volume Spike
                if settings['volume_spike_enabled']:
                    volume_ratio = analysis.get('volume_ratio', 0)
                    if volume_ratio > settings['volume_multiplier']:
                        await self.send_alert(
                            user_id, 'volume_spike', symbol,
                            f"🔥 VOLUME SPIKE: {symbol.replace(':USDT', '')}\\n"
                            f"💰 Cena: ${current_price}\\n"
                            f"📊 Volume: {volume_ratio:.1f}x średniej\\n"
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
                            f"🤖 SYGNAŁ AI {signal}: {symbol.replace(':USDT', '')}\\n"
                            f"💰 Cena: ${current_price}\\n"
                            f"🎯 Confidence: {confidence}%\\n"
                            f"📊 RSI: {rsi:.1f}\\n"
                            f"⏱ {timeframe} | 🌐 {exchange.upper()}"
                        )
                        return
                
            except Exception as e:
                logger.error(f"Analysis error for {symbol}: {e}")
                return
"""

# Append to existing file
with open('alert_scanner.py', 'a') as f:
    f.write(scanner_code_part2)

print("✅ Added to alert_scanner.py - PART 2")

