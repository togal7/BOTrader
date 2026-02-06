with open('handlers.py', 'r') as f:
    lines = f.readlines()

print("=== MANUAL REPLACEMENT ===\n")

# Znajdź change_interval_menu
for i, line in enumerate(lines):
    if 'async def change_interval_menu' in line:
        print(f"Found at line {i+1}")
        
        # Następne 8 linii to stara funkcja - zastąp
        new_func = [
            'async def change_interval_menu(query, user_id, user):\n',
            '    """Change interval"""\n',
            '    text = "⏰  WYBIERZ INTERWAŁ\\n\\nDostępne:"\n',
            '    \n',
            '    # Hardcoded timeframes - 16 intervals\n',
            '    custom_tfs = {\n',
            "        '1m': '1 minuta', '5m': '5 minut', '15m': '15 minut', '30m': '30 minut',\n",
            "        '1h': '1 godzina', '4h': '4 godziny', '12h': '12 godzin',\n",
            "        '1d': '1 dzień', '3d': '3 dni', '5d': '5 dni',\n",
            "        '1w': '1 tydzień', '2w': '2 tygodnie',\n",
            "        '1M': '1 miesiąc', '3M': '3 miesiące', '6M': '6 miesięcy', '1Y': '1 rok'\n",
            '    }\n',
            '    \n',
            '    keyboard = []\n',
            '    for tf_id, tf_label in custom_tfs.items():\n',
            '        keyboard.append([InlineKeyboardButton(tf_label, callback_data=f\'set_interval_{tf_id}\')])\n',
            "    keyboard.append([InlineKeyboardButton('⬅️ Powrót', callback_data='settings')])\n",
            '    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))\n',
        ]
        
        # Zastąp linie i+0 do i+8
        lines[i:i+8] = new_func
        print(f"✅ Replaced lines {i+1} to {i+8}")
        break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("\n✅ Done!")

