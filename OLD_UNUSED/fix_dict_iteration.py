with open('alert_scanner.py', 'r') as f:
    content = f.read()

print("=== FIXING DICT ITERATION ===\n")

# Znajdź for user_id, user_data in all_users.items():
old = "for user_id, user_data in all_users.items():"
new = "for user_id, user_data in list(all_users.items()):"

if old in content:
    content = content.replace(old, new)
    print("✅ Fixed: list(all_users.items())")

with open('alert_scanner.py', 'w') as f:
    f.write(content)

