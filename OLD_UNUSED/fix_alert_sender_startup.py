with open('bot.py', 'r') as f:
    content = f.read()

print("Fixing alert_sender startup...")

# Usuń błędne create_task przed run_polling
content = content.replace(
    '    asyncio.create_task(alert_sender_loop(application))',
    '    # Alert sender will be started via post_init hook'
)

# Dodaj proper startup via application.post_init
startup_code = '''
async def post_init(application):
    """Called after bot starts - safe place for background tasks"""
    logger.info("🔔 Starting alert sender loop...")
    asyncio.create_task(alert_sender_loop(application))

'''

# Wstaw przed def main()
main_pos = content.find('def main():')
if main_pos != -1:
    content = content[:main_pos] + startup_code + content[main_pos:]

# Dodaj post_init do application
# Znajdź application.run_polling
old_run = 'application.run_polling(allowed_updates=Update.ALL_TYPES)'
new_run = '''# Start alert sender via post_init
    application.post_init = post_init
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)'''

content = content.replace(old_run, new_run)

with open('bot.py', 'w') as f:
    f.write(content)

print("✅ Fixed!")

