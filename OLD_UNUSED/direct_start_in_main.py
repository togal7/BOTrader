with open('bot.py', 'r') as f:
    content = f.read()

print("Direct approach - start alert sender in main() via async helper...")

# Usuń post_init attempt
lines = content.split('\n')
new_lines = []

skip_until_blank = False

for i, line in enumerate(lines):
    # Skip old post_init section
    if '# Post init callback' in line or 'async def on_startup' in line:
        skip_until_blank = True
        continue
    
    if skip_until_blank:
        if line.strip() == '':
            skip_until_blank = False
        continue
    
    # Find application.run_polling and add startup INSIDE run_polling
    if 'application.run_polling' in line:
        indent = '    '
        
        # Add before run_polling
        new_lines.append(f'{indent}# Start alert sender in background\n')
        new_lines.append(f'{indent}async def _start_sender():\n')
        new_lines.append(f'{indent}    await asyncio.sleep(2)  # Wait for bot to be ready\n')
        new_lines.append(f'{indent}    logger.info("🔔 Starting Alert Sender Loop...")\n')
        new_lines.append(f'{indent}    asyncio.create_task(alert_sender_loop(application))\n')
        new_lines.append(f'{indent}\n')
        new_lines.append(f'{indent}asyncio.create_task(_start_sender())\n')
        new_lines.append(f'{indent}\n')
    
    new_lines.append(line + '\n')

content = ''.join(new_lines)

with open('bot.py', 'w') as f:
    f.write(content)

print("✅ Direct startup added!")

