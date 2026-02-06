with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING SEARCH DISPLAY ===\n")

# W handle_text_message, gdzie tworzy przyciski
old_button = """        for symbol in matching[:20]:
            keyboard.append([InlineKeyboardButton(f"📊 {symbol}", callback_data=f'analyze_{symbol}')])"""

new_button = """        for symbol in matching[:20]:
            display_symbol = symbol.replace(':USDT', '')
            keyboard.append([InlineKeyboardButton(f"📊 {display_symbol}", callback_data=f'analyze_{symbol}')])"""

if old_button in content:
    content = content.replace(old_button, new_button)
    print("✅ Fixed search display - removed :USDT")

with open('handlers.py', 'w') as f:
    f.write(content)

