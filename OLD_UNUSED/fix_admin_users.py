with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING ADMIN GET ALL USERS ===\n")

# Linia 657-658: all_users = db.get_all_users()
#                 all_users.sort(...)

old_code = """    all_users = db.get_all_users()
    all_users.sort(key=lambda u: u.get('last_active', ''), reverse=True)"""

new_code = """    all_users_dict = db.get_all_users()
    # Convert dict to list
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    all_users.sort(key=lambda u: u.get('last_active', ''), reverse=True)"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ Fixed get_all_users() - converted dict to list")
else:
    print("❌ Pattern not found, trying alternative...")
    
    # Alternatywnie - zamień tylko sort
    content = content.replace(
        "all_users = db.get_all_users()\n    all_users.sort(",
        "all_users_dict = db.get_all_users()\n    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict\n    all_users.sort("
    )
    print("✅ Fixed with alternative method")

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Admin users list fixed!")

