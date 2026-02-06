"""
Make broadcast interactive - no commands needed
"""

with open('handlers.py', 'r') as f:
    content = f.read()

print("=== MAKING BROADCAST INTERACTIVE ===\n")

# 1. Update admin_broadcast_menu - dodaj stan "awaiting_broadcast"
new_broadcast_menu = '''
async def admin_broadcast_menu(query, user_id):
    """Broadcast message menu - interactive"""
    if user_id not in ADMIN_IDS:
        return
    
    all_users_dict = db.get_all_users()
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    total = len(all_users)
    
    text = f"""📢 BROADCAST DO WSZYSTKICH

👥 Otrzyma: {total} użytkowników

💡 INSTRUKCJA:
1. Kliknij "✍️ Napisz wiadomość"
2. Wyślij tekst wiadomości w czacie
3. Potwierdź wysyłkę

⚠️ Każdy użytkownik otrzyma tę wiadomość!"""

    keyboard = [
        [InlineKeyboardButton('✍️ Napisz wiadomość', callback_data='admin_broadcast_write')],
        [InlineKeyboardButton('⬅️ Panel Admina', callback_data='admin_panel')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_broadcast_write(query, user_id):
    """Set state to await broadcast message"""
    if user_id not in ADMIN_IDS:
        return
    
    # Set awaiting state
    admin_user = db.get_user(user_id)
    admin_user['awaiting_broadcast'] = True
    db.update_user(user_id, admin_user)
    
    await query.edit_message_text(
        "✍️ NAPISZ WIADOMOŚĆ BROADCAST\\n\\n"
        "Wyślij teraz wiadomość którą chcesz wysłać do wszystkich użytkowników.\\n\\n"
        "Aby anulować, wyślij /cancel"
    )

async def admin_broadcast_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE, message_text):
    """Confirm broadcast before sending"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        return
    
    all_users_dict = db.get_all_users()
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    total = len(all_users)
    
    # Preview
    preview = message_text[:200] + "..." if len(message_text) > 200 else message_text
    
    text = f"""📢 POTWIERDZENIE BROADCAST

📤 Wysyłam do: {total} użytkowników

📝 Wiadomość:
{preview}

✅ Wyślij teraz?"""

    keyboard = [
        [InlineKeyboardButton('✅ TAK, WYŚLIJ', callback_data=f'admin_broadcast_send')],
        [InlineKeyboardButton('❌ Anuluj', callback_data='admin_broadcast')]
    ]
    
    # Store message temporarily
    admin_user = db.get_user(user_id)
    admin_user['pending_broadcast'] = message_text
    admin_user['awaiting_broadcast'] = False
    db.update_user(user_id, admin_user)
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_broadcast_send(query, user_id, context):
    """Send broadcast to all users"""
    if user_id not in ADMIN_IDS:
        return
    
    # Get stored message
    admin_user = db.get_user(user_id)
    message = admin_user.get('pending_broadcast')
    
    if not message:
        await query.answer("❌ Brak wiadomości do wysłania", show_alert=True)
        return
    
    # Clear pending
    admin_user['pending_broadcast'] = None
    db.update_user(user_id, admin_user)
    
    await query.edit_message_text("📢 Wysyłam broadcast...\\n\\nProszę czekać...")
    
    # Get all users
    all_users_dict = db.get_all_users()
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    
    success = 0
    failed = 0
    
    for user_data in all_users:
        uid = user_data['user_id']
        
        try:
            await context.bot.send_message(
                chat_id=uid,
                text=f"📢 OGŁOSZENIE:\\n\\n{message}"
            )
            success += 1
            
            # Small delay to avoid rate limits
            await asyncio.sleep(0.05)
        except Exception as e:
            failed += 1
            logger.error(f"Broadcast failed for user {uid}: {e}")
    
    # Report
    text = f"""✅ BROADCAST ZAKOŃCZONY!

📤 Wysłano: {success}
❌ Błędy: {failed}

Wiadomość została dostarczona do {success} użytkowników."""

    keyboard = [[InlineKeyboardButton('⬅️ Panel Admina', callback_data='admin_panel')]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    logger.info(f"Admin {user_id} broadcast: {success} success, {failed} failed")
'''

# Replace old broadcast functions
import re

# Remove old admin_broadcast_menu
old_pattern = r'async def admin_broadcast_menu\(query.*?\n(?:.*?\n)*?(?=async def [a-z_]+\()'
if re.search(old_pattern, content):
    content = re.sub(old_pattern, '', content)
    print("✅ Removed old admin_broadcast_menu")

# Remove old admin_broadcast_command
old_cmd_pattern = r'async def admin_broadcast_command\(update.*?\n(?:.*?\n)*?(?=async def [a-z_]+\()'
if re.search(old_cmd_pattern, content):
    content = re.sub(old_cmd_pattern, '', content)
    print("✅ Removed old admin_broadcast_command")

# Add new functions at end
content = content.rstrip() + '\n\n' + new_broadcast_menu + '\n'

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Added new interactive broadcast functions")

