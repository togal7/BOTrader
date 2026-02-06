with open('handlers.py', 'r') as f:
    content = f.read()

print("STEP 3: Adding callback handlers\n")

# Znajdź i zamień handler scan_
old_handler = """    elif data.startswith('scan_'):
        await handle_scan(query, user_id, user, data)
        return"""

new_handler = """    elif data.startswith('scan_select_'):
        # Menu wyboru rozmiaru
        scan_type = data.replace('scan_select_', '')
        await scan_size_menu(query, user_id, user, scan_type)
        return
    
    elif data.startswith('scan_') and '_' in data:
        # scan_TYPE_SIZE (np. scan_gainers_50)
        parts = data.replace('scan_', '').rsplit('_', 1)
        if len(parts) == 2:
            scan_type = f'scan_{parts[0]}'
            size_str = parts[1]
            size = int(size_str) if size_str.isdigit() else 9999  # 'all' = 9999
            await handle_scan(query, user_id, user, scan_type, size)
        return
    
    elif data.startswith('scan_'):
        # Stary format (fallback)
        await handle_scan(query, user_id, user, data, 50)
        return"""

if old_handler in content:
    content = content.replace(old_handler, new_handler)
    print("✅ Replaced scan_ handler")
else:
    print("❌ Could not find old handler")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ Step 3 complete")

