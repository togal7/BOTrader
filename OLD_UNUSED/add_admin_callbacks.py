"""
Add admin panel callbacks and additional functions
"""

with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING ADMIN CALLBACKS ===\n")

# 1. Dodaj callbacki do button_callback
old_callback_section = """    elif data == 'admin_panel':
        await admin_panel(query, user_id, user)
        return"""

new_callback_section = """    elif data == 'admin_panel':
        await admin_panel(query, user_id, user)
        return
    
    elif data == 'admin_users_list':
        await admin_users_list(query, user_id, user, page=0)
        return
    
    elif data.startswith('admin_users_page_'):
        page = int(data.replace('admin_users_page_', ''))
        await admin_users_list(query, user_id, user, page=page)
        return
    
    elif data.startswith('admin_user_'):
        target_uid = data.replace('admin_user_', '')
        await admin_user_manage(query, user_id, target_uid)
        return
    
    elif data.startswith('admin_chat_'):
        target_uid = data.replace('admin_chat_', '')
        await admin_chat_view(query, user_id, target_uid)
        return
    
    elif data.startswith('admin_add_days_'):
        target_uid = data.replace('admin_add_days_', '')
        await admin_add_days_menu(query, user_id, target_uid)
        return
    
    elif data.startswith('admin_remove_days_'):
        target_uid = data.replace('admin_remove_days_', '')
        await admin_remove_days_menu(query, user_id, target_uid)
        return
    
    elif data.startswith('admin_give_days_'):
        parts = data.replace('admin_give_days_', '').split('_')
        target_uid = parts[0]
        days = int(parts[1])
        await admin_give_days(query, user_id, target_uid, days)
        return
    
    elif data.startswith('admin_take_days_'):
        parts = data.replace('admin_take_days_', '').split('_')
        target_uid = parts[0]
        days = int(parts[1])
        await admin_take_days(query, user_id, target_uid, days)
        return
    
    elif data.startswith('admin_toggle_premium_'):
        target_uid = data.replace('admin_toggle_premium_', '')
        await admin_toggle_premium(query, user_id, target_uid)
        return
    
    elif data.startswith('admin_delete_confirm_'):
        target_uid = data.replace('admin_delete_confirm_', '')
        await admin_delete_user_confirm(query, user_id, target_uid)
        return
    
    elif data.startswith('admin_delete_yes_'):
        target_uid = data.replace('admin_delete_yes_', '')
        await admin_delete_user(query, user_id, target_uid)
        return
    
    elif data == 'admin_broadcast':
        await admin_broadcast_menu(query, user_id)
        return
    
    elif data == 'admin_stats_detailed':
        await admin_stats_detailed(query, user_id)
        return"""

if old_callback_section in content:
    content = content.replace(old_callback_section, new_callback_section)
    print("✅ Added admin callbacks to button_callback")
else:
    print("⚠️ Old callback not found - need manual insertion")

