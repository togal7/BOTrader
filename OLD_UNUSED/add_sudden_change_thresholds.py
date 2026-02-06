"""
Add multiple threshold options for sudden changes
"""

with open('handlers.py', 'r') as f:
    content = f.read()

print("=== UPDATING SUDDEN CHANGE THRESHOLD MENU ===\n")

# Znajdź set_sudden_threshold_menu i zastąp
import re

old_menu = r'async def set_sudden_threshold_menu\(query, user_id, user\):.*?await query\.edit_message_text\(text, reply_markup=InlineKeyboardMarkup\(keyboard\)\)'

new_menu = '''async def set_sudden_threshold_menu(query, user_id, user):
    """Menu for sudden change threshold - multiple options"""
    settings = user.get('alert_settings', {})
    current = settings.get('sudden_threshold', 5)
    
    text = f"""🔔 PRÓG NAGŁYCH ZMIAN

Obecny próg: ±{current}%

Wybierz czułość alertów:

📊 PROFILE TRADINGOWE:

• 25% (±5%) - Day Trading ⚡
  Bardzo czułe, dużo alertów
  
• 50% (±10%) - Swing Trading 📈
  Balans - rekomendowane ⭐
  
• 75% (±15%) - Position Trading 📊
  Większe ruchy
  
• 90% (±20%) - Long-term 🎯
  Tylko znaczące zmiany
  
• 100%+ (±25%+) - Extreme Only 💥
  Tylko epicki ruchy

💡 Im niższy próg, tym więcej alertów!"""

    keyboard = [
        [InlineKeyboardButton('25% (±5%) ⚡', callback_data='set_sudden_thresh_5'),
         InlineKeyboardButton('50% (±10%) ⭐', callback_data='set_sudden_thresh_10')],
        [InlineKeyboardButton('75% (±15%) 📊', callback_data='set_sudden_thresh_15'),
         InlineKeyboardButton('90% (±20%) 🎯', callback_data='set_sudden_thresh_20')],
        [InlineKeyboardButton('100%+ (±25%+) 💥', callback_data='set_sudden_thresh_25')],
        [InlineKeyboardButton('⬅️ Powrót', callback_data='alerts_sudden_settings')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))'''

# Replace
content = re.sub(old_menu, new_menu, content, flags=re.DOTALL)
print("✅ Updated set_sudden_threshold_menu")

# Znajdź handler set_sudden_threshold i update
old_handler = r'async def set_sudden_threshold\(query, user_id, user, threshold\):.*?await alerts_sudden_settings\(query, user_id, user\)'

new_handler = '''async def set_sudden_threshold(query, user_id, user, threshold):
    """Set sudden change threshold"""
    settings = user.get('alert_settings', {})
    settings['sudden_threshold'] = threshold
    user['alert_settings'] = settings
    
    db.update_user(user_id, user)
    
    # Map threshold to profile name
    profiles = {
        5: "Day Trading (±5%)",
        10: "Swing Trading (±10%)",
        15: "Position Trading (±15%)",
        20: "Long-term (±20%)",
        25: "Extreme Only (±25%+)"
    }
    
    profile_name = profiles.get(threshold, f"±{threshold}%")
    
    await query.answer(f"✅ Ustawiono: {profile_name}", show_alert=True)
    await alerts_sudden_settings(query, user_id, user)'''

content = re.sub(old_handler, new_handler, content, flags=re.DOTALL)
print("✅ Updated set_sudden_threshold handler")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ Menu updated with 5 threshold options")

