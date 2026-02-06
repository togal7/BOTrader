with open('alert_scanner.py', 'r') as f:
    content = f.read()

print("=== REMOVING BUTTONS FROM ALERTS ===\n")

# Znajdź i usuń wszystkie przyciski z alertów
import re

# Znajdź sekcję send_alert
pattern = r'(async def send_alert.*?)(from telegram import.*?InlineKeyboardMarkup.*?keyboard = \[.*?\].*?)(await self\.app\.bot\.send_message\(.*?reply_markup=InlineKeyboardMarkup\(keyboard\),)'

def replace_func(match):
    before = match.group(1)
    buttons_section = match.group(2)
    send_part = match.group(3)
    
    # Usuń reply_markup
    new_send = send_part.replace('reply_markup=InlineKeyboardMarkup(keyboard),', '')
    
    return before + new_send

content = re.sub(pattern, replace_func, content, flags=re.DOTALL)

# Alternatywna metoda - prosta zamiana
content = content.replace(
    """            # Send Telegram message with button
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            
            keyboard = [
                [InlineKeyboardButton('📜 Zobacz historię', callback_data='alerts_history')],
                [InlineKeyboardButton('⚙️ Ustawienia alertów', callback_data='alerts_settings')],
                [InlineKeyboardButton('🏠 Menu główne', callback_data='back_main')]
            ]
            
            await self.app.bot.send_message(
                chat_id=user_id,
                text=f"🔔 ALERT\\n\\n{message}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=None
            )""",
    """            # Send Telegram message (no buttons - won't block bot)
            await self.app.bot.send_message(
                chat_id=user_id,
                text=f"🔔 ALERT\\n\\n{message}\\n\\n💡 Menu → Alerty → Historia",
                parse_mode=None
            )"""
)

print("✅ Removed buttons from alerts")

with open('alert_scanner.py', 'w') as f:
    f.write(content)

