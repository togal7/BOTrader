with open('handlers.py', 'r') as f:
    content = f.read()

print("=== UNIFYING START MENU ===\n")

# 1. Zmień start_command aby używał TEJ SAMEJ logiki
old_start = """async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"Start command - main menu\"\"\"
    user = update.effective_user
    user_id = user.id

    # Get or create user
    user_data = db.get_user(user_id)
    if not user_data:
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

new_start = """async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    \"\"\"Start command - main menu\"\"\"
    user = update.effective_user
    user_id = user.id

    # Get or create user
    user_data = db.get_user(user_id)
    if not user_data:
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
        db.add_user(user_data)
    
    # Use SAME menu as callback version
    sub_status = format_subscription_status(user_data.get('subscription_expires'), user_data.get('is_blocked', False))
    is_admin = user_id in ADMIN_IDS
    
    welcome = f\"\"\"👋 BOTrader Bot

Status: {sub_status}
🆔 ID: {user_id}

✨ Wpisz nazwę pary (np. BTC) aby wyszukać
📊 Lub użyj menu poniżej\"\"\"
    
    keyboard = [
        [InlineKeyboardButton("🔍 Wyszukaj parę", callback_data='search_pair')],
        [InlineKeyboardButton("📊 Skaner ekstremów", callback_data='scan_extremes')],
        [InlineKeyboardButton("🎯 Sygnały AI", callback_data='ai_signals')],
        [InlineKeyboardButton("🔔 Alerty", callback_data='alerts_menu')],
        [InlineKeyboardButton("💬 Czat z adminem", callback_data='admin_chat')],
        [InlineKeyboardButton("⚙️ Ustawienia", callback_data='settings')],
        [InlineKeyboardButton("💎 Subskrypcja", callback_data='subscription')],
        [InlineKeyboardButton("ℹ️ Wyjaśnienia", callback_data='explanations_menu')],
        [InlineKeyboardButton("⭐ Oceń bota", callback_data='rate_bot')]
    ]
    
    if is_admin:
        keyboard.append([InlineKeyboardButton("👑 Admin Panel", callback_data='admin_panel')])
    
    await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard))"""

content = content.replace(old_start, new_start)
print("✅ Unified start_command to match callback version")

# 2. Upewnij się że back_main używa start_command_from_callback
old_back = "elif data == 'back_main':\n        await start_command(update, context)"
new_back = "elif data == 'back_main':\n        await start_command_from_callback(query, user_id, user)"

if old_back in content:
    content = content.replace(old_back, new_back)
    print("✅ Fixed back_main to use callback version")

with open('handlers.py', 'w') as f:
    f.write(content)

