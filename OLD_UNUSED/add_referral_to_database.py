"""
Add referral system to database
"""

with open('database.py', 'r') as f:
    content = f.read()

print("=== ADDING REFERRAL SYSTEM TO DATABASE ===\n")

# Dodaj funkcje do klasy Database
referral_functions = '''
    def generate_referral_code(self, user_id):
        """Generate unique 6-character referral code"""
        import random
        import string
        
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            
            # Check if code already exists
            exists = False
            for uid, user_data in self.users.items():
                if user_data.get('referral_code') == code:
                    exists = True
                    break
            
            if not exists:
                return code
    
    def apply_referral_code(self, new_user_id, referral_code):
        """Apply referral code when new user registers"""
        from datetime import datetime, timedelta
        
        # Find referrer by code
        referrer_id = None
        for uid, user_data in self.users.items():
            if user_data.get('referral_code') == referral_code:
                referrer_id = uid
                break
        
        if not referrer_id:
            return None  # Invalid code
        
        # Don't allow self-referral
        if referrer_id == new_user_id:
            return None
        
        # Get both users
        new_user = self.get_user(new_user_id)
        referrer = self.get_user(referrer_id)
        
        # Check if new user already has been referred
        if new_user.get('referred_by'):
            return None  # Already used a code
        
        # Apply referral
        new_user['referred_by'] = referrer_id
        
        # Give +15 days to new user
        if new_user.get('is_premium'):
            expires = new_user.get('subscription_expires')
            if expires:
                try:
                    exp_date = datetime.fromisoformat(expires)
                    new_exp = exp_date + timedelta(days=15)
                except:
                    new_exp = datetime.now() + timedelta(days=15)
            else:
                new_exp = datetime.now() + timedelta(days=15)
        else:
            new_exp = datetime.now() + timedelta(days=15)
            new_user['is_premium'] = True
        
        new_user['subscription_expires'] = new_exp.isoformat()
        
        # Give +15 days to referrer
        if referrer.get('is_premium'):
            expires = referrer.get('subscription_expires')
            if expires:
                try:
                    exp_date = datetime.fromisoformat(expires)
                    ref_new_exp = exp_date + timedelta(days=15)
                except:
                    ref_new_exp = datetime.now() + timedelta(days=15)
            else:
                ref_new_exp = datetime.now() + timedelta(days=15)
        else:
            ref_new_exp = datetime.now() + timedelta(days=15)
            referrer['is_premium'] = True
        
        referrer['subscription_expires'] = ref_new_exp.isoformat()
        
        # Add to referrer's list
        if 'referrals' not in referrer:
            referrer['referrals'] = []
        
        referrer['referrals'].append({
            'user_id': new_user_id,
            'username': new_user.get('username', 'Unknown'),
            'joined_at': datetime.now().isoformat(),
            'bonus_given': 15
        })
        
        # Track total bonus days
        referrer['referral_bonus_days'] = referrer.get('referral_bonus_days', 0) + 15
        
        # Save
        self.update_user(new_user_id, new_user)
        self.update_user(referrer_id, referrer)
        
        return {
            'referrer_id': referrer_id,
            'referrer_username': referrer.get('username', 'Unknown'),
            'bonus_days': 15
        }
    
    def add_referral_renewal_bonus(self, renewed_user_id):
        """Give +3 days bonus to referrer when referred user renews"""
        from datetime import datetime, timedelta
        
        user = self.get_user(renewed_user_id)
        referrer_id = user.get('referred_by')
        
        if not referrer_id:
            return None  # Not referred
        
        referrer = self.get_user(referrer_id)
        if not referrer:
            return None
        
        # Give +3 days to referrer
        if referrer.get('is_premium'):
            expires = referrer.get('subscription_expires')
            if expires:
                try:
                    exp_date = datetime.fromisoformat(expires)
                    new_exp = exp_date + timedelta(days=3)
                except:
                    new_exp = datetime.now() + timedelta(days=3)
            else:
                new_exp = datetime.now() + timedelta(days=3)
        else:
            new_exp = datetime.now() + timedelta(days=3)
            referrer['is_premium'] = True
        
        referrer['subscription_expires'] = new_exp.isoformat()
        referrer['referral_bonus_days'] = referrer.get('referral_bonus_days', 0) + 3
        
        self.update_user(referrer_id, referrer)
        
        return {
            'referrer_id': referrer_id,
            'referrer_username': referrer.get('username', 'Unknown'),
            'bonus_days': 3
        }
'''

# Znajdź koniec klasy Database
import re
pattern = r'(class Database:.*?)(\n# Globalna instancja|\ndb = Database\(\))'

def replacement(match):
    return match.group(1) + '\n' + referral_functions + '\n' + match.group(2)

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('database.py', 'w') as f:
    f.write(content)

print("✅ Added referral functions to Database class")

