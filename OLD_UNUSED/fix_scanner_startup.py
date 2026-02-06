with open('bot.py', 'r') as f:
    content = f.read()

print("=== FIXING SCANNER STARTUP ===\n")

# Sprawdź czy jest post_init
if 'scanner.start()' not in content:
    print("⚠️ scanner.start() NOT FOUND - adding...")
    
    # Znajdź application.run_polling
    old = """    # Start polling
    logger.info("✅  Bot uruchomiony!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)"""
    
    new = """    # Start polling
    logger.info("✅  Bot uruchomiony!")
    
    # Start alert scanner
    async def post_init(app):
        await scanner.start()
        logger.info("🔔 Alert Scanner STARTED in background")
    
    application.post_init = post_init
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)"""
    
    if old in content:
        content = content.replace(old, new)
        print("✅ Added scanner.start() in post_init")
    else:
        print("❌ Pattern not found")
else:
    print("✅ scanner.start() already exists")

with open('bot.py', 'w') as f:
    f.write(content)

