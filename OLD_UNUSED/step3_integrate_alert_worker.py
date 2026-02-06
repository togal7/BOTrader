"""
STEP 3: Integrate Alert Worker with Main Bot
1. Remove alert_scanner import/usage from bot.py
2. Add alert sender loop to bot
3. Update alert settings to notify worker
"""

import re

print("=" * 60)
print("STEP 3: Integrating Alert Worker with Main Bot")
print("=" * 60)

# 1. Update bot.py - remove old alert_scanner
with open('bot.py', 'r') as f:
    bot_content = f.read()

print("\n1️⃣ Removing old alert_scanner from bot.py...")

# Remove import
bot_content = bot_content.replace('from alert_scanner import AlertScanner', '# Alert scanner moved to alert_worker.py')
bot_content = bot_content.replace('from alert_scanner import alert_scanner', '# Alert scanner moved to alert_worker.py')

# Remove initialization
bot_content = re.sub(
    r'alert_scanner = AlertScanner\(application\).*\n.*alert_scanner\.start\(\)',
    '# Alert scanning handled by separate alert_worker.py process',
    bot_content,
    flags=re.DOTALL
)

# Add alert queue import
if 'from alert_queue import alert_queue' not in bot_content:
    # Add after other imports
    import_section = bot_content.find('from database import db')
    if import_section != -1:
        bot_content = bot_content[:import_section] + 'from alert_queue import alert_queue\n' + bot_content[import_section:]

# Add alert sender loop
alert_sender_code = '''
# ==========================================
# ALERT SENDER - Check queue and send alerts
# ==========================================

async def alert_sender_loop(application):
    """Check alert queue and send pending alerts to users"""
    logger.info("🔔 Alert Sender started")
    
    while True:
        try:
            # Get pending alerts from queue
            pending_alerts = alert_queue.get_pending_alerts(limit=10)
            
            if pending_alerts:
                logger.info(f"📬 Processing {len(pending_alerts)} pending alerts")
                
                for filepath, alert_data in pending_alerts:
                    try:
                        # Mark as processing
                        processing_path = alert_queue.mark_alert_processing(filepath)
                        
                        # Send alert
                        user_id = alert_data['user_id']
                        message = alert_data['alert_data']['message']
                        
                        await application.bot.send_message(
                            chat_id=user_id,
                            text=message,
                            parse_mode='HTML'
                        )
                        
                        # Mark as completed
                        alert_queue.mark_alert_completed(processing_path, success=True)
                        logger.info(f"✅ Alert sent to user {user_id}")
                        
                    except Exception as e:
                        logger.error(f"Failed to send alert: {e}")
                        # Leave in processing to retry later
                        continue
            
            # Check every 5 seconds
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"Alert sender error: {e}")
            await asyncio.sleep(10)

'''

# Add alert sender before main()
main_func_pos = bot_content.find('def main():')
if main_func_pos != -1:
    bot_content = bot_content[:main_func_pos] + alert_sender_code + '\n' + bot_content[main_func_pos:]

# Start alert sender in main()
if 'asyncio.create_task(alert_sender_loop(application))' not in bot_content:
    # Find application.run_polling()
    run_polling_pos = bot_content.find('application.run_polling(')
    if run_polling_pos != -1:
        # Add before run_polling
        indent = '    '
        insert_code = f'\n{indent}# Start alert sender loop\n{indent}asyncio.create_task(alert_sender_loop(application))\n{indent}\n'
        bot_content = bot_content[:run_polling_pos] + insert_code + bot_content[run_polling_pos:]

with open('bot.py', 'w') as f:
    f.write(bot_content)

print("✅ bot.py updated - alert_scanner removed, alert_sender added")

# 2. Update handlers.py - notify worker when settings change
with open('handlers.py', 'r') as f:
    handlers_content = f.read()

print("\n2️⃣ Updating handlers.py to notify worker on settings changes...")

# Find alert settings save functions
# Add alert_queue import if not present
if 'from alert_queue import alert_queue' not in handlers_content:
    handlers_content = 'from alert_queue import alert_queue\n' + handlers_content

# Find where alert settings are saved and add notification
# Look for db.update_user in alert settings context
save_settings_pattern = r'(user\[\'alert_settings\'\] = .*\n.*db\.update_user\(user_id, user\))'

def add_notification(match):
    original = match.group(1)
    return original + '\n        # Notify worker about settings change\n        alert_queue.add_settings_update(user_id, user[\'alert_settings\'])'

handlers_content = re.sub(save_settings_pattern, add_notification, handlers_content)

with open('handlers.py', 'w') as f:
    f.write(handlers_content)

print("✅ handlers.py updated - worker notifications added")

print("\n" + "=" * 60)
print("✅ STEP 3 COMPLETE!")
print("=" * 60)

