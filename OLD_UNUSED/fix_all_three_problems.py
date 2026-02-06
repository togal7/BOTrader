from datetime import datetime, timedelta

with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING 3 PROBLEMS ===\n")

# 1. Fix start_command - dodaj 7 dni premium dla nowych
old_create = """    if not user_data:
        user_data = {
            'user_id': user_id,
            'username': user.username or 'Unknown',
            'first_name': user.first_name or '',
            'selected_exchange': 'mexc',
            'interval': '15m',
            'is_premium': False,
            'subscription_expires': None,
            'is_blocked': False,
            'signals_count': 0,
            'last_active': datetime.now().isoformat()
        }
        db.add_user(user_data)"""

new_create = """    if not user_data:
        # Nowi użytkownicy dostają 7 dni premium
        expires = (datetime.now() + timedelta(days=7)).isoformat()
        user_data = {
            'user_id': user_id,
            'username': user.username or 'Unknown',
            'first_name': user.first_name or '',
            'selected_exchange': 'mexc',
            'interval': '15m',
            'is_premium': True,
            'subscription_expires': expires,
            'is_blocked': False,
            'signals_count': 0,
            'last_active': datetime.now().isoformat()
        }
        db.add_user(user_data)
        logger.info(f"New user {user_id} created with 7 days premium")"""

content = content.replace(old_create, new_create)
print("✅ Added 7 days premium for new users")

# 2. Fix admin_add_days_menu - pokaż WSZYSTKICH
old_list = """async def admin_add_days_menu(query, user_id, user):
    \"\"\"Add days - show users list\"\"\"
    all_users_dict = db.get_all_users()
    # Convert dict to list
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    all_users.sort(key=lambda u: u.get('last_active', ''), reverse=True)

    text = f\"\"\"➕ DODAJ DNI SUBSKRYPCJI"""

new_list = """async def admin_add_days_menu(query, user_id, user):
    \"\"\"Add days - show users list\"\"\"
    all_users_dict = db.get_all_users()
    
    # FIX: Convert properly - db returns dict with user_id as keys
    if isinstance(all_users_dict, dict):
        all_users = list(all_users_dict.values())
    else:
        all_users = all_users_dict
    
    # Sort by last_active
    all_users.sort(key=lambda u: u.get('last_active', '') if isinstance(u, dict) else '', reverse=True)

    text = f\"\"\"➕ DODAJ DNI SUBSKRYPCJI"""

content = content.replace(old_list, new_list)
print("✅ Fixed user list conversion")

# 3. Fix admin panel - użyj TEGO SAMEGO co stats
old_panel = """async def admin_panel(query, user_id, user):
    \"\"\"Admin panel\"\"\"
    all_users = db.get_all_users()
    total_users = len(all_users)
    active_users = len(db.get_active_users(7))

    text = f\"\"\"👨‍💼 PANEL ADMINA

📊 Statystyki:
• Użytkownicy: {total_users}
• Aktywni (7 dni): {active_users}

⚙️ Zarządzanie:\"\"\""""

new_panel = """async def admin_panel(query, user_id, user):
    \"\"\"Admin panel\"\"\"
    all_users_dict = db.get_all_users()
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    total_users = len(all_users)
    active_users = len(db.get_active_users(7))
    premium_users = sum(1 for u in all_users if u.get('is_premium', False))

    text = f\"\"\"👨‍💼 PANEL ADMINA

📊 Statystyki:
• Użytkownicy: {total_users}
• Aktywni (7 dni): {active_users}
• Premium: {premium_users}

⚙️ Zarządzanie:\"\"\""""

content = content.replace(old_panel, new_panel)
print("✅ Fixed admin panel stats")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ ALL 3 PROBLEMS FIXED!")

