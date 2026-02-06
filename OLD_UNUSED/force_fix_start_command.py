with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== FORCE FIXING start_command ===\n")

# Znajdź linię 67 (async def start_command)
new_lines = []
in_start_command = False
replaced = False

for i, line in enumerate(lines):
    if i == 66 and 'async def start_command' in line:  # linia 67 (index 66)
        in_start_command = True
        new_lines.append(line)
        
        # Dodaj całą NOWĄ funkcję
        new_lines.extend([
            '    """Start command - main menu"""\n',
            '    user = update.effective_user\n',
            '    user_id = user.id\n',
            '\n',
            '    # Get or create user\n',
            '    user_data = db.get_user(user_id)\n',
            '    if not user_data:\n',
            '        user_data = {\n',
            "            'user_id': user_id,\n",
            "            'username': user.username or 'Unknown',\n",
            "            'first_name': user.first_name or '',\n",
            "            'selected_exchange': 'mexc',\n",
            "            'interval': '15m',\n",
            "            'is_premium': False,\n",
            "            'subscription_expires': None,\n",
            "            'is_blocked': False,\n",
            "            'signals_count': 0,\n",
            "            'last_active': datetime.now().isoformat()\n",
            '        }\n',
            '        db.add_user(user_data)\n',
            '\n',
            '    # Format status\n',
            "    sub_status = format_subscription_status(user_data.get('subscription_expires'), user_data.get('is_blocked', False))\n",
            '    is_admin = user_id in ADMIN_IDS\n',
            '\n',
            '    welcome = f"""👋 BOTrader Bot\n',
            '\n',
            'Status: {sub_status}\n',
            '🆔 ID: {user_id}\n',
            '\n',
            '✨ Wpisz nazwę pary (np. BTC) aby wyszukać\n',
            '📊 Lub użyj menu poniżej"""\n',
            '\n',
            '    keyboard = [\n',
            '        [InlineKeyboardButton("🔍 Wyszukaj parę", callback_data=\'search_pair\')],\n',
            '        [InlineKeyboardButton("📊 Skaner ekstremów", callback_data=\'scan_extremes\')],\n',
            '        [InlineKeyboardButton("🎯 Sygnały AI", callback_data=\'ai_signals\')],\n',
            '        [InlineKeyboardButton("🔔 Alerty", callback_data=\'alerts_menu\')],\n',
            '        [InlineKeyboardButton("💬 Czat z adminem", callback_data=\'admin_chat\')],\n',
            '        [InlineKeyboardButton("⚙️ Ustawienia", callback_data=\'settings\')],\n',
            '        [InlineKeyboardButton("💎 Subskrypcja", callback_data=\'subscription\')],\n',
            '        [InlineKeyboardButton("ℹ️ Wyjaśnienia", callback_data=\'explanations_menu\')],\n',
            '        [InlineKeyboardButton("⭐ Oceń bota", callback_data=\'rate_bot\')]\n',
            '    ]\n',
            '\n',
            '    if is_admin:\n',
            '        keyboard.append([InlineKeyboardButton("👑 Admin Panel", callback_data=\'admin_panel\')])\n',
            '\n',
            '    await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard))\n',
            '\n',
            '\n'
        ])
        
        # Skip do następnej funkcji async def
        skip = True
        continue
    
    # Skipuj starą zawartość start_command
    if in_start_command:
        if line.startswith('async def ') or line.startswith('def '):
            in_start_command = False
            new_lines.append(line)
        continue
    
    new_lines.append(line)

with open('handlers.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Replaced start_command")

