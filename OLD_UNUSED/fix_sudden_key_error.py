with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING KEY ERROR ===\n")

# Znajdź funkcję btn w alerts_settings_menu
old_btn = """    def btn(name, field):
        emoji = '✅ ' if settings[field] else '❌ '
        return InlineKeyboardButton(f'{emoji} {name}', callback_data=f'toggle_alert_{field}')"""

new_btn = """    def btn(name, field):
        emoji = '✅ ' if settings.get(field, 0) else '❌ '
        return InlineKeyboardButton(f'{emoji} {name}', callback_data=f'toggle_alert_{field}')"""

content = content.replace(old_btn, new_btn)
print("✅ Fixed btn() to use .get()")

with open('handlers.py', 'w') as f:
    f.write(content)

