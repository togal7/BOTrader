"""
Fix Admin Panel - na podstawie odczytanej struktury z GitHub
"""

def fix_admin_panel():
    with open('handlers.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Znajdź button_callback funkcję
    button_callback_line = None
    for i, line in enumerate(lines):
        if 'async def button_callback' in line:
            button_callback_line = i
            break
    
    if not button_callback_line:
        print("❌ Nie znaleziono button_callback")
        return False
    
    # Znajdź pierwsze "elif data ==" po query = update.callback_query
    first_elif = None
    for i in range(button_callback_line, min(button_callback_line + 50, len(lines))):
        if 'elif data ==' in lines[i] or "elif data.startswith" in lines[i]:
            first_elif = i
            break
    
    if not first_elif:
        print("❌ Nie znaleziono pierwszego elif")
        return False
    
    # Sprawdź czy admin_panel już istnieje i usuń
    new_lines = []
    skip = False
    for i, line in enumerate(lines):
        if "data == 'admin_panel'" in line:
            # Usuń cały blok admin_panel (do następnego elif lub innej funkcji)
            skip = True
        
        if skip:
            # Przestań pomijać gdy natrafimy na kolejny elif na tym samym poziomie wcięcia
            if line.strip().startswith('elif ') or line.strip().startswith('async def'):
                skip = False
        
        if not skip:
            new_lines.append(line)
    
    lines = new_lines
    
    # Dodaj poprawny kod admin_panel PRZED pierwszym elif
    admin_panel_code = """    # ═══════════════════════════════════════════════════════
    # ADMIN PANEL
    # ═══════════════════════════════════════════════════════
    if data == 'admin_panel':
        user_id = query.from_user.id
        if user_id != 1794363283:
            await query.answer("⛔ Brak dostępu", show_alert=True)
            return
        
        # Pobierz statystyki
        import json
        try:
            with open('ai_signals_history.json', 'r') as f:
                signals = json.load(f)
            total_signals = len(signals)
        except:
            total_signals = 0
        
        keyboard = [
            [InlineKeyboardButton('⚡ ULTRA Manual', callback_data='ultra_manual')],
            [InlineKeyboardButton('📊 Statystyki DB', callback_data='admin_stats')],
            [InlineKeyboardButton('🏠 Menu Główne', callback_data='back_main')]
        ]
        
        text = f\"\"\"🎛️ **ADMIN PANEL**

📊 **Status Systemu:**
• Sygnałów w bazie: **{total_signals}**
• BOTrader: **Online** ✅
• ULTRA: Auto co 6h ⏰

⚡ **ULTRA Manual:**
Ręczne skanowanie 500/1000/2000 analiz

📊 **Statystyki:**
Szczegółowe dane bazy sygnałów
\"\"\"
        
        await query.edit_message_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
        return
    
    """
    
    # Wstaw kod przed pierwszym elif
    # Znajdź ponownie first_elif w nowych lines
    for i in range(button_callback_line, len(lines)):
        if 'elif data ==' in lines[i] or "elif data.startswith" in lines[i]:
            lines.insert(i, admin_panel_code)
            break
    
    # Zapisz
    with open('handlers.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Admin panel code dodany")
    return True

def add_admin_button_to_start():
    """Dodaje przycisk Admin Panel w start_command"""
    with open('handlers.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Znajdź start_command
    start_line = None
    for i, line in enumerate(lines):
        if 'async def start_command' in line:
            start_line = i
            break
    
    if not start_line:
        return False
    
    # Znajdź gdzie są InlineKeyboardButton dla AI Signals
    ai_signals_line = None
    for i in range(start_line, min(start_line + 100, len(lines))):
        if "InlineKeyboardButton('🎯 AI Signals'" in lines[i]:
            ai_signals_line = i
            break
    
    if not ai_signals_line:
        return False
    
    # Sprawdź czy admin button już jest
    for i in range(max(0, ai_signals_line - 10), ai_signals_line):
        if 'Admin Panel' in lines[i]:
            print("⚠️ Admin button już istnieje")
            return True
    
    # Dodaj admin button PRZED AI Signals
    admin_button = """    # Admin Panel button (tylko dla admina)
    if user_id == 1794363283:
        keyboard.insert(0, [InlineKeyboardButton('🎛️ Admin Panel', callback_data='admin_panel')])
    
"""
    
    lines.insert(ai_signals_line, admin_button)
    
    with open('handlers.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print("✅ Admin button dodany do start_command")
    return True

# Uruchom fixes
if __name__ == '__main__':
    print("🔧 Fixing Admin Panel...")
    if fix_admin_panel():
        print("✅ Admin panel fixed")
    
    if add_admin_button_to_start():
        print("✅ Admin button added")
    
    print("\n✅ Wszystko naprawione!")

