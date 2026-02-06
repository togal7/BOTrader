with open('alert_scanner.py', 'r') as f:
    content = f.read()

print("=== FIXING ALERT ORDER ===\n")

# Opcja 1: Usuń return po big_gains i big_losses
# Wtedy będzie sprawdzać WSZYSTKIE alerty

old_gains = """        if settings['big_gains_enabled'] and change_24h > settings['gain_threshold']:
            await self.send_alert(
                user_id, 'big_gain', symbol,
                f"🚀 DUŻY WZROST: {symbol.replace(':USDT', '')}\\n"
                f"💰 Cena: ${current_price}\\n"
                f"📈 Zmiana 24h: +{change_24h:.2f}%"
            )
            return"""

new_gains = """        if settings['big_gains_enabled'] and change_24h > settings['gain_threshold']:
            await self.send_alert(
                user_id, 'big_gain', symbol,
                f"🚀 DUŻY WZROST: {symbol.replace(':USDT', '')}\\n"
                f"💰 Cena: ${current_price}\\n"
                f"📈 Zmiana 24h: +{change_24h:.2f}%"
            )
            # Removed return - continue checking other alerts"""

content = content.replace(old_gains, new_gains)
print("✅ Removed return after big_gains")

old_losses = """        if settings['big_losses_enabled'] and change_24h < -settings['loss_threshold']:
            await self.send_alert(
                user_id, 'big_loss', symbol,
                f"📉 DUŻY SPADEK: {symbol.replace(':USDT', '')}\\n"
                f"💰 Cena: ${current_price}\\n"
                f"📉 Zmiana 24h: {change_24h:.2f}%"
            )
            return"""

new_losses = """        if settings['big_losses_enabled'] and change_24h < -settings['loss_threshold']:
            await self.send_alert(
                user_id, 'big_loss', symbol,
                f"📉 DUŻY SPADEK: {symbol.replace(':USDT', '')}\\n"
                f"💰 Cena: ${current_price}\\n"
                f"📉 Zmiana 24h: {change_24h:.2f}%"
            )
            # Removed return - continue checking other alerts"""

content = content.replace(old_losses, new_losses)
print("✅ Removed return after big_losses")

with open('alert_scanner.py', 'w') as f:
    f.write(content)

print("\n✅ Teraz będzie sprawdzać WSZYSTKIE alerty!")

