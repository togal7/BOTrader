with open('handlers.py', 'r') as f:
    content = f.read()

print("\n=== ADDING NOTIFICATION TOGGLE HANDLER ===\n")

# Sprawdź czy już jest
if "elif data.startswith('toggle_alert_'):" not in content:
    # Dodaj callback handler
    old_toggle = """    # Settings changes (toggle)
    if data.startswith('set_'):"""
    
    new_toggle = """    # Toggle alert settings
    elif data.startswith('toggle_alert_'):
        field = data.replace('toggle_alert_', '')
        current = settings.get(field, 0)
        db.update_alert_settings(user_id, {field: 1 if not current else 0})
        await query.answer('✅ Zapisano')
        await alerts_settings_menu(query, user_id, user)
        return
    
    # Settings changes (toggle)
    if data.startswith('set_'):"""
    
    content = content.replace(old_toggle, new_toggle)
    print("✅ Added toggle_alert_ handler")
else:
    print("✅ Handler already exists")

with open('handlers.py', 'w') as f:
    f.write(content)

