with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING ADMIN ISSUES ===\n")

# 1. Napraw admin_stats_menu - ten sam problem dict→list
old_stats = """    all_users = db.get_all_users()
    total = len(all_users)
    premium = sum(1 for u in all_users if u.get('is_premium', False))"""

new_stats = """    all_users_dict = db.get_all_users()
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    total = len(all_users)
    premium = sum(1 for u in all_users if u.get('is_premium', False))"""

if old_stats in content:
    content = content.replace(old_stats, new_stats)
    print("✅ Fixed admin_stats_menu")

# 2. Usuń duplikaty - pokazuj tylko TOP 15 UNIKALNYCH użytkowników
old_users_loop = """    for u in all_users[:15]:
        uid = u['user_id']"""

new_users_loop = """    # Usuń duplikaty po user_id
    seen_ids = set()
    unique_users = []
    for u in all_users:
        if u['user_id'] not in seen_ids:
            seen_ids.add(u['user_id'])
            unique_users.append(u)
    
    for u in unique_users[:15]:
        uid = u['user_id']"""

if old_users_loop in content:
    content = content.replace(old_users_loop, new_users_loop)
    print("✅ Removed duplicates")

with open('handlers.py', 'w') as f:
    f.write(content)

