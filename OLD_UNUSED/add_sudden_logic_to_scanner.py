with open('alert_scanner.py', 'r') as f:
    content = f.read()

print("=== ADDING SUDDEN CHANGE LOGIC TO SCANNER ===\n")

# Dodaj sprawdzanie nagłych zmian PO alertach 24h, PRZED wskaźnikami technicznymi
old_code = """        # For technical indicators, we need OHLCV data
        if any([
            settings['oversold_enabled'],"""

new_code = """        # Check sudden price changes (on custom timeframe)
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
                            f"{emoji} NAGŁA ZMIANA: {symbol.replace(':USDT', '')}\\n"
                            f"💰 Cena: ${current_price}\\n"
                            f"⚡ {direction}: {abs(sudden_change):.2f}% w {sudden_tf}\\n"
                            f"📊 {previous_close:.6f} → {current_close:.6f}"
                        )
                        # Continue checking other alerts (no return)
                        
            except Exception as e:
                logger.error(f"Sudden change check error for {symbol}: {e}")
        
        # For technical indicators, we need OHLCV data
        if any([
            settings['oversold_enabled'],"""

content = content.replace(old_code, new_code)
print("✅ Added sudden change logic to scanner")

with open('alert_scanner.py', 'w') as f:
    f.write(content)

