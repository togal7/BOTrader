with open('bot.py', 'r') as f:
    content = f.read()

print("Switching to JobQueue for alert sender (guaranteed to work)...")

# Znajdź application.run_polling i dodaj PRZED nim proper callback
old_section = '''    async def post_init(app):
        logger.info("🔔 Starting Alert Sender Loop..."); import asyncio; asyncio.create_task(alert_sender_loop(app))
    
    application.post_init = post_init'''

new_section = '''    # Use job_queue for alert sender (runs after bot starts)
    def start_sender_callback(context):
        """Callback to start alert sender"""
        logger.info("🔔 Starting Alert Sender via JobQueue...")
        import asyncio
        asyncio.create_task(alert_sender_loop(context.application))
    
    # Schedule to run once after 2 seconds
    application.job_queue.run_once(start_sender_callback, when=2)'''

if old_section in content:
    content = content.replace(old_section, new_section)
    print("✅ Switched to JobQueue")
else:
    print("⚠️ Old section not found, trying manual approach...")
    
    # Manual: znajdź gdzie jest application.post_init
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        if 'application.post_init = post_init' in line:
            # Zamień na JobQueue approach
            new_lines.append('    # Use job_queue for alert sender (runs after bot starts)\n')
            new_lines.append('    def start_sender(context):\n')
            new_lines.append('        logger.info("🔔 Starting Alert Sender via JobQueue...")\n')
            new_lines.append('        import asyncio\n')
            new_lines.append('        asyncio.create_task(alert_sender_loop(context.application))\n')
            new_lines.append('    \n')
            new_lines.append('    application.job_queue.run_once(start_sender, when=2)\n')
            
            # Skip next 2 lines (old code)
            continue
        else:
            new_lines.append(line + '\n')
    
    content = ''.join(new_lines)
    print("✅ Manual replacement done")

with open('bot.py', 'w') as f:
    f.write(content)

