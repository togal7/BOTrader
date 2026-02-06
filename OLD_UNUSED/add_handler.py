with open('handlers.py', 'r') as f:
    content = f.read()

# Sprawdź czy handler istnieje
if "elif data == 'show_cached_scan':" in content:
    print("✅ Handler już istnieje")
else:
    print("❌ Handler NIE istnieje - dodaję...")
    
    # Znajdź miejsce - przed 'ai_signals' lub po 'refresh_analysis'
    insert_before = """    elif data == 'ai_signals':"""
    
    new_handler = """    elif data == 'show_cached_scan':
        await show_cached_scan(query, user_id, user)
        return
    
"""
    
    if insert_before in content:
        content = content.replace(insert_before, new_handler + insert_before)
        print("✅ Dodano handler show_cached_scan")
    else:
        print("❌ Nie znaleziono miejsca wstawienia!")

with open('handlers.py', 'w') as f:
    f.write(content)

