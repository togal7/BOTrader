with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING HARDCODED TEXTS ===\n")

# Lista zamian (PL → t())
replacements = [
    # 1. Skanuję
    ('f"🔍 Skanuję {EXCHANGES[exchange][\'name\']}...\\n\\nCzekaj..."',
     'f"🔍 {t(\'scanning\', get_user_language(user))} {EXCHANGES[exchange][\'name\']}...\\n\\n{t(\'please_wait\', get_user_language(user))}..."'),
    
    # 2. Szukam
    ('f"🔍 Szukam \'{search_term}\' na {EXCHANGES[exchange][\'name\']}..."',
     'f"🔍 {t(\'searching\', lang)} \'{search_term}\' {t(\'on\', lang)} {EXCHANGES[exchange][\'name\']}..."'),
    
    # 3. Wyniki wyszukiwania
    ('f"🔍 WYNIKI WYSZUKIWANIA\\n\\nZnaleziono: {len(matching)} par\\n\\n"',
     'f"🔍 {t(\'search_results\', lang).upper()}\\n\\n{t(\'found\', lang)}: {len(matching)} {t(\'pairs\', lang)}\\n\\n"'),
    
    # 4. Proszę czekać (w ai_scan)
    ('⏳  Proszę czekać...',
     '⏳  {t(\'please_wait\', lang)}...'),
    
    # 5. Znaleziono (w ai_scan)
    ('📊 Znaleziono: {len(results)} sygnałów',
     '📊 {t(\'found\', lang)}: {len(results)} {t(\'signals\', lang)}'),
    
    # 6. Znaleziono (w cached)
    ('🔍 Znaleziono: {len(cached)} sygnałów',
     '🔍 {t(\'found\', lang)}: {len(cached)} {t(\'signals\', lang)}'),
    
    # 7. Analizuję
    ('⏳  Analizuję...',
     '⏳  {t(\'analyzing\', lang)}...'),
    
    # 8. Proszę czekać ~10 sekund
    ('Proszę czekać ~10 sekund...',
     '{t(\'please_wait\', lang)} ~10 {t(\'seconds\', lang)}...'),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"✅ Replaced: {old[:50]}...")
    else:
        print(f"⚠️ Not found: {old[:50]}...")

# Dodaj lang = get_user_language(user) gdzie brak
# W handle_text_message
if 'async def handle_text_message' in content:
    # Sprawdź czy ma lang
    lines = content.split('\n')
    new_lines = []
    in_handle_text = False
    has_lang = False
    
    for i, line in enumerate(lines):
        if 'async def handle_text_message' in line:
            in_handle_text = True
        
        if in_handle_text and 'lang = get_user_language(user)' in line:
            has_lang = True
        
        if in_handle_text and 'search_term = ' in line and not has_lang:
            # Wstaw lang PRZED search_term
            indent = len(line) - len(line.lstrip())
            new_lines.append(' ' * indent + 'lang = get_user_language(user)\n')
            has_lang = True
            print("✅ Added lang to handle_text_message")
        
        new_lines.append(line)
        
        if in_handle_text and line.strip().startswith('async def ') and 'handle_text_message' not in line:
            in_handle_text = False
    
    content = '\n'.join(new_lines)

with open('handlers.py', 'w') as f:
    f.write(content)

print(f"\n✅ Total: {count} replacements")

