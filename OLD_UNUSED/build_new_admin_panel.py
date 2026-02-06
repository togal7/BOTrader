"""
Build new Admin Panel with user management
"""

admin_panel_code = '''
# ==========================================
# ADMIN PANEL - NEW VERSION
# ==========================================

async def admin_panel(query, user_id, user):
    """Main admin panel with statistics"""
    if user_id not in ADMIN_IDS:
        await query.answer("❌ Brak uprawnień", show_alert=True)
        return
    
    all_users_dict = db.get_all_users()
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    
    total_users = len(all_users)
    active_users = len(db.get_active_users(7))
    premium_users = sum(1 for u in all_users if u.get('is_premium', False))
    total_signals = sum(u.get('signals_count', 0) for u in all_users)

    text = f"""👨‍💼 PANEL ADMINA

📊 STATYSTYKI:
• Użytkownicy: {total_users}
• Aktywni (7 dni): {active_users}
• Premium: {premium_users}
• Wysłane sygnały: {total_signals}

⚙️ ZARZĄDZANIE:"""

    keyboard = [
        [InlineKeyboardButton("👥 Użytkownicy", callback_data='admin_users_list')],
        [InlineKeyboardButton("📢 Broadcast", callback_data='admin_broadcast')],
        [InlineKeyboardButton("📊 Statystyki", callback_data='admin_stats_detailed')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='back_main')]
    ]

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_users_list(query, user_id, user, page=0):
    """Show paginated list of users"""
    if user_id not in ADMIN_IDS:
        return
    
    all_users_dict = db.get_all_users()
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    
    # Sort by last_active (newest first)
    all_users.sort(key=lambda u: u.get('last_active', ''), reverse=True)
    
    # Pagination
    per_page = 10
    total_pages = (len(all_users) + per_page - 1) // per_page
    start_idx = page * per_page
    end_idx = start_idx + per_page
    page_users = all_users[start_idx:end_idx]
    
    text = f"""👥 UŻYTKOWNICY ({len(all_users)})

📄 Strona {page + 1}/{total_pages}

Kliknij aby zarządzać:"""

    keyboard = []
    
    for u in page_users:
        uid = u['user_id']
        username = u.get('username', 'Unknown')
        is_premium = u.get('is_premium', False)
        
        # Premium status
        if is_premium:
            expires = u.get('subscription_expires')
            if expires:
                try:
                    from datetime import datetime
                    expires_date = datetime.fromisoformat(expires)
                    days_left = (expires_date - datetime.now()).days
                    status = f"💎 {days_left}d"
                except:
                    status = "💎"
            else:
                status = "💎"
        else:
            status = "⚪"
        
        # Last active
        last = u.get('last_active', '')
        if last:
            try:
                from datetime import datetime
                last_date = datetime.fromisoformat(last)
                last_str = last_date.strftime('%d.%m')
            except:
                last_str = '?'
        else:
            last_str = '?'
        
        button_text = f"{status} {uid[:8]}... @{username} ({last_str})"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"admin_user_{uid}")])
    
    # Navigation
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅️ Poprzednia", callback_data=f"admin_users_page_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Następna ➡️", callback_data=f"admin_users_page_{page+1}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    keyboard.append([InlineKeyboardButton('⬅️ Panel Admina', callback_data='admin_panel')])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_user_manage(query, user_id, target_user_id):
    """Manage specific user"""
    if user_id not in ADMIN_IDS:
        return
    
    target_user = db.get_user(target_user_id)
    if not target_user:
        await query.answer("❌ Użytkownik nie znaleziony", show_alert=True)
        return
    
    username = target_user.get('username', 'Unknown')
    is_premium = target_user.get('is_premium', False)
    expires = target_user.get('subscription_expires')
    signals = target_user.get('signals_count', 0)
    last_active = target_user.get('last_active', 'Nigdy')
    
    # Format expiry
    if is_premium and expires:
        try:
            from datetime import datetime
            exp_date = datetime.fromisoformat(expires)
            days_left = (exp_date - datetime.now()).days
            exp_str = f"{exp_date.strftime('%Y-%m-%d')} ({days_left} dni)"
        except:
            exp_str = expires
    else:
        exp_str = "Brak"
    
    # Format last active
    if last_active and last_active != 'Nigdy':
        try:
            from datetime import datetime
            last_date = datetime.fromisoformat(last_active)
            last_str = last_date.strftime('%Y-%m-%d %H:%M')
        except:
            last_str = last_active[:16]
    else:
        last_str = "Nigdy"
    
    text = f"""👤 ZARZĄDZANIE UŻYTKOWNIKIEM

🆔 ID: {target_user_id}
👤 Username: @{username}
💎 Premium: {'Tak' if is_premium else 'Nie'}
📅 Wygasa: {exp_str}
📊 Sygnały: {signals}
🕐 Ostatnia aktywność: {last_str}

Wybierz akcję:"""

    keyboard = [
        [InlineKeyboardButton("💬 Chat z userem", callback_data=f"admin_chat_{target_user_id}")],
        [InlineKeyboardButton("➕ Dodaj dni", callback_data=f"admin_add_days_{target_user_id}"),
         InlineKeyboardButton("➖ Odejmij dni", callback_data=f"admin_remove_days_{target_user_id}")],
        [InlineKeyboardButton("🔒 Blokuj Premium" if is_premium else "🔓 Odblokuj Premium", 
                            callback_data=f"admin_toggle_premium_{target_user_id}")],
        [InlineKeyboardButton("🗑️ Usuń usera", callback_data=f"admin_delete_confirm_{target_user_id}")],
        [InlineKeyboardButton('⬅️ Lista użytkowników', callback_data='admin_users_list')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
'''

print("Writing new admin panel code...")

with open('handlers.py', 'r') as f:
    content = f.read()

# Find old admin panel and replace
import re

# Find admin_panel function
old_admin_pattern = r'async def admin_panel\(query.*?\n(?:.*?\n)*?(?=async def [a-z_]+\(|# ={5,})'

# Check if exists
if re.search(old_admin_pattern, content):
    print("✅ Found old admin_panel, replacing...")
    content = re.sub(old_admin_pattern, admin_panel_code.strip() + '\n\n', content, count=1)
else:
    print("⚠️ Old admin_panel not found, appending...")
    # Add before the last function or at end
    content += '\n\n' + admin_panel_code

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ New admin panel code added!")

