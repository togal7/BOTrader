with open('bot.py', 'r') as f:
    lines = f.readlines()

print("Searching for application.run_polling...")

new_lines = []
added = False

for i, line in enumerate(lines):
    # Dodaj PRZED application.run_polling
    if 'application.run_polling' in line and not added:
        print(f"Found at line {i+1}: {line.strip()}")
        
        # Sprawdź wcięcie
        indent = len(line) - len(line.lstrip())
        spaces = ' ' * indent
        
        # Dodaj alert sender startup
        new_lines.append(f'{spaces}# Start alert sender background task\n')
        new_lines.append(f'{spaces}from alert_queue import alert_queue\n')
        new_lines.append(f'{spaces}\n')
        new_lines.append(f'{spaces}async def start_background_tasks(app):\n')
        new_lines.append(f'{spaces}    """Start background tasks after bot initialization"""\n')
        new_lines.append(f'{spaces}    import asyncio\n')
        new_lines.append(f'{spaces}    logger.info("🔔 Starting Alert Sender Loop...")\n')
        new_lines.append(f'{spaces}    asyncio.create_task(alert_sender_loop(app))\n')
        new_lines.append(f'{spaces}\n')
        new_lines.append(f'{spaces}application.post_init = start_background_tasks\n')
        new_lines.append(f'{spaces}\n')
        added = True
    
    new_lines.append(line)

with open('bot.py', 'w') as f:
    f.writelines(new_lines)

if added:
    print("✅ Alert sender startup added!")
else:
    print("❌ Could not find application.run_polling")

