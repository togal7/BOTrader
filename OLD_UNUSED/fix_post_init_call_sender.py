with open('bot.py', 'r') as f:
    content = f.read()

print("Fixing post_init to actually start alert_sender_loop...")

# Usuń błędny post_init (linie 103-106)
old_broken_init = '''    async def post_init(app):
        logger.info("🔔 Alert Scanner STARTED")
    
    application.post_init = post_init'''

new_working_init = '''    async def post_init(app):
        """Start background tasks after bot initialization"""
        logger.info("🔔 Starting Alert Sender Loop...")
        import asyncio
        asyncio.create_task(alert_sender_loop(app))
    
    application.post_init = post_init'''

content = content.replace(old_broken_init, new_working_init)

with open('bot.py', 'w') as f:
    f.write(content)

print("✅ post_init fixed to call alert_sender_loop!")

