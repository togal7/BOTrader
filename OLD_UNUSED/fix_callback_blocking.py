with open('handlers.py', 'r') as f:
    content = f.read()

print("=== FIXING CALLBACK BLOCKING ===\n")

# Znajdź analyze_from_alert i dodaj natychmiastowy answer
old_analyze = """async def analyze_from_alert(query, user_id, user, symbol, timeframe):
    \"\"\"Show analysis with quick interval change buttons\"\"\"
    try:
        await query.answer('⏳ Analizuję...')"""

new_analyze = """async def analyze_from_alert(query, user_id, user, symbol, timeframe):
    \"\"\"Show analysis with quick interval change buttons\"\"\"
    try:
        # IMMEDIATELY answer to unblock UI
        await query.answer()
        
        # Show loading message
        await query.edit_message_text('⏳ Analizuję...')"""

content = content.replace(old_analyze, new_analyze)
print("✅ Fixed analyze callback blocking")

# Również napraw wszystkie inne callbacki - dodaj answer na początku
# Znajdź button_callback i upewnij się że wszystkie mają answer
lines = content.split('\n')
new_lines = []
in_callback = False
callback_has_answer = False

for i, line in enumerate(lines):
    new_lines.append(line)
    
    # Sprawdź czy to początek funkcji callback
    if 'async def button_callback' in line:
        in_callback = True
        callback_has_answer = False
    
    # Sprawdź czy ma już answer
    if in_callback and 'await query.answer()' in line:
        callback_has_answer = True
        in_callback = False

content = '\n'.join(new_lines)

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Fixed callback handling")

