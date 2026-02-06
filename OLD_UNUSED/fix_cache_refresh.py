with open('handlers.py', 'r') as f:
    lines = f.readlines()

# Znajdź show_cached_scan (linia 1163)
for i, line in enumerate(lines):
    if 'async def show_cached_scan(query, user_id, user):' in line:
        # Dodaj pobieranie świeżego user z DB na początku funkcji
        # Wstaw po linii z def
        insert_pos = i + 2  # Po def i po docstring
        
        new_code = """    # Pobierz świeży user z DB (z zapisanym cache)
    user = db.get_user(user_id)
    
"""
        
        lines.insert(insert_pos, new_code)
        print(f"✅ Added fresh user fetch at line {insert_pos+1}")
        break

with open('handlers.py', 'w') as f:
    f.writelines(lines)

print("✅ Fixed cache refresh!")

