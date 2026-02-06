with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING ALERTS MENU - PART 2 ===\n")

# Dodaj funkcje menu alertów
new_functions = """

# ==========================================
# ALERTS SYSTEM
# ==========================================

async def alerts_menu(query, user_id, user):
    \"\"\"Main alerts menu\"\"\"
    settings = db.get_alert_settings(user_id)
    
    # Status emoji
    def status(enabled):
        return '✅' if enabled else '❌'
    
    text = f\"\"\"🔔 SYSTEM ALERTÓW

📊 Status alertów:
{status(settings['oversold_enabled'])} Oversold (RSI < 20)
{status(settings['overbought_enabled'])} Overbought (RSI > 80)
{status(settings['big_gains_enabled'])} Duże Wzrosty (+{settings['gain_threshold']}%)
{status(settings['big_losses_enabled'])} Duże Spadki (-{settings['loss_threshold']}%)
{status(settings['ai_signals_enabled'])} Sygnały AI (>{settings['min_confidence']}%)
{status(settings['volume_spike_enabled'])} Volume Spike (>{settings['volume_multiplier']}x)
{status(settings['macd_cross_enabled'])} MACD Cross
{status(settings['ema_cross_enabled'])} EMA Cross

⚙️ Ustawienia skanera:
📊 Zakres: TOP {settings['scan_range']}
⏰ Częstotliwość: {settings['scan_frequency']}
📈 Timeframe: {settings['scan_timeframe']}

Bot automatycznie skanuje rynek i wysyła powiadomienia o okazjach!\"\"\"
    
    keyboard = [
        [InlineKeyboardButton('⚙️ Ustawienia Alertów', callback_data='alerts_settings')],
        [InlineKeyboardButton('📜 Historia (ostatnie 50)', callback_data='alerts_history')],
        [InlineKeyboardButton('⬅️ Menu główne', callback_data='back_main')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def alerts_settings_menu(query, user_id, user):
    \"\"\"Alert settings menu\"\"\"
    settings = db.get_alert_settings(user_id)
    
    def btn(name, field):
        emoji = '✅' if settings[field] else '❌'
        return InlineKeyboardButton(f'{emoji} {name}', callback_data=f'toggle_alert_{field}')
    
    text = \"\"\"⚙️ USTAWIENIA ALERTÓW

Kliknij aby włączyć/wyłączyć:\"\"\"
    
    keyboard = [
        [btn('Oversold', 'oversold_enabled')],
        [btn('Overbought', 'overbought_enabled')],
        [btn('Duże Wzrosty', 'big_gains_enabled')],
        [btn('Duże Spadki', 'big_losses_enabled')],
        [btn('Sygnały AI', 'ai_signals_enabled')],
        [btn('Volume Spike', 'volume_spike_enabled')],
        [btn('MACD Cross', 'macd_cross_enabled')],
        [btn('EMA Cross', 'ema_cross_enabled')],
        [InlineKeyboardButton('━━━━━━━━━━', callback_data='none')],
        [InlineKeyboardButton('📊 Zakres skanowania', callback_data='set_scan_range')],
        [InlineKeyboardButton('⏰ Częstotliwość', callback_data='set_scan_frequency')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

"""

# Wstaw przed ostatnim separatorem
insert_point = content.rfind("# ==========================================")
if insert_point > 0:
    content = content[:insert_point] + new_functions + content[insert_point:]
    print("✅ Added alerts_menu and alerts_settings_menu")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ PART 2A DONE")

