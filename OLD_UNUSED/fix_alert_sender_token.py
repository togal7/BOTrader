with open('alert_sender.py', 'r') as f:
    content = f.read()

# Replace import
content = content.replace(
    'from config import BOT_TOKEN',
    'import os\nfrom dotenv import load_dotenv\n\nload_dotenv()\nBOT_TOKEN = os.getenv("BOT_TOKEN")'
)

with open('alert_sender.py', 'w') as f:
    f.write(content)

print("✅ Fixed BOT_TOKEN import")

