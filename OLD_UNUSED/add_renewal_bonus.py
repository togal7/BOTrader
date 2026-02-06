"""
Add renewal bonus - when referred user extends premium
"""

with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING RENEWAL BONUS TRIGGER ===\n")

# Dodaj funkcję do wywoływania przy przedłużeniu
renewal_trigger = '''
async def trigger_referral_renewal_bonus(context, renewed_user_id):
    """Trigger referral bonus when user renews premium"""
    result = db.add_referral_renewal_bonus(renewed_user_id)
    
    if result:
        # Notify referrer about bonus
        try:
            await context.bot.send_message(
                chat_id=result['referrer_id'],
                text=f"💰 BONUS POLECENIOWY!\\n\\n"
                     f"@{db.get_user(renewed_user_id).get('username', 'Unknown')} przedłużył Premium!\\n"
                     f"Otrzymujesz: +{result['bonus_days']} dni bonusu 🎁"
            )
            
            logger.info(f"Renewal bonus: {result['referrer_id']} got +{result['bonus_days']} days")
        except:
            pass
'''

# Dodaj na końcu
content = content.rstrip() + '\n\n' + renewal_trigger + '\n'

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Added renewal bonus trigger")
print("\n💡 Note: Call this function when user extends premium (payment system)")

