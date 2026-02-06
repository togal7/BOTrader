"""
Add referral menu - CLEAN version without breaking escapes
"""

with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING REFERRAL MENU (CLEAN) ===\n")

# Kod bez literalnych \n - wszystko w """ strings
referral_code = '''
async def referral_menu(query, user_id, user):
    """Referral system menu"""
    from datetime import datetime
    
    referral_code = user.get('referral_code', 'ERROR')
    referrals = user.get('referrals', [])
    total_bonus = user.get('referral_bonus_days', 0)
    referred_by = user.get('referred_by')
    
    active_refs = len(referrals)
    
    referrer_text = ""
    if referred_by:
        referrer = db.get_user(referred_by)
        if referrer:
            ref_username = referrer.get('username', 'Unknown')
            referrer_text = f"""
📌 Dołączyłeś przez: @{ref_username}"""
    
    text = f"""💰 SYSTEM POLECEŃ

🎁 TWÓJ KOD: {referral_code}

🔗 Link do udostępnienia:
https://t.me/BOTraderBot?start={referral_code}

📊 STATYSTYKI:
• Poleconych użytkowników: {active_refs}
• Otrzymane dni bonusu: {total_bonus} dni{referrer_text}

🎯 JAK TO DZIAŁA?

1️⃣ Udostępnij swój kod znajomym
2️⃣ Gdy się zarejestrują - dostajecie po +15 dni Premium
3️⃣ Gdy przedłużą Premium - dostajesz +3 dni

💎 Im więcej polecisz, tym więcej bonusu!"""

    keyboard = [
        [InlineKeyboardButton("👥 Moi poleceni", callback_data='referral_list')],
        [InlineKeyboardButton("📋 Jak udostępnić?", callback_data='referral_howto')],
        [InlineKeyboardButton('⬅️ Menu Główne', callback_data='back_main')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def referral_list(query, user_id, user):
    """Show list of referred users"""
    referrals = user.get('referrals', [])
    
    if not referrals:
        text = """👥 POLECENI UŻYTKOWNICY

📭 Nie poleciłeś jeszcze nikogo.

💡 Udostępnij swój kod znajomym!
Za każdego nowego użytkownika:
• Ty: +15 dni Premium
• Twój znajomy: +15 dni Premium"""
    else:
        text = f"""👥 POLECENI UŻYTKOWNICY ({len(referrals)})

"""
        
        for i, ref in enumerate(referrals[-10:], 1):
            username = ref.get('username', 'Unknown')
            joined = ref.get('joined_at', '')[:10]
            bonus = ref.get('bonus_given', 15)
            
            text += f"{i}. @{username}\\n   Dołączył: {joined} | Bonus: +{bonus}d\\n\\n"
        
        if len(referrals) > 10:
            text += f"\\n... i {len(referrals) - 10} więcej"
    
    keyboard = [[InlineKeyboardButton('⬅️ Polecenia', callback_data='referral_menu')]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def referral_howto(query, user_id, user):
    """How to share referral"""
    referral_code = user.get('referral_code', 'ERROR')
    
    text = f"""📋 JAK UDOSTĘPNIĆ KOD?

🔗 LINK:
https://t.me/BOTraderBot?start={referral_code}

📱 SPOSOBY UDOSTĘPNIENIA:

1️⃣ Wyślij link bezpośrednio:
   • WhatsApp, Messenger, SMS
   • Media społecznościowe
   • Grupy tradingowe

2️⃣ Skopiuj kod: {referral_code}
   • Znajomy wpisuje: /start {referral_code}

3️⃣ Udostępnij screenshot tego ekranu

💡 WSKAZÓWKI:

✅ Udostępniaj w grupach tradingowych
✅ Pokaż swoje wyniki z bota
✅ Wyjaśnij że dostaną +15 dni Premium
❌ Nie spamuj - udostępniaj naturalnie"""

    keyboard = [[InlineKeyboardButton('⬅️ Polecenia', callback_data='referral_menu')]]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
'''

# Dodaj na końcu (bezpiecznie)
content = content.rstrip() + '\n\n' + referral_code + '\n'

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Added referral functions")

