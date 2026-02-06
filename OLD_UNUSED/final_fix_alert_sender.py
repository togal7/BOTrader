with open('alert_sender.py', 'r') as f:
    content = f.read()

# Usuń cały broken import section
import re

# Znajdź i usuń od "import os" do "raise ValueError"
pattern = r'import os.*?raise ValueError\("BOT_TOKEN not found in \.env!"\)'
content = re.sub(pattern, 'from config import TELEGRAM_BOT_TOKEN as BOT_TOKEN', content, flags=re.DOTALL)

with open('alert_sender.py', 'w') as f:
    f.write(content)

print("✅ Changed to: from config import TELEGRAM_BOT_TOKEN")

