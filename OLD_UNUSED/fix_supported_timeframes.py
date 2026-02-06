# 1. Config.py - tylko obsługiwane
with open('config.py', 'r') as f:
    content = f.read()

old_tf = """TIMEFRAMES = {
    '1m': {'label': '1 minuta'},
    '5m': {'label': '5 minut'},
    '15m': {'label': '15 minut'},
    '30m': {'label': '30 minut'},
    '1h': {'label': '1 godzina'},
    '4h': {'label': '4 godziny'},
    '12h': {'label': '12 godzin'},
    '1d': {'label': '1 dzień'},
    '3d': {'label': '3 dni'},
    '5d': {'label': '5 dni'},
    '1w': {'label': '1 tydzień'},
    '2w': {'label': '2 tygodnie'},
    '1M': {'label': '1 miesiąc'},
    '3M': {'label': '3 miesiące'},
    '6M': {'label': '6 miesięcy'},
    '1Y': {'label': '1 rok'}
}"""

new_tf = """TIMEFRAMES = {
    '1m': {'label': '1 minuta'},
    '5m': {'label': '5 minut'},
    '15m': {'label': '15 minut'},
    '30m': {'label': '30 minut'},
    '1h': {'label': '1 godzina'},
    '4h': {'label': '4 godziny'},
    '8h': {'label': '8 godzin'},
    '1d': {'label': '1 dzień'},
    '1w': {'label': '1 tydzień'},
    '1M': {'label': '1 miesiąc'}
}"""

content = content.replace(old_tf, new_tf)

with open('config.py', 'w') as f:
    f.write(content)

print("✅ Config.py - tylko obsługiwane przez MEXC")

# 2. Handlers.py - zaktualizuj menu
with open('handlers.py', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'async def change_interval_menu' in line:
        new_func = [
            'async def change_interval_menu(query, user_id, user):\n',
            '    """Change interval"""\n',
            '    text = "⏰  WYBIERZ INTERWAŁ"\n',
            '    \n',
            '    keyboard = [\n',
            "        [InlineKeyboardButton('1m', callback_data='set_interval_1m'), InlineKeyboardButton('5m', callback_data='set_interval_5m'), InlineKeyboardButton('15m', callback_data='set_interval_15m')],\n",
            "        [InlineKeyboardButton('30m', callback_data='set_interval_30m'), InlineKeyboardButton('1h', callback_data='set_interval_1h'), InlineKeyboardButton('4h', callback_data='set_interval_4h')],\n",
            "        [InlineKeyboardButton('8h', callback_data='set_interval_8h'), InlineKeyboardButton('1d', callback_data='set_interval_1d'), InlineKeyboardButton('1w', callback_data='set_interval_1w')],\n",
            "        [InlineKeyboardButton('1M', callback_data='set_interval_1M')],\n",
            "        [InlineKeyboardButton('⬅️ Powrót', callback_data='settings')]\n",
            '    ]\n',
            '    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))\n',
        ]
        
        end = i
        for j in range(i, len(lines)):
            if j > i and (lines[j].startswith('async def ') or lines[j].startswith('# ===')):
                end = j
                break
        
        lines[i:end] = new_func
        print(f"✅ Handlers.py - menu z 10 obsługiwanymi interwałami")
        break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

