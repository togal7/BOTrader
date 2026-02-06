with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== MAKING NICE 2-COLUMN MENU ===\n")

# Znajdź change_interval_menu
for i, line in enumerate(lines):
    if 'async def change_interval_menu' in line:
        print(f"Found at line {i+1}")
        
        # Nowa funkcja z 2 kolumnami i skrótami
        new_func = [
            'async def change_interval_menu(query, user_id, user):\n',
            '    """Change interval"""\n',
            '    text = "⏰  WYBIERZ INTERWAŁ"\n',
            '    \n',
            '    # Timeframes with short labels\n',
            '    keyboard = [\n',
            "        [InlineKeyboardButton('1m', callback_data='set_interval_1m'), InlineKeyboardButton('5m', callback_data='set_interval_5m')],\n",
            "        [InlineKeyboardButton('15m', callback_data='set_interval_15m'), InlineKeyboardButton('30m', callback_data='set_interval_30m')],\n",
            "        [InlineKeyboardButton('1h', callback_data='set_interval_1h'), InlineKeyboardButton('4h', callback_data='set_interval_4h')],\n",
            "        [InlineKeyboardButton('12h', callback_data='set_interval_12h'), InlineKeyboardButton('1d', callback_data='set_interval_1d')],\n",
            "        [InlineKeyboardButton('3d', callback_data='set_interval_3d'), InlineKeyboardButton('5d', callback_data='set_interval_5d')],\n",
            "        [InlineKeyboardButton('1w', callback_data='set_interval_1w'), InlineKeyboardButton('2w', callback_data='set_interval_2w')],\n",
            "        [InlineKeyboardButton('1M', callback_data='set_interval_1M'), InlineKeyboardButton('3M', callback_data='set_interval_3M')],\n",
            "        [InlineKeyboardButton('6M', callback_data='set_interval_6M'), InlineKeyboardButton('1Y', callback_data='set_interval_1Y')],\n",
            "        [InlineKeyboardButton('⬅️ Powrót', callback_data='settings')]\n",
            '    ]\n',
            '    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))\n',
        ]
        
        # Znajdź koniec obecnej funkcji
        end = i
        for j in range(i, len(lines)):
            if j > i and lines[j].startswith('async def ') or lines[j].startswith('# ==='):
                end = j
                break
        
        # Zastąp
        lines[i:end] = new_func
        print(f"✅ Replaced with 2-column layout")
        break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Done!")

