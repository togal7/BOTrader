with open('handlers.py', 'r') as f:
    content = f.read()

print("STEP 4: Modifying handle_scan to accept size\n")

# 1. Zmień definicję funkcji
old_def = "async def handle_scan(query, user_id, user, scan_type):"
new_def = "async def handle_scan(query, user_id, user, scan_type, scan_size=50):"

if old_def in content:
    content = content.replace(old_def, new_def)
    print("✅ Changed function signature")
else:
    print("⚠️ Function signature already changed or not found")

# 2. Dodaj limit w pętli skanowania
# Znajdź: for symbol in list(symbols)[:50]:
old_loop = "        for symbol in list(symbols)[:50]:"

new_loop = """        # Limit do wybranego rozmiaru
        scan_limit = min(scan_size, len(symbols)) if scan_size < 9999 else len(symbols)
        logger.info(f'Scanning {scan_limit}/{len(symbols)} pairs')
        
        for symbol in list(symbols)[:scan_limit]:"""

if old_loop in content:
    content = content.replace(old_loop, new_loop)
    print("✅ Added scan limit to loop")
else:
    print("⚠️ Loop pattern not found - checking alternative")
    
    # Może już jest futures_symbols
    old_loop2 = "        for symbol in list(futures_symbols):"
    new_loop2 = """        # Limit do wybranego rozmiaru
        scan_limit = min(scan_size, len(futures_symbols)) if scan_size < 9999 else len(futures_symbols)
        logger.info(f'Scanning {scan_limit}/{len(futures_symbols)} pairs')
        
        for symbol in list(futures_symbols)[:scan_limit]:"""
    
    if old_loop2 in content:
        content = content.replace(old_loop2, new_loop2)
        print("✅ Added scan limit (futures version)")

with open('handlers.py', 'w') as f:
    f.write(content)

print("\n✅ Step 4 complete - ALL DONE!")

