with open('bot.py', 'r') as f:
    lines = f.readlines()

print("=== FORCE ADDING SCANNER START ===\n")

# Znajdź linię z application.run_polling
for i, line in enumerate(lines):
    if 'application.run_polling' in line:
        print(f"Found run_polling at line {i+1}")
        
        # Wstaw PRZED tą linią
        indent = '    '
        new_lines = [
            '\n',
            indent + '# Start alert scanner in background\n',
            indent + 'async def post_init(app):\n',
            indent + '    await scanner.start()\n',
            indent + '    logger.info("🔔 Alert Scanner STARTED")\n',
            '\n',
            indent + 'application.post_init = post_init\n',
            '\n'
        ]
        
        # Wstaw
        lines[i:i] = new_lines
        print(f"✅ Inserted scanner start before line {i+1}")
        break

with open('bot.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Done!")

