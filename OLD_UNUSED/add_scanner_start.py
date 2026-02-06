with open('bot.py', 'r') as f:
    content = f.read()

print("=== ADDING SCANNER START ===\n")

# Dokładny pattern z bot.py
old = """    # Start polling
    logger.info("✅  Bot uruchomiony!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)"""

new = """    # Start polling
    logger.info("✅  Bot uruchomiony!")
    
    # Start alert scanner in background
    async def post_init(app):
        await scanner.start()
        logger.info("🔔 Alert Scanner STARTED")
    
    application.post_init = post_init
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)"""

if old in content:
    content = content.replace(old, new)
    print("✅ Added scanner.start()")
else:
    print("❌ Pattern STILL not found - showing what we have:")
    print(content[-200:])

with open('bot.py', 'w') as f:
    f.write(content)