# 2. Dodaj funkcje pomocnicze
helper_functions = '''
# ==========================================
# ADMIN HELPER FUNCTIONS
# ==========================================

async def admin_add_days_menu(query, user_id, target_uid):
    """Show menu to add days"""
    if user_id not in ADMIN_IDS:
        return
    
    target_user = db.get_user(target_uid)
    username = target_user.get('username', 'Unknown')
    
    text = f"""➕ DODAJ DNI PREMIUM

👤 User: @{username}
🆔 ID: {target_uid}

Wybierz ile dni dodać:"""

    keyboard = [
        [InlineKeyboardButton("+ 3 dni", callback_data=f"admin_give_days_{target_uid}_3"),
         InlineKeyboardButton("+ 7 dni", callback_data=f"admin_give_days_{target_uid}_7")],
        [InlineKeyboardButton("+ 14 dni", callback_data=f"admin_give_days_{target_uid}_14"),
         InlineKeyboardButton("+ 30 dni", callback_data=f"admin_give_days_{target_uid}_30")],
        [InlineKeyboardButton("+ 90 dni", callback_data=f"admin_give_days_{target_uid}_90"),
         InlineKeyboardButton("+ 365 dni", callback_data=f"admin_give_days_{target_uid}_365")],
        [InlineKeyboardButton('⬅️ Powrót', callback_data=f'admin_user_{target_uid}')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_remove_days_menu(query, user_id, target_uid):
    """Show menu to remove days"""
    if user_id not in ADMIN_IDS:
        return
    
    target_user = db.get_user(target_uid)
    username = target_user.get('username', 'Unknown')
    
    text = f"""➖ ODEJMIJ DNI PREMIUM

👤 User: @{username}
🆔 ID: {target_uid}

Wybierz ile dni odjąć:"""

    keyboard = [
        [InlineKeyboardButton("- 3 dni", callback_data=f"admin_take_days_{target_uid}_3"),
         InlineKeyboardButton("- 7 dni", callback_data=f"admin_take_days_{target_uid}_7")],
        [InlineKeyboardButton("- 14 dni", callback_data=f"admin_take_days_{target_uid}_14"),
         InlineKeyboardButton("- 30 dni", callback_data=f"admin_take_days_{target_uid}_30")],
        [InlineKeyboardButton('⬅️ Powrót', callback_data=f'admin_user_{target_uid}')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_give_days(query, user_id, target_uid, days):
    """Add days to user subscription"""
    if user_id not in ADMIN_IDS:
        return
    
    from datetime import datetime, timedelta
    
    target_user = db.get_user(target_uid)
    username = target_user.get('username', 'Unknown')
    
    # Calculate new expiry
    current_expires = target_user.get('subscription_expires')
    
    if current_expires:
        try:
            current_date = datetime.fromisoformat(current_expires)
            # If expired, start from now
            if current_date < datetime.now():
                new_date = datetime.now() + timedelta(days=days)
            else:
                new_date = current_date + timedelta(days=days)
        except:
            new_date = datetime.now() + timedelta(days=days)
    else:
        new_date = datetime.now() + timedelta(days=days)
    
    target_user['subscription_expires'] = new_date.isoformat()
    target_user['is_premium'] = True
    
    db.update_user(target_uid, target_user)
    
    await query.answer(f"✅ Dodano {days} dni dla @{username}", show_alert=True)
    
    # Show updated user info
    await admin_user_manage(query, user_id, target_uid)
    
    logger.info(f"Admin {user_id} added {days} days to user {target_uid}")

async def admin_take_days(query, user_id, target_uid, days):
    """Remove days from user subscription"""
    if user_id not in ADMIN_IDS:
        return
    
    from datetime import datetime, timedelta
    
    target_user = db.get_user(target_uid)
    username = target_user.get('username', 'Unknown')
    
    current_expires = target_user.get('subscription_expires')
    
    if current_expires:
        try:
            current_date = datetime.fromisoformat(current_expires)
            new_date = current_date - timedelta(days=days)
            
            # Check if expired
            if new_date < datetime.now():
                target_user['is_premium'] = False
                target_user['subscription_expires'] = None
            else:
                target_user['subscription_expires'] = new_date.isoformat()
        except:
            target_user['is_premium'] = False
            target_user['subscription_expires'] = None
    
    db.update_user(target_uid, target_user)
    
    await query.answer(f"✅ Odjęto {days} dni dla @{username}", show_alert=True)
    await admin_user_manage(query, user_id, target_uid)
    
    logger.info(f"Admin {user_id} removed {days} days from user {target_uid}")

async def admin_toggle_premium(query, user_id, target_uid):
    """Toggle premium status"""
    if user_id not in ADMIN_IDS:
        return
    
    from datetime import datetime, timedelta
    
    target_user = db.get_user(target_uid)
    username = target_user.get('username', 'Unknown')
    
    is_premium = target_user.get('is_premium', False)
    
    if is_premium:
        # Block premium
        target_user['is_premium'] = False
        target_user['subscription_expires'] = None
        msg = f"🔒 Zablokowano Premium dla @{username}"
    else:
        # Unblock - give 30 days
        target_user['is_premium'] = True
        target_user['subscription_expires'] = (datetime.now() + timedelta(days=30)).isoformat()
        msg = f"🔓 Odblokowano Premium (30 dni) dla @{username}"
    
    db.update_user(target_uid, target_user)
    
    await query.answer(msg, show_alert=True)
    await admin_user_manage(query, user_id, target_uid)
    
    logger.info(f"Admin {user_id} toggled premium for user {target_uid}")

async def admin_delete_user_confirm(query, user_id, target_uid):
    """Confirm user deletion"""
    if user_id not in ADMIN_IDS:
        return
    
    target_user = db.get_user(target_uid)
    username = target_user.get('username', 'Unknown')
    
    text = f"""⚠️ POTWIERDZENIE USUNIĘCIA

Czy na pewno chcesz usunąć użytkownika?

👤 @{username}
🆔 {target_uid}

❗ Ta akcja jest NIEODWRACALNA!"""

    keyboard = [
        [InlineKeyboardButton("🗑️ TAK, USUŃ", callback_data=f"admin_delete_yes_{target_uid}"),
         InlineKeyboardButton("❌ NIE", callback_data=f"admin_user_{target_uid}")]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_delete_user(query, user_id, target_uid):
    """Delete user from database"""
    if user_id not in ADMIN_IDS:
        return
    
    target_user = db.get_user(target_uid)
    username = target_user.get('username', 'Unknown')
    
    # Delete from database
    db.users.pop(target_uid, None)
    db.save_users()
    
    await query.answer(f"✅ Usunięto @{username}", show_alert=True)
    
    # Return to users list
    await admin_users_list(query, user_id, user, page=0)
    
    logger.warning(f"Admin {user_id} DELETED user {target_uid} (@{username})")

async def admin_chat_view(query, user_id, target_uid):
    """View chat history with user"""
    if user_id not in ADMIN_IDS:
        return
    
    # TODO: Implement chat history (requires chat storage)
    await query.answer("💬 Chat history - wkrótce!", show_alert=True)

async def admin_broadcast_menu(query, user_id):
    """Broadcast message menu"""
    if user_id not in ADMIN_IDS:
        return
    
    text = """📢 BROADCAST DO WSZYSTKICH

⚠️ Funkcja wkrótce!

Aby wysłać wiadomość do wszystkich użytkowników:
1. Napisz wiadomość w czacie
2. Bot rozpozna i zapyta o potwierdzenie

Status: W BUDOWIE"""

    keyboard = [[InlineKeyboardButton('⬅️ Panel Admina', callback_data='admin_panel')]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_stats_detailed(query, user_id):
    """Detailed statistics"""
    if user_id not in ADMIN_IDS:
        return
    
    all_users_dict = db.get_all_users()
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    
    from datetime import datetime, timedelta
    
    total = len(all_users)
    active_24h = len([u for u in all_users if u.get('last_active', '') > (datetime.now() - timedelta(hours=24)).isoformat()])
    active_7d = len(db.get_active_users(7))
    premium = sum(1 for u in all_users if u.get('is_premium', False))
    total_signals = sum(u.get('signals_count', 0) for u in all_users)
    
    text = f"""📊 STATYSTYKI SZCZEGÓŁOWE

👥 Użytkownicy:
• Wszyscy: {total}
• Aktywni 24h: {active_24h}
• Aktywni 7d: {active_7d}
• Premium: {premium}

📈 Aktywność:
• Sygnały wysłane: {total_signals}
• Średnio/user: {total_signals / total if total > 0 else 0:.1f}

🔔 Alerty:
• Users z alertami: {len([u for u in all_users if any(v==1 for k,v in u.get('alert_settings',{}).items() if k.endswith('_enabled'))])}

💎 Premium:
• Aktywni: {premium}
• % wszystkich: {premium/total*100 if total > 0 else 0:.1f}%"""

    keyboard = [[InlineKeyboardButton('⬅️ Panel Admina', callback_data='admin_panel')]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
'''

# Add helper functions before last line
content = content.rstrip() + '\n\n' + helper_functions + '\n'

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Added all helper functions")

