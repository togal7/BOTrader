with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING start_command_from_callback ===\n")

# Znajdź i zamień
old_callback = """    keyboard = [
        [InlineKeyboardButton("🔍 Wyszukaj parę", callback_data='search_pair')],
        [InlineKeyboardButton("📊 Skaner ekstremów", callback_data='scan_extremes')],
        [InlineKeyboardButton("🎯 Sygnały AI", callback_data='ai_signals')],
        [InlineKeyboardButton("⚙️ Ustawienia", callback_data='settings')],
        [InlineKeyboardButton("💎 Subskrypcja", callback_data='subscription')],
        [InlineKeyboardButton("💬 Czat z adminem", callback_data='admin_chat')],
        [InlineKeyboardButton("⭐ Oceń bota", callback_data='rate_bot')]
    ]"""

new_callback = """    keyboard = [
        [InlineKeyboardButton("🔍 Wyszukaj parę", callback_data='search_pair')],
        [InlineKeyboardButton("📊 Skaner ekstremów", callback_data='scan_extremes')],
        [InlineKeyboardButton("🎯 Sygnały AI", callback_data='ai_signals')],
        [InlineKeyboardButton("🔔 Alerty", callback_data='alerts_menu')],
        [InlineKeyboardButton("💬 Czat z adminem", callback_data='admin_chat')],
        [InlineKeyboardButton("⚙️ Ustawienia", callback_data='settings')],
        [InlineKeyboardButton("💎 Subskrypcja", callback_data='subscription')],
        [InlineKeyboardButton("ℹ️ Wyjaśnienia", callback_data='explanations_menu')],
        [InlineKeyboardButton("⭐ Oceń bota", callback_data='rate_bot')]
    ]"""

if old_callback in content:
    content = content.replace(old_callback, new_callback)
    print("✅ Added Alerty and Wyjaśnienia to callback menu")
else:
    print("⚠️ Pattern not found, checking alternative...")
    # Może być bez "⭐ Oceń bota"
    alt_old = """    keyboard = [
        [InlineKeyboardButton("🔍 Wyszukaj parę", callback_data='search_pair')],
        [InlineKeyboardButton("📊 Skaner ekstremów", callback_data='scan_extremes')],
        [InlineKeyboardButton("🎯 Sygnały AI", callback_data='ai_signals')],
        [InlineKeyboardButton("⚙️ Ustawienia", callback_data='settings')],
        [InlineKeyboardButton("💎 Subskrypcja", callback_data='subscription')],
        [InlineKeyboardButton("💬 Czat z adminem", callback_data='admin_chat')]
    ]"""
    
    if alt_old in content:
        content = content.replace(alt_old, new_callback)
        print("✅ Added buttons (alternative pattern)")

with open('handlers.py', 'w') as f:
    f.write(content)

