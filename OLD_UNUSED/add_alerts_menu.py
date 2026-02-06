with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING ALERTS MENU ===\n")

# 1. Dodaj przycisk "Alerty" do głównego menu
old_main = """        [InlineKeyboardButton(t('settings', lang), callback_data='settings')],"""

new_main = """        [InlineKeyboardButton(t('settings', lang), callback_data='settings')],
        [InlineKeyboardButton('🔔 Alerty', callback_data='alerts_menu')],"""

content = content.replace(old_main, new_main)
print("✅ Added Alerty button to main menu")

# 2. Dodaj handlery callbacków
old_handler = """    elif data == 'settings':
        await settings_menu(query, user_id, user)
        return"""

new_handler = """    elif data == 'settings':
        await settings_menu(query, user_id, user)
        return
    
    elif data == 'alerts_menu':
        await alerts_menu(query, user_id, user)
        return
    
    elif data == 'alerts_settings':
        await alerts_settings_menu(query, user_id, user)
        return
    
    elif data == 'alerts_history':
        await alerts_history_menu(query, user_id, user)
        return
    
    elif data.startswith('toggle_alert_'):
        alert_type = data.replace('toggle_alert_', '')
        await toggle_alert(query, user_id, user, alert_type)
        return
    
    elif data.startswith('set_scan_range_'):
        range_val = int(data.replace('set_scan_range_', ''))
        await set_scan_range(query, user_id, user, range_val)
        return
    
    elif data.startswith('set_scan_freq_'):
        freq = data.replace('set_scan_freq_', '')
        await set_scan_frequency(query, user_id, user, freq)
        return"""

content = content.replace(old_handler, new_handler)
print("✅ Added alert callbacks")

# 3. Dodaj funkcje menu
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
    
    def btn(name, enabled):
        emoji = '✅' if enabled else '❌'
        return InlineKeyboardButton(f'{emoji} {name}', callback_data=f'toggle_alert_{name.lower().replace(" ", "_")}')
    
    text = \"\"\"⚙️ USTAWIENIA ALERTÓW

Kliknij aby włączyć/wyłączyć:\"\"\"
    
    keyboard = [
        [btn('Oversold', settings['oversold_enabled'])],
        [btn('Overbought', settings['overbought_enabled'])],
        [btn('Duże Wzrosty', settings['big_gains_enabled'])],
        [btn('Duże Spadki', settings['big_losses_enabled'])],
        [btn('Sygnały AI', settings['ai_signals_enabled'])],
        [btn('Volume Spike', settings['volume_spike_enabled'])],
        [btn('MACD Cross', settings['macd_cross_enabled'])],
        [btn('EMA Cross', settings['ema_cross_enabled'])],
        [InlineKeyboardButton('━━━━━━━━━━', callback_data='none')],
        [InlineKeyboardButton('📊 Zakres skanowania', callback_data='set_scan_range')],
        [InlineKeyboardButton('⏰ Częstotliwość', callback_data='set_scan_frequency')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def toggle_alert(query, user_id, user, alert_type):
    \"\"\"Toggle alert on/off\"\"\"
    settings = db.get_alert_settings(user_id)
    
    # Map button name to db field
    field_map = {
        'oversold': 'oversold_enabled',
        'overbought': 'overbought_enabled',
        'duże_wzrosty': 'big_gains_enabled',
        'duże_spadki': 'big_losses_enabled',
        'sygnały_ai': 'ai_signals_enabled',
        'volume_spike': 'volume_spike_enabled',
        'macd_cross': 'macd_cross_enabled',
        'ema_cross': 'ema_cross_enabled'
    }
    
    field = field_map.get(alert_type)
    if field:
        new_value = 0 if settings[field] else 1
        db.update_alert_settings(user_id, {field: new_value})
        await query.answer(f"{'✅ Włączono' if new_value else '❌ Wyłączono'} alert")
    
    await alerts_settings_menu(query, user_id, user)


async def set_scan_range(query, user_id, user, range_val=None):
    \"\"\"Set scan range menu\"\"\"
    if range_val:
        db.update_alert_settings(user_id, {'scan_range': range_val})
        await query.answer(f'✅ Ustawiono zakres: TOP {range_val}')
        await alerts_settings_menu(query, user_id, user)
        return
    
    text = \"\"\"📊 ZAKRES SKANOWANIA

Ile par ma być skanowanych?

• TOP 10 - najszybsze
• TOP 50 - balans
• TOP 100 - dokładne
• TOP 200 - bardzo dokładne
• ALL - wszystkie pary (wolne)\"\"\"
    
    keyboard = [
        [InlineKeyboardButton('TOP 10', callback_data='set_scan_range_10'), InlineKeyboardButton('TOP 50', callback_data='set_scan_range_50')],
        [InlineKeyboardButton('TOP 100', callback_data='set_scan_range_100'), InlineKeyboardButton('TOP 200', callback_data='set_scan_range_200')],
        [InlineKeyboardButton('ALL (~700)', callback_data='set_scan_range_9999')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_settings')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def set_scan_frequency(query, user_id, user, freq=None):
    \"\"\"Set scan frequency\"\"\"
    if freq:
        db.update_alert_settings(user_id, {'scan_frequency': freq})
        await query.answer(f'✅ Częstotliwość: {freq}')
        await alerts_settings_menu(query, user_id, user)
        return
    
    text = \"\"\"⏰ CZĘSTOTLIWOŚĆ SKANOWANIA

Jak często bot ma sprawdzać rynek?

• 5m - bardzo często (więcej alertów)
• 15m - balans ⭐
• 30m - rzadziej
• 1h - oszczędne\"\"\"
    
    keyboard = [
        [InlineKeyboardButton('5 minut', callback_data='set_scan_freq_5m'), InlineKeyboardButton('15 minut', callback_data='set_scan_freq_15m')],
        [InlineKeyboardButton('30 minut', callback_data='set_scan_freq_30m'), InlineKeyboardButton('1 godzina', callback_data='set_scan_freq_1h')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_settings')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


async def alerts_history_menu(query, user_id, user):
    \"\"\"Show alert history\"\"\"
    history = db.get_alert_history(user_id, limit=50)
    
    if not history:
        text = \"\"\"📜 HISTORIA ALERTÓW

Brak alertów w historii.
Włącz alerty w ustawieniach!\"\"\"
        keyboard = [[InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return
    
    text = f\"\"\"📜 HISTORIA ALERTÓW

Ostatnie {len(history)} alertów:\\n\\n\"\"\"
    
    for alert in history[:10]:  # Show last 10
        time = alert['triggered_at'][:16].replace('T', ' ')
        text += f\"\"\"🔔 {alert['alert_type'].upper()}
{alert['symbol']} - {time}
{alert['message'][:60]}...\\n\\n\"\"\"
    
    keyboard = [[InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_menu')]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

"""

# Wstaw przed # ==========================================
insert_before = "# ==========================================" 
# Znajdź ostatnie wystąpienie (przed końcem pliku)
parts = content.rsplit(insert_before, 1)
if len(parts) == 2:
    content = parts[0] + new_functions + '\n' + insert_before + parts[1]
    print("✅ Added alerts menu functions")

with open('handlers.py', 'w') as f:
    f.write(content)

