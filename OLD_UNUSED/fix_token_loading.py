# Najpierw sprawdź jak bot.py ładuje token
with open('bot.py', 'r') as f:
    bot_content = f.read()

# Znajdź jak ładuje token
import re
token_load = None

# Szukaj różnych możliwości
if 'from config import' in bot_content and 'TOKEN' in bot_content:
    # Sprawdź config.py
    with open('config.py', 'r') as f:
        config = f.read()
    
    # Znajdź token w config
    match = re.search(r'TOKEN\s*=\s*["\']([^"\']+)["\']', config)
    if match:
        token = match.group(1)
        print(f"Found TOKEN in config.py: {token[:20]}...")
        token_load = f'TOKEN = "{token}"'
    else:
        # Sprawdź os.getenv w config
        if 'os.getenv' in config:
            match = re.search(r'os\.getenv\(["\']([^"\']+)["\']\)', config)
            if match:
                env_var = match.group(1)
                print(f"Config uses os.getenv('{env_var}')")
                token_load = f'import os\nTOKEN = os.getenv("{env_var}")'

if not token_load:
    print("Using default .env approach")
    token_load = '''import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent / '.env'
load_dotenv(env_path)
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env!")'''

# Update alert_sender.py
with open('alert_sender.py', 'r') as f:
    content = f.read()

# Replace the broken import section
old_import = '''import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")'''

content = content.replace(old_import, token_load)

with open('alert_sender.py', 'w') as f:
    f.write(content)

print("✅ Fixed token loading")

