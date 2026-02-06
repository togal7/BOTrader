with open('bot.py', 'r') as f:
    lines = f.readlines()

print("Removing broken asyncio.create_task calls...")

new_lines = []
skip_next = False

for i, line in enumerate(lines):
    line_num = i + 1
    
    # Skip linia 72
    if 'asyncio.create_task(alert_sender_loop(application))' in line:
        print(f"Line {line_num}: REMOVED - {line.strip()}")
        continue
    
    # Skip linia 104 (długa z logger.info)
    if 'logger.info("🔔 Starting Alert Sender Loop...")' in line and 'asyncio.create_task' in line:
        print(f"Line {line_num}: REMOVED - {line.strip()[:80]}...")
        continue
    
    # Skip całą sekcję async def post_init jeśli istnieje
    if 'async def post_init(app):' in line or 'async def on_startup' in line:
        skip_next = True
        print(f"Line {line_num}: Skipping post_init section")
        continue
    
    if skip_next:
        if line.strip() == '' or 'application.post_init' in line:
            skip_next = False
        continue
    
    # Skip application.post_init = ...
    if 'application.post_init' in line:
        print(f"Line {line_num}: REMOVED - {line.strip()}")
        continue
    
    # Skip async def _start_sender
    if 'async def _start_sender' in line:
        skip_next = True
        print(f"Line {line_num}: Skipping _start_sender section")
        continue
    
    new_lines.append(line)

with open('bot.py', 'w') as f:
    f.writelines(new_lines)

print("\n✅ Removed all broken alert sender calls!")
print("Bot will now use separate AlertSender process.")

