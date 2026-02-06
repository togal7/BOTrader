"""
Dodaj kontrolki admina - bez regex, ręcznie
"""

with open('handlers.py', 'r') as f:
    content = f.read()

# 1. Dodaj import na początku main_menu
import_line = "from admin_features_config import is_feature_enabled"

if import_line not in content:
    # Znajdź main_menu i dodaj import
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        new_lines.append(line)
        
        # Po definicji main_menu dodaj import
        if 'async def main_menu(update' in line:
            next_line = lines[i+1] if i+1 < len(lines) else ''
            if 'from admin_features_config' not in next_line:
                new_lines.append('    from admin_features_config import is_feature_enabled')
    
    content = '\n'.join(new_lines)
    print("✅ Dodano import is_feature_enabled")

# 2. Zmień konkretne linie z przyciskami
# Subskrypcja
old_sub = "[InlineKeyboardButton('💎 Subskrypcja', callback_data='subscription')]"
new_sub = "[InlineKeyboardButton('💎 Subskrypcja', callback_data='subscription')] if is_feature_enabled('subscription_enabled') else []"

if old_sub in content and new_sub not in content:
    content = content.replace(
        '        [InlineKeyboardButton(\'💎 Subskrypcja\', callback_data=\'subscription\')],',
        '        [InlineKeyboardButton(\'💎 Subskrypcja\', callback_data=\'subscription\')] if is_feature_enabled(\'subscription_enabled\') else [],',
        1  # tylko pierwsze wystąpienie
    )
    print("✅ Dodano conditional dla Subskrypcja")

# Polecenia
old_ref = "[InlineKeyboardButton('🎁 Polecenia', callback_data='referral_menu')]"

if old_ref in content:
    content = content.replace(
        '        [InlineKeyboardButton(\'🎁 Polecenia\', callback_data=\'referral_menu\')],',
        '        [InlineKeyboardButton(\'🎁 Polecenia\', callback_data=\'referral_menu\')] if is_feature_enabled(\'referral_enabled\') else [],',
        1
    )
    print("✅ Dodano conditional dla Polecenia")

# 3. Dodaj filtr pustych list
# Znajdź keyboard = [ w main_menu
if 'keyboard = [' in content and 'keyboard = [row for row in' not in content:
    # Wrap keyboard w filter
    lines = content.split('\n')
    new_lines = []
    in_main_menu = False
    kb_start = None
    
    for i, line in enumerate(lines):
        if 'async def main_menu' in line:
            in_main_menu = True
        elif in_main_menu and 'async def ' in line and 'main_menu' not in line:
            in_main_menu = False
        
        if in_main_menu and 'keyboard = [' in line and 'InlineKeyboardButton' in line:
            kb_start = i
        
        new_lines.append(line)
    
    if kb_start:
        # Znajdź koniec keyboard (najbliższe ])
        kb_end = None
        bracket_count = 0
        for i in range(kb_start, len(new_lines)):
            line = new_lines[i]
            bracket_count += line.count('[') - line.count(']')
            if bracket_count == 0 and ']' in line:
                kb_end = i
                break
        
        if kb_end:
            # Zmień tylko tę linię końcową
            new_lines[kb_end] = new_lines[kb_end].replace(']', '] # End keyboard list')
            # Dodaj filter na następnej linii
            indent = '    '
            new_lines.insert(kb_end + 1, f'{indent}keyboard = [row for row in keyboard if row]  # Remove empty rows')
            print("✅ Dodano filter pustych list")
    
    content = '\n'.join(new_lines)

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ handlers.py zaktualizowany (clean)")

