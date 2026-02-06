with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING SEARCH ===\n")

# Po znalezieniu par, zresetuj awaiting_search
old_code = """        text = f"🔍 WYNIKI WYSZUKIWANIA\\n\\nZnaleziono: {len(matching)} par\\n\\n"
        keyboard = []"""

new_code = """        text = f"🔍 WYNIKI WYSZUKIWANIA\\n\\nZnaleziono: {len(matching)} par\\n\\n"
        
        # Reset awaiting_search
        user['awaiting_search'] = False
        db.update_user(user_id, user)
        
        keyboard = []"""

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ Added awaiting_search reset")

with open('handlers.py', 'w') as f:
    f.write(content)

