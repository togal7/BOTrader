"""
Make admin chat fully interactive (no commands)
"""

with open('handlers.py', 'r') as f:
    content = f.read()

print("=== MAKING ADMIN CHAT INTERACTIVE ===\n")

# 1. Update admin_chat_view - usuń instrukcję /msg
new_chat_view = '''
async def admin_chat_view(query, user_id, target_uid):
    """View and manage chat with user - INTERACTIVE"""
    if user_id not in ADMIN_IDS:
        return
    
    target_user = db.get_user(target_uid)
    username = target_user.get('username', 'Unknown')
    
    # Get chat history
    chat_history = db.get_admin_chat(target_uid)
    
    if not chat_history:
        history_text = "📭 Brak wiadomości"
    else:
        history_text = "💬 OSTATNIE WIADOMOŚCI:\\n\\n"
        
        # Show last 5 messages
        for msg in chat_history[-5:]:
            from_who = "👨‍💼 Admin" if msg['from_admin'] else f"👤 @{username}"
            timestamp = msg['timestamp'][:16]  # YYYY-MM-DD HH:MM
            text = msg['message'][:80] + "..." if len(msg['message']) > 80 else msg['message']
            history_text += f"{from_who} ({timestamp}):\\n{text}\\n\\n"
    
    text = f"""💬 CHAT Z UŻYTKOWNIKIEM

👤 User: @{username}
🆔 ID: {target_uid}

{history_text}"""

    keyboard = [
        [InlineKeyboardButton("✍️ Napisz wiadomość", callback_data=f"admin_msg_write_{target_uid}")],
        [InlineKeyboardButton("🗑️ Wyczyść historię", callback_data=f"admin_clear_chat_{target_uid}")],
        [InlineKeyboardButton('⬅️ Powrót', callback_data=f'admin_user_{target_uid}')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def admin_msg_write(query, user_id, target_uid):
    """Set state to await message to specific user"""
    if user_id not in ADMIN_IDS:
        return
    
    target_user = db.get_user(target_uid)
    username = target_user.get('username', 'Unknown')
    
    # Set awaiting state
    admin_user = db.get_user(user_id)
    admin_user['awaiting_admin_message'] = target_uid
    db.update_user(user_id, admin_user)
    
    await query.edit_message_text(
        f"✍️ WIADOMOŚĆ DO @{username}\\n\\n"
        f"Napisz teraz wiadomość którą chcesz wysłać.\\n\\n"
        f"Aby anulować, wyślij /cancel"
    )

async def admin_msg_send(update: Update, context: ContextTypes.DEFAULT_TYPE, target_uid, message_text):
    """Send message to specific user"""
    user_id = update.effective_user.id
    
    if user_id not in ADMIN_IDS:
        return
    
    target_user = db.get_user(target_uid)
    if not target_user:
        await update.message.reply_text(f"❌ User {target_uid} nie istnieje")
        return
    
    username = target_user.get('username', 'Unknown')
    
    from datetime import datetime
    
    # Save to chat history
    db.add_admin_chat_message(target_uid, from_admin=True, message=message_text, 
                               timestamp=datetime.now().isoformat())
    
    # Send to user
    try:
        await context.bot.send_message(
            chat_id=target_uid,
            text=f"💬 WIADOMOŚĆ OD ADMINA:\\n\\n{message_text}"
        )
        
        await update.message.reply_text(
            f"✅ Wysłano do @{username}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('💬 Powrót do chatu', callback_data=f'admin_chat_{target_uid}')],
                [InlineKeyboardButton('👤 Powrót do usera', callback_data=f'admin_user_{target_uid}')]
            ])
        )
        
        logger.info(f"Admin {user_id} sent message to user {target_uid}")
    except Exception as e:
        await update.message.reply_text(f"❌ Błąd wysyłania: {e}")
        logger.error(f"Failed to send admin message: {e}")

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

# Replace old functions
import re

# Remove old admin_chat_view
pattern = r'async def admin_chat_view\(query.*?\n(?:.*?\n)*?(?=async def [a-z_]+\()'
if re.search(pattern, content):
    content = re.sub(pattern, '', content)
    print("✅ Removed old admin_chat_view")

# Remove old admin_msg_command
pattern = r'async def admin_msg_command\(update.*?\n(?:.*?\n)*?(?=async def [a-z_]+\()'
if re.search(pattern, content):
    content = re.sub(pattern, '', content)
    print("✅ Removed old admin_msg_command")

# Remove admin_clear_chat if exists
pattern = r'async def admin_clear_chat\(query.*?\n(?:.*?\n)*?(?=async def [a-z_]+\()'
if re.search(pattern, content):
    content = re.sub(pattern, '', content)
    print("✅ Removed old admin_clear_chat")

# Add new functions
content = content.rstrip() + '\n\n' + new_chat_view + '\n'

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Added new interactive chat functions")

