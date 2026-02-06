"""
Add admin chat with users and broadcast functionality
"""

with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING ADMIN CHAT & BROADCAST ===\n")

# 1. Dodaj strukturę do przechowywania chatów w database.py
chat_storage_code = '''
    def get_admin_chat(self, user_id):
        """Get chat history with user"""
        user = self.get_user(user_id)
        return user.get('admin_chat_history', [])
    
    def add_admin_chat_message(self, user_id, from_admin, message, timestamp):
        """Add message to chat history"""
        user = self.get_user(user_id)
        if not user:
            return
        
        if 'admin_chat_history' not in user:
            user['admin_chat_history'] = []
        
        user['admin_chat_history'].append({
            'from_admin': from_admin,
            'message': message,
            'timestamp': timestamp
        })
        
        # Keep only last 50 messages
        user['admin_chat_history'] = user['admin_chat_history'][-50:]
        
        self.update_user(user_id, user)
'''

# Dodaj do database.py
with open('database.py', 'r') as f:
    db_content = f.read()

if 'def get_admin_chat' not in db_content:
    # Znajdź koniec klasy Database
    class_end = db_content.rfind('\n# Globalna instancja')
    if class_end == -1:
        class_end = db_content.rfind('\ndb = Database()')
    
    if class_end != -1:
        db_content = db_content[:class_end] + '\n' + chat_storage_code + db_content[class_end:]
        
        with open('database.py', 'w') as f:
            f.write(db_content)
        
        print("✅ Added chat storage to database.py")
else:
    print("✅ Chat storage already in database.py")

# 2. Update admin_chat_view
new_chat_view = '''
async def admin_chat_view(query, user_id, target_uid):
    """View and manage chat with user"""
    if user_id not in ADMIN_IDS:
        return
    
    target_user = db.get_user(target_uid)
    username = target_user.get('username', 'Unknown')
    
    # Get chat history
    chat_history = db.get_admin_chat(target_uid)
    
    if not chat_history:
        history_text = "📭 Brak wiadomości"
    else:
        history_text = "💬 HISTORIA CZATU:\\n\\n"
        
        # Show last 10 messages
        for msg in chat_history[-10:]:
            from_who = "👨‍💼 Admin" if msg['from_admin'] else f"👤 @{username}"
            timestamp = msg['timestamp'][:16]  # YYYY-MM-DD HH:MM
            text = msg['message'][:50] + "..." if len(msg['message']) > 50 else msg['message']
            history_text += f"{from_who} ({timestamp}):\\n{text}\\n\\n"
    
    text = f"""💬 CHAT Z UŻYTKOWNIKIEM

👤 User: @{username}
🆔 ID: {target_uid}

{history_text}

💡 Aby wysłać wiadomość do tego usera:
Użyj: /msg {target_uid} Twoja wiadomość"""

    keyboard = [
        [InlineKeyboardButton("🗑️ Wyczyść historię", callback_data=f"admin_clear_chat_{target_uid}")],
        [InlineKeyboardButton('⬅️ Powrót', callback_data=f'admin_user_{target_uid}')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_clear_chat(query, user_id, target_uid):
    """Clear chat history"""
    if user_id not in ADMIN_IDS:
        return
    
    target_user = db.get_user(target_uid)
    target_user['admin_chat_history'] = []
    db.update_user(target_uid, target_user)
    
    await query.answer("✅ Historia czatu wyczyszczona", show_alert=True)
    await admin_chat_view(query, user_id, target_uid)
'''

# Replace old admin_chat_view
import re
old_pattern = r'async def admin_chat_view\(query.*?\n(?:.*?\n)*?(?=async def [a-z_]+\()'

if re.search(old_pattern, content):
    content = re.sub(old_pattern, new_chat_view.strip() + '\n\n', content)
    print("✅ Updated admin_chat_view")
else:
    print("⚠️ admin_chat_view not found")

# 3. Dodaj callback dla clear chat
clear_chat_callback = '''
    elif data.startswith('admin_clear_chat_'):
        target_uid = data.replace('admin_clear_chat_', '')
        await admin_clear_chat(query, user_id, target_uid)
        return
'''

# Znajdź miejsce po innych admin callbacks
callback_insert = content.find("    elif data == 'admin_stats_detailed':")
if callback_insert != -1:
    content = content[:callback_insert] + clear_chat_callback + '\n' + content[callback_insert:]
    print("✅ Added clear_chat callback")

