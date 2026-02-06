with open('ai_trader.py', 'r') as f:
    content = f.read()

print("=== FIXING 'price' -> 'last' ===\n")

# Zamień data.get('price') na data.get('last')
old = "data.get('price')"
new = "data.get('last')"

if old in content:
    content = content.replace(old, new)
    print(f"✅ Replaced {old} -> {new}")
else:
    print("⚠️ Not found")

with open('ai_trader.py', 'w') as f:
    f.write(content)

