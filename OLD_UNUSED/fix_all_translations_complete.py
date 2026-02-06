with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING ALL TRANSLATION ISSUES ===\n")

# 1. Fix podwójne emoji ⚙️ ⚙️ (linia 652)
old_settings_header = """    text = f\"\"\"⚙️ {t('settings', lang).upper()}"""
new_settings_header = """    text = f\"\"\"{t('settings', lang).upper()}"""

content = content.replace(old_settings_header, new_settings_header)
print("✅ Fixed double emoji in settings")

# 2. Fix TIMEFRAMES - musi używać lang!
# Najpierw znajdź definicję TIMEFRAMES
old_timeframes_def = """TIMEFRAMES = {
    '1m': {'label': '1 minuta', 'seconds': 60},
    '3m': {'label': '3 minuty', 'seconds': 180},
    '5m': {'label': '5 minut', 'seconds': 300},
    '15m': {'label': '15 minut', 'seconds': 900},
    '30m': {'label': '30 minut', 'seconds': 1800},
    '1h': {'label': '1 godzina', 'seconds': 3600},
    '2h': {'label': '2 godziny', 'seconds': 7200},
    '4h': {'label': '4 godziny', 'seconds': 14400},
    '8h': {'label': '8 godzin', 'seconds': 28800},
    '12h': {'label': '12 godzin', 'seconds': 43200},
    '1d': {'label': '1 dzień', 'seconds': 86400},
    '3d': {'label': '3 dni', 'seconds': 259200},
    '1w': {'label': '1 tydzień', 'seconds': 604800},
    '1M': {'label': '1 miesiąc', 'seconds': 2592000}
}"""