# 4. Dodaj /msg command handler
msg_command_code = '''
async def admin_msg_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to send message to specific user"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Brak uprawnień")
        return
    
    # Parse: /msg USER_ID message text
    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Użycie: /msg USER_ID wiadomość\\n\\n"
            "Przykład: /msg 123456789 Witaj! Jak mogę pomóc?"
        )
        return
    
    target_uid = context.args[0]
    message = ' '.join(context.args[1:])
    
    # Verify user exists
    target_user = db.get_user(target_uid)
    if not target_user:
        await update.message.reply_text(f"❌ User {target_uid} nie istnieje")
        return
    
    from datetime import datetime
    
    # Save to chat history
    db.add_admin_chat_message(target_uid, from_admin=True, message=message, 
                               timestamp=datetime.now().isoformat())
    
    # Send to user
    try:
        await context.bot.send_message(
            chat_id=target_uid,
            text=f"💬 WIADOMOŚĆ OD ADMINA:\\n\\n{message}"
        )
        
        await update.message.reply_text(
            f"✅ Wysłano do @{target_user.get('username', 'Unknown')}"
        )
        
        logger.info(f"Admin {user_id} sent message to user {target_uid}")
    except Exception as e:
        await update.message.reply_text(f"❌ Błąd wysyłania: {e}")
        logger.error(f"Failed to send admin message: {e}")
'''

# Dodaj msg_command_code przed ostatnim return w pliku
content = content.rstrip() + '\n\n' + msg_command_code + '\n'

# 5. Update broadcast menu
new_broadcast = '''
async def admin_broadcast_menu(query, user_id):
    """Broadcast message menu"""
    if user_id not in ADMIN_IDS:
        return
    
    all_users_dict = db.get_all_users()
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    total = len(all_users)
    
    text = f"""📢 BROADCAST DO WSZYSTKICH

👥 Otrzyma: {total} użytkowników

💡 Aby wysłać broadcast:
Użyj komendy:

/broadcast Twoja wiadomość do wszystkich

⚠️ Każdy użytkownik otrzyma tę wiadomość!"""

    keyboard = [[InlineKeyboardButton('⬅️ Panel Admina', callback_data='admin_panel')]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
'''

# Replace old broadcast
old_broadcast_pattern = r'async def admin_broadcast_menu\(query.*?\n(?:.*?\n)*?(?=async def [a-z_]+\()'

if re.search(old_broadcast_pattern, content):
    content = re.sub(old_broadcast_pattern, new_broadcast.strip() + '\n\n', content)
    print("✅ Updated admin_broadcast_menu")

# 6. Dodaj broadcast command
broadcast_command_code = '''
async def admin_broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to broadcast message to all users"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Brak uprawnień")
        return
    
    if not context.args:
        await update.message.reply_text(
            "Użycie: /broadcast wiadomość\\n\\n"
            "Przykład: /broadcast Witam! Nowa funkcja w bocie!"
        )
        return
    
    message = ' '.join(context.args)
    
    # Get all users
    all_users_dict = db.get_all_users()
    all_users = list(all_users_dict.values()) if isinstance(all_users_dict, dict) else all_users_dict
    
    await update.message.reply_text(f"📢 Wysyłam do {len(all_users)} użytkowników...")
    
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
    
    await update.message.reply_text(
        f"✅ Broadcast zakończony!\\n\\n"
        f"📤 Wysłano: {success}\\n"
        f"❌ Błędy: {failed}"
    )
    
    logger.info(f"Admin {user_id} broadcast: {success} success, {failed} failed")
'''

content = content.rstrip() + '\n\n' + broadcast_command_code + '\n'

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Added chat and broadcast functionality")

# 7. Dodaj handlery do bot.py
print("\n=== ADDING COMMAND HANDLERS TO BOT.PY ===\n")

with open('bot.py', 'r') as f:
    bot_content = f.read()

# Znajdź gdzie są handlery
handler_section = bot_content.find('application.add_handler(CommandHandler("start", start_command))')

if handler_section != -1:
    # Dodaj po start command
    new_handlers = '''
    # Admin commands
    application.add_handler(CommandHandler("msg", admin_msg_command))
    application.add_handler(CommandHandler("broadcast", admin_broadcast_command))
'''
    
    insert_pos = bot_content.find('\n', handler_section) + 1
    bot_content = bot_content[:insert_pos] + new_handlers + bot_content[insert_pos:]
    
    with open('bot.py', 'w') as f:
        f.write(bot_content)
    
    print("✅ Added command handlers to bot.py")
else:
    print("⚠️ Could not find handler section in bot.py")

