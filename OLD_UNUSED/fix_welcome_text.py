with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING WELCOME TEXT ===\n")

# Znajdź start_command
old_welcome = """    text = f\"\"\"👋 {t('welcome', lang)}

{t('your_status', lang)}: {sub_status}
🆔 ID: {user_id}

✨ {t('possibilities', lang)}:
🔍 {t('search_desc', lang)}
📊 {t('scan_desc', lang)}
🎯 {t('ai_desc', lang)}
⚙️ {t('settings_desc', lang)}\"\"\""""

new_welcome = """    text = f\"\"\"👋 Witaj w BOTrader!

Status: {sub_status}
🆔 ID: {user_id}

✨ Co możesz zrobić:
🔍 Analiza AI - szczegółowa analiza wybranej pary
📊 Skaner Ekstremów - znajdź wzrosty, spadki, RSI
🎯 Sygnały AI - automatyczne sygnały trading
🔔 Alerty - powiadomienia o okazjach rynkowych
⚙️ Ustawienia - giełda, interwał, język\"\"\""""

if old_welcome in content:
    content = content.replace(old_welcome, new_welcome)
    print("✅ Fixed welcome text")
else:
    # Alternatywnie - znajdź i zamień inaczej
    print("⚠️ Pattern not found, trying alternative...")

with open('handlers.py', 'w') as f:
    f.write(content)

