with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING USER COUNT ===\n")

# Znajdź i zamień kolejność - najpierw deduplikacja, POTEM text
old_order = """    text = f\"\"\"➕ DODAJ DNI SUBSKRYPCJI

👥 Użytkowników: {len(all_users)}

Kliknij użytkownika:\"\"\"

    keyboard = []

    keyboard.append([InlineKeyboardButton('🎁 +7 dni WSZYSTKIM', callback_data='admin_promo_all_7')])
    keyboard.append([InlineKeyboardButton('🎁 +30 dni WSZYSTKIM', callback_data='admin_promo_all_30')])
    keyboard.append([InlineKeyboardButton('─────────────', callback_data='ignore')])

    # Usuń duplikaty po user_id
    seen_ids = set()
    unique_users = []
    for u in all_users:
        if u['user_id'] not in seen_ids:
            seen_ids.add(u['user_id'])
            unique_users.append(u)"""

new_order = """    # Usuń duplikaty po user_id NAJPIERW
    seen_ids = set()
    unique_users = []
    for u in all_users:
        if u['user_id'] not in seen_ids:
            seen_ids.add(u['user_id'])
            unique_users.append(u)
    
    # POTEM pokaż prawidłową liczbę
    text = f\"\"\"➕ DODAJ DNI SUBSKRYPCJI

👥 Użytkowników: {len(unique_users)}

Kliknij użytkownika:\"\"\"

    keyboard = []

    keyboard.append([InlineKeyboardButton('🎁 +7 dni WSZYSTKIM', callback_data='admin_promo_all_7')])
    keyboard.append([InlineKeyboardButton('🎁 +30 dni WSZYSTKIM', callback_data='admin_promo_all_30')])
    keyboard.append([InlineKeyboardButton('─────────────', callback_data='ignore')])"""

content = content.replace(old_order, new_order)
print("✅ Fixed: count unique_users AFTER deduplication")

# Usuń debug logi
content = content.replace("""    # DEBUG
    logger.info(f"admin_add_days_menu: all_users_dict type={type(all_users_dict)}, len={len(all_users_dict)}")
    logger.info(f"admin_add_days_menu: all_users (after convert) len={len(all_users)}")
    
""", "")
print("✅ Removed debug logs")

with open('handlers.py', 'w') as f:
    f.write(content)

