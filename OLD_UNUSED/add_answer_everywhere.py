with open('handlers.py', 'r') as f:
    content = f.read()

print("\n=== ADDING IMMEDIATE ANSWER TO ALL CALLBACKS ===\n")

# Lista callbacków do naprawy
fixes = [
    ("elif data.startswith('toggle_alert_'):", 
     "elif data.startswith('toggle_alert_'):\n        await query.answer()"),
    
    ("elif data.startswith('analyze_'):",
     "elif data.startswith('analyze_'):\n        await query.answer()"),
]

for old, new in fixes:
    if old in content and 'await query.answer()' not in content[content.find(old):content.find(old)+200]:
        content = content.replace(old, new)
        print(f"✅ Added answer to {old[:30]}")

with open('handlers.py', 'w') as f:
    f.write(content)

