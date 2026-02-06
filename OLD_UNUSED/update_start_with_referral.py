"""
Update start_command to handle referral codes
"""

with open('handlers.py', 'r') as f:
    content = f.read()

print("=== UPDATING start_command WITH REFERRAL ===\n")

import re

# Znajdź start_command
pattern = r'(async def start_command\(update: Update, context: ContextTypes\.DEFAULT_TYPE\):.*?user_id = .*?\n.*?user = db\.get_user\(user_id\))'

replacement = r'''\1
    
    # Check for referral code in /start command
    referral_code = None
    if context.args and len(context.args) > 0:
        referral_code = context.args[0].upper()
        logger.info(f"User {user_id} started with referral code: {referral_code}")
    
    # If new user with referral code
    if referral_code and not user.get('referred_by'):
        result = db.apply_referral_code(user_id, referral_code)
        
        if result:
            # Reload user data
            user = db.get_user(user_id)
            
            # Send success message to new user
            await update.message.reply_text(
                f"🎉 KOD POLECAJĄCY ZASTOSOWANY!\\n\\n"
                f"Polecił Cię: @{result['referrer_username']}\\n"
                f"Otrzymujesz: +{result['bonus_days']} dni Premium\\n\\n"
                f"Witaj w BOTrader! 🚀"
            )
            
            # Notify referrer
            try:
                await context.bot.send_message(
                    chat_id=result['referrer_id'],
                    text=f"🎉 NOWY UŻYTKOWNIK Z TWOJEGO KODU!\\n\\n"
                         f"@{user.get('username', 'Unknown')} dołączył przez Twój kod!\\n"
                         f"Otrzymujesz: +{result['bonus_days']} dni Premium 💎"
                )
            except:
                pass  # Referrer might have blocked bot
            
            logger.info(f"Referral successful: {user_id} referred by {result['referrer_id']}")
        else:
            await update.message.reply_text(
                "⚠️ Nieprawidłowy kod polecający lub już został użyty."
            )'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Updated start_command with referral handling")

