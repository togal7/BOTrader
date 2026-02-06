with open('bot.py', 'r') as f:
    content = f.read()

print("Using proper Application.post_init callback...")

# Usuń job_queue attempt
content = content.replace(
    '''    # Use job_queue for alert sender (runs after bot starts)
    def start_sender(context):
        logger.info("🔔 Starting Alert Sender via JobQueue...")
        import asyncio
        asyncio.create_task(alert_sender_loop(context.application))
    
    application.job_queue.run_once(start_sender, when=2)''',
    '''    # Post init callback - starts alert sender after bot initialization
    async def on_startup(application):
        logger.info("🔔 Starting Alert Sender Loop...")
        import asyncio
        asyncio.create_task(alert_sender_loop(application))
    
    # Register post_init callback
    application.post_init = on_startup'''
)

with open('bot.py', 'w') as f:
    f.write(content)

print("✅ Fixed with proper post_init callback")

