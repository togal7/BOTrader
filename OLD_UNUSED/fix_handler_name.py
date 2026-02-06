with open('bot.py', 'r') as f:
    content = f.read()

# Zmień nazwę
content = content.replace('handle_message', 'handle_text_message')

with open('bot.py', 'w') as f:
    f.write(content)

print("✅ Fixed handler name")

