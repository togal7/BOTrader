# Wstaw debug do admin_add_days_menu

with open('handlers.py', 'r') as f:
    content = f.read()

# Znajdź funkcję i dodaj debug
old_func = """    text = f\"\"\"➕ DODAJ DNI SUBSKRYPCJI

👥 Użytkowników: {len(all_users)}

Kliknij użytkownika:\"\"\""""

new_func = """    # DEBUG
    logger.info(f"admin_add_days_menu: all_users_dict type={type(all_users_dict)}, len={len(all_users_dict)}")
    logger.info(f"admin_add_days_menu: all_users (after convert) len={len(all_users)}")
    
    text = f\"\"\"➕ DODAJ DNI SUBSKRYPCJI

👥 Użytkowników: {len(all_users)}

Kliknij użytkownika:\"\"\""""

content = content.replace(old_func, new_func)

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Added debug logs")

