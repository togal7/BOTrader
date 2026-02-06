with open('handlers.py', 'r') as f:
    content = f.read()

print("=== RENAMING BOT ===\n")

# Zamień wszystkie wystąpienia
replacements = [
    ('BOTrader', 'BOTrader'),
    ('Bot BOTrader', 'BOTrader'),
    ('BOTrader Bot', 'BOTrader'),
]

count = 0
for old, new in replacements:
    occurrences = content.count(old)
    if occurrences > 0:
        content = content.replace(old, new)
        count += occurrences
        print(f"✅ Zamieniono '{old}' → '{new}' ({occurrences}x)")

with open('handlers.py', 'w') as f:
    f.write(content)

print(f"\n✅ Total: {count} zmian")

