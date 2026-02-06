with open('handlers.py', 'r') as f:
    content = f.read()

print("=== STEP 2: Multilingual TIMEFRAMES ===\n")

# Znajdź obecne TIMEFRAMES
old_tf = """TIMEFRAMES = {
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

# Nowe z dict dla języków
new_tf = """TIMEFRAMES = {
    '1m': {
        'seconds': 60,
        'label': {'pl': '1 minuta', 'en': '1 minute', 'es': '1 minuto', 'de': '1 Minute', 'fr': '1 minute', 'it': '1 minuto', 'pt': '1 minuto', 'ru': '1 минута', 'tr': '1 dakika', 'zh': '1分钟'}
    },
    '3m': {
        'seconds': 180,
        'label': {'pl': '3 minuty', 'en': '3 minutes', 'es': '3 minutos', 'de': '3 Minuten', 'fr': '3 minutes', 'it': '3 minuti', 'pt': '3 minutos', 'ru': '3 минуты', 'tr': '3 dakika', 'zh': '3分钟'}
    },
    '5m': {
        'seconds': 300,
        'label': {'pl': '5 minut', 'en': '5 minutes', 'es': '5 minutos', 'de': '5 Minuten', 'fr': '5 minutes', 'it': '5 minuti', 'pt': '5 minutos', 'ru': '5 минут', 'tr': '5 dakika', 'zh': '5分钟'}
    },
    '15m': {
        'seconds': 900,
        'label': {'pl': '15 minut', 'en': '15 minutes', 'es': '15 minutos', 'de': '15 Minuten', 'fr': '15 minutes', 'it': '15 minuti', 'pt': '15 minutos', 'ru': '15 минут', 'tr': '15 dakika', 'zh': '15分钟'}
    },
    '30m': {
        'seconds': 1800,
        'label': {'pl': '30 minut', 'en': '30 minutes', 'es': '30 minutos', 'de': '30 Minuten', 'fr': '30 minutes', 'it': '30 minuti', 'pt': '30 minutos', 'ru': '30 минут', 'tr': '30 dakika', 'zh': '30分钟'}
    },
    '1h': {
        'seconds': 3600,
        'label': {'pl': '1 godzina', 'en': '1 hour', 'es': '1 hora', 'de': '1 Stunde', 'fr': '1 heure', 'it': '1 ora', 'pt': '1 hora', 'ru': '1 час', 'tr': '1 saat', 'zh': '1小时'}
    },
    '2h': {
        'seconds': 7200,
        'label': {'pl': '2 godziny', 'en': '2 hours', 'es': '2 horas', 'de': '2 Stunden', 'fr': '2 heures', 'it': '2 ore', 'pt': '2 horas', 'ru': '2 часа', 'tr': '2 saat', 'zh': '2小时'}
    },
    '4h': {
        'seconds': 14400,
        'label': {'pl': '4 godziny', 'en': '4 hours', 'es': '4 horas', 'de': '4 Stunden', 'fr': '4 heures', 'it': '4 ore', 'pt': '4 horas', 'ru': '4 часа', 'tr': '4 saat', 'zh': '4小时'}
    },
    '8h': {
        'seconds': 28800,
        'label': {'pl': '8 godzin', 'en': '8 hours', 'es': '8 horas', 'de': '8 Stunden', 'fr': '8 heures', 'it': '8 ore', 'pt': '8 horas', 'ru': '8 часов', 'tr': '8 saat', 'zh': '8小时'}
    },
    '12h': {
        'seconds': 43200,
        'label': {'pl': '12 godzin', 'en': '12 hours', 'es': '12 horas', 'de': '12 Stunden', 'fr': '12 heures', 'it': '12 ore', 'pt': '12 horas', 'ru': '12 часов', 'tr': '12 saat', 'zh': '12小时'}
    },
    '1d': {
        'seconds': 86400,
        'label': {'pl': '1 dzień', 'en': '1 day', 'es': '1 día', 'de': '1 Tag', 'fr': '1 jour', 'it': '1 giorno', 'pt': '1 dia', 'ru': '1 день', 'tr': '1 gün', 'zh': '1天'}
    },
    '3d': {
        'seconds': 259200,
        'label': {'pl': '3 dni', 'en': '3 days', 'es': '3 días', 'de': '3 Tage', 'fr': '3 jours', 'it': '3 giorni', 'pt': '3 dias', 'ru': '3 дня', 'tr': '3 gün', 'zh': '3天'}
    },
    '1w': {
        'seconds': 604800,
        'label': {'pl': '1 tydzień', 'en': '1 week', 'es': '1 semana', 'de': '1 Woche', 'fr': '1 semaine', 'it': '1 settimana', 'pt': '1 semana', 'ru': '1 неделя', 'tr': '1 hafta', 'zh': '1周'}
    },
    '1M': {
        'seconds': 2592000,
        'label': {'pl': '1 miesiąc', 'en': '1 month', 'es': '1 mes', 'de': '1 Monat', 'fr': '1 mois', 'it': '1 mese', 'pt': '1 mês', 'ru': '1 месяц', 'tr': '1 ay', 'zh': '1月'}
    }
}"""

if old_tf in content:
    content = content.replace(old_tf, new_tf)
    print("✅ TIMEFRAMES updated with multilingual dict")
    
    # Teraz zmień użycie w settings_menu
    old_settings = "⏰ {t('interval', lang)}: {TIMEFRAMES[interval]['label']}\"\"\""
    new_settings = "⏰ {t('interval', lang)}: {TIMEFRAMES.get(interval, {}).get('label', {}).get(lang, interval)}\"\"\""
    
    content = content.replace(old_settings, new_settings)
    print("✅ settings_menu updated to use lang")
else:
    print("⚠️ Old TIMEFRAMES not found")

with open('handlers.py', 'w') as f:
    f.write(content)

