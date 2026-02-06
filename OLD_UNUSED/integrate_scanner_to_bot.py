with open('bot.py', 'r') as f:
    content = f.read()

print("=== INTEGRATING ALERT SCANNER TO BOT ===\n")

# 1. Dodaj import
old_imports = "from handlers import *"
new_imports = """from handlers import *
from alert_scanner import AlertScanner"""

content = content.replace(old_imports, new_imports)
print("✅ Added import")

# 2. Dodaj inicjalizację w main()
old_main = """    # Aplikacja
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()"""

new_main = """    # Aplikacja
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Initialize Alert Scanner
    scanner = AlertScanner(application)"""

content = content.replace(old_main, new_main)
print("✅ Added scanner initialization")

# 3. Dodaj uruchomienie po start polling
old_polling = """    # Start polling
    logger.info("✅  Bot uruchomiony!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)"""

new_polling = """    # Start polling
    logger.info("✅  Bot uruchomiony!")
    
    # Start alert scanner in background
    async def post_init(app):
        await scanner.start()
    
    application.post_init = post_init
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)"""

content = content.replace(old_polling, new_polling)
print("✅ Added scanner startup")

with open('bot.py', 'w') as f:
    f.write(content)

print("\n✅ Integration complete!")

