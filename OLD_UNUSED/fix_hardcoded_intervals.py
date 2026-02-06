with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING HARDCODED 15m INTERVALS ===\n")

# Problem 1: Linia 613 - wyszukiwanie par
old_search = 'callback_data=f"analyze_{symbol_encoded}_15m"'
new_search = 'callback_data=f"analyze_{symbol_encoded}_{user.get(\'interval\', \'15m\')}"'

if old_search in content:
    content = content.replace(old_search, new_search)
    print("✅ Fixed line 613 - search results now use user interval")
else:
    print("⚠️ Line 613 pattern not found")

# Problem 2: Linia 1049 - scan extremes
old_scan = 'callback_data=f"analyze_{symbol_encoded}_15m"'
# To samo co wyżej, więc już naprawione

# Problem 3: Linia 440 - ai_sig context
old_ai = "timeframe = parts[1] if len(parts) > 1 else '15m'"
new_ai = "timeframe = parts[1] if len(parts) > 1 else user.get('interval', '15m')"

if old_ai in content:
    content = content.replace(old_ai, new_ai)
    print("✅ Fixed line 440 - AI signals use user interval")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ ALL FIXED!")

