with open('alert_scanner.py', 'r') as f:
    lines = f.readlines()

print("=== FORCE FIXING SEND_ALERT ===\n")

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Znajdź linię z await self.app.bot.send_message
    if 'await self.app.bot.send_message' in line and 'send_alert' in ''.join(lines[max(0,i-20):i]):
        print(f"Found send_message at line {i+1}")
        
        # Wstaw PRZED nią check + keyboard
        indent = '            '
        new_lines.extend([
            indent + '# Check if user wants notifications\n',
            indent + 'settings = db.get_alert_settings(user_id)\n',
            indent + 'notifications_on = settings.get("notifications_enabled", 1)\n',
            indent + '\n',
            indent + 'if notifications_on:\n',
            indent + '    from telegram import InlineKeyboardButton, InlineKeyboardMarkup\n',
            indent + '    timeframe = settings.get("alert_timeframe", "1h")\n',
            indent + '    symbol_encoded = symbol.replace("/", "_").replace(":", "_")\n',
            indent + '    keyboard = [\n',
            indent + '        [InlineKeyboardButton(f"📊 Analiza {symbol.split(\'/\')[0]} ({timeframe})", callback_data=f"analyze_{symbol_encoded}_{timeframe}")],\n',
            indent + '        [InlineKeyboardButton("📜 Historia", callback_data="alerts_history")]\n',
            indent + '    ]\n',
            indent + '    \n',
        ])
        
        # Dodaj wcięcie do send_message (wewnątrz if)
        new_lines.append('    ' + line)
        i += 1
        
        # Następne 4 linijki też muszą być wcięte (text, parse_mode, )
        for j in range(4):
            if i < len(lines):
                if 'parse_mode' in lines[i]:
                    # Dodaj reply_markup przed parse_mode
                    new_lines.append('                reply_markup=InlineKeyboardMarkup(keyboard),\n')
                new_lines.append('    ' + lines[i])
                i += 1
        
        # Dodaj else
        new_lines.extend([
            indent + 'else:\n',
            indent + '    logger.info(f"Saved to history (notifications OFF): {user_id} - {symbol}")\n',
            '\n'
        ])
        
        print("✅ Inserted notification check + keyboard")
        continue
    
    new_lines.append(line)
    i += 1

with open('alert_scanner.py', 'w') as f:
    f.writelines(new_lines)

print("\n✅ Done!")

