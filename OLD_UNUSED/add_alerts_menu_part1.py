with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING ALERTS MENU - PART 1 ===\n")

# 1. Dodaj przycisk "Alerty" do głównego menu
old_main = """        [InlineKeyboardButton(t('settings', lang), callback_data='settings')],"""

new_main = """        [InlineKeyboardButton(t('settings', lang), callback_data='settings')],
        [InlineKeyboardButton('🔔 Alerty', callback_data='alerts_menu')],"""

content = content.replace(old_main, new_main)
print("✅ Added Alerty button to main menu")

# 2. Dodaj handlery callbacków
old_handler = """    elif data == 'settings':
        await settings_menu(query, user_id, user)
        return"""

new_handler = """    elif data == 'settings':
        await settings_menu(query, user_id, user)
        return
    
    elif data == 'alerts_menu':
        await alerts_menu(query, user_id, user)
        return
    
    elif data == 'alerts_settings':
        await alerts_settings_menu(query, user_id, user)
        return
    
    elif data == 'alerts_history':
        await alerts_history_menu(query, user_id, user)
        return
    
    elif data.startswith('toggle_alert_'):
        alert_type = data.replace('toggle_alert_', '')
        await toggle_alert(query, user_id, user, alert_type)
        return
    
    elif data.startswith('set_scan_range_'):
        range_val = int(data.replace('set_scan_range_', ''))
        await set_scan_range(query, user_id, user, range_val)
        return
    
    elif data.startswith('set_scan_freq_'):
        freq = data.replace('set_scan_freq_', '')
        await set_scan_frequency(query, user_id, user, freq)
        return
    
    elif data == 'set_scan_range':
        await set_scan_range(query, user_id, user)
        return
    
    elif data == 'set_scan_frequency':
        await set_scan_frequency(query, user_id, user)
        return"""

content = content.replace(old_handler, new_handler)
print("✅ Added alert callbacks")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ PART 1 DONE")

