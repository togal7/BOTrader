with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING ADMIN - DICT TO LIST ===\n")

# Linia 712: all_users.sort - ale all_users to dict!
old_code = """    all_users = db.get_all_users()
    all_users.sort(key=lambda u: u.get('last_active', ''), reverse=True)"""

new_code = """    all_users_dict = db.get_all_users()
    # Convert dict to list
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    all_users.sort(key=lambda u: u.get('last_active', ''), reverse=True)"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ Fixed admin get_all_users")
else:
    print("⚠️ Pattern not found")

with open('handlers.py', 'w') as f:
    f.write(content)

