with open('handlers.py', 'r') as f:
    content = f.read()

# Znajdź dokładnie keyboard w show_pair_analysis
import re

# Szukam keyboard z interwałami
pattern = r"""keyboard = \[
            \[InlineKeyboardButton\('🔄 Odśwież analizę'.*?\)\],
            \[
                InlineKeyboardButton\('⏱ 15m'.*?\),
                InlineKeyboardButton\('⏱ 1h'.*?\),
                InlineKeyboardButton\('⏱ 4h'.*?\)
            \],
            \[InlineKeyboardButton\('📊 Więcej wskaźników'.*?\)\],
            \[InlineKeyboardButton\(back_label, callback_data=back_data\)\]
        \]"""

replacement = """keyboard = [
            [InlineKeyboardButton('🔄 Odśwież analizę', callback_data=f'refresh_analysis_{symbol}_{timeframe}')],
            [InlineKeyboardButton(back_label, callback_data=back_data)]
        ]"""

content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Naprawiono keyboard")