new_timeframes_def = """# TIMEFRAMES - multilingual
def get_timeframe_label(tf, lang='pl'):
    \"\"\"Get timeframe label in user's language\"\"\"
    labels = {
        '1m': {'pl': '1 minuta', 'en': '1 minute', 'es': '1 minuto', 'de': '1 Minute', 'fr': '1 minute', 'it': '1 minuto', 'pt': '1 minuto', 'ru': '1 минута', 'tr': '1 dakika', 'zh': '1分钟'},
        '3m': {'pl': '3 minuty', 'en': '3 minutes', 'es': '3 minutos', 'de': '3 Minuten', 'fr': '3 minutes', 'it': '3 minuti', 'pt': '3 minutos', 'ru': '3 минуты', 'tr': '3 dakika', 'zh': '3分钟'},
        '5m': {'pl': '5 minut', 'en': '5 minutes', 'es': '5 minutos', 'de': '5 Minuten', 'fr': '5 minutes', 'it': '5 minuti', 'pt': '5 minutos', 'ru': '5 минут', 'tr': '5 dakika', 'zh': '5分钟'},
        '15m': {'pl': '15 minut', 'en': '15 minutes', 'es': '15 minutos', 'de': '15 Minuten', 'fr': '15 minutes', 'it': '15 minuti', 'pt': '15 minutos', 'ru': '15 минут', 'tr': '15 dakika', 'zh': '15分钟'},
        '30m': {'pl': '30 minut', 'en': '30 minutes', 'es': '30 minutos', 'de': '30 Minuten', 'fr': '30 minutes', 'it': '30 minuti', 'pt': '30 minutos', 'ru': '30 минут', 'tr': '30 dakika', 'zh': '30分钟'},
        '1h': {'pl': '1 godzina', 'en': '1 hour', 'es': '1 hora', 'de': '1 Stunde', 'fr': '1 heure', 'it': '1 ora', 'pt': '1 hora', 'ru': '1 час', 'tr': '1 saat', 'zh': '1小时'},
        '2h': {'pl': '2 godziny', 'en': '2 hours', 'es': '2 horas', 'de': '2 Stunden', 'fr': '2 heures', 'it': '2 ore', 'pt': '2 horas', 'ru': '2 часа', 'tr': '2 saat', 'zh': '2小时'},
        '4h': {'pl': '4 godziny', 'en': '4 hours', 'es': '4 horas', 'de': '4 Stunden', 'fr': '4 heures', 'it': '4 ore', 'pt': '4 horas', 'ru': '4 часа', 'tr': '4 saat', 'zh': '4小时'},
        '8h': {'pl': '8 godzin', 'en': '8 hours', 'es': '8 horas', 'de': '8 Stunden', 'fr': '8 heures', 'it': '8 ore', 'pt': '8 horas', 'ru': '8 часов', 'tr': '8 saat', 'zh': '8小时'},
        '12h': {'pl': '12 godzin', 'en': '12 hours', 'es': '12 horas', 'de': '12 Stunden', 'fr': '12 heures', 'it': '12 ore', 'pt': '12 horas', 'ru': '12 часов', 'tr': '12 saat', 'zh': '12小时'},
        '1d': {'pl': '1 dzień', 'en': '1 day', 'es': '1 día', 'de': '1 Tag', 'fr': '1 jour', 'it': '1 giorno', 'pt': '1 dia', 'ru': '1 день', 'tr': '1 gün', 'zh': '1天'},
        '3d': {'pl': '3 dni', 'en': '3 days', 'es': '3 días', 'de': '3 Tage', 'fr': '3 jours', 'it': '3 giorni', 'pt': '3 dias', 'ru': '3 дня', 'tr': '3 gün', 'zh': '3天'},
        '1w': {'pl': '1 tydzień', 'en': '1 week', 'es': '1 semana', 'de': '1 Woche', 'fr': '1 semaine', 'it': '1 settimana', 'pt': '1 semana', 'ru': '1 неделя', 'tr': '1 hafta', 'zh': '1周'},
        '1M': {'pl': '1 miesiąc', 'en': '1 month', 'es': '1 mes', 'de': '1 Monat', 'fr': '1 mois', 'it': '1 mese', 'pt': '1 mês', 'ru': '1 месяц', 'tr': '1 ay', 'zh': '1月'}
    }
    return labels.get(tf, {}).get(lang, labels.get(tf, {}).get('pl', tf))

TIMEFRAMES = {
    '1m': {'seconds': 60},
    '3m': {'seconds': 180},
    '5m': {'seconds': 300},
    '15m': {'seconds': 900},
    '30m': {'seconds': 1800},
    '1h': {'seconds': 3600},
    '2h': {'seconds': 7200},
    '4h': {'seconds': 14400},
    '8h': {'seconds': 28800},
    '12h': {'seconds': 43200},
    '1d': {'seconds': 86400},
    '3d': {'seconds': 259200},
    '1w': {'seconds': 604800},
    '1M': {'seconds': 2592000}
}"""

if old_timeframes_def in content:
    content = content.replace(old_timeframes_def, new_timeframes_def)
    print("✅ Added multilingual timeframes function")

# 3. Fix settings_menu to use new function
old_settings_interval = """🌐 {t('exchange', lang)}: {EXCHANGES[exchange]['name']}
⏰ {t('interval', lang)}: {TIMEFRAMES[interval]['label']}"""

new_settings_interval = """🌐 {t('exchange', lang)}: {EXCHANGES[exchange]['name']}
⏰ {t('interval', lang)}: {get_timeframe_label(interval, lang)}"""

content = content.replace(old_settings_interval, new_settings_interval)
print("✅ Fixed interval label in settings")

# 4. Fix change_exchange_menu - hardcoded Polish
old_change_exchange = """    text = "🌐 WYBIERZ GIEŁDĘ\\n\\nDostępne giełdy:\""""

new_change_exchange = """    lang = get_user_language(user)
    text = f"🌐 {t('select_exchange', lang)}\\n\\n{t('available_exchanges', lang)}:\""""

content = content.replace(old_change_exchange, new_change_exchange)
print("✅ Fixed change_exchange_menu")

# 5. Fix "Powrót" button
content = content.replace("[InlineKeyboardButton('⬅️ Powrót', callback_data='settings')]", 
                         "[InlineKeyboardButton(t('back', lang), callback_data='settings')]")
print("✅ Fixed back button in change_exchange")

with open('handlers.py', 'w') as f:
    f.write(content)

