with open('bot.py', 'r') as f:
    content = f.read()

# Sprawdź czy alert_sender_loop istnieje
if 'async def alert_sender_loop' not in content:
    print("❌ alert_sender_loop NOT FOUND - adding it!")
    
    # Dodaj PRZED def main()
    sender_code = '''
async def alert_sender_loop(application):
    """Check alert queue and send pending alerts to users"""
    logger.info("🔔 Alert Sender Loop starting...")
    
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
                            text=message
                        )
                        
                        # Mark as completed
                        alert_queue.mark_alert_completed(processing_path, success=True)
                        logger.info(f"✅ Alert sent to user {user_id}")
                        
                    except Exception as e:
                        logger.error(f"Failed to send alert: {e}")
                        continue
            
            # Check every 5 seconds
            await asyncio.sleep(5)
            
        except Exception as e:
            logger.error(f"Alert sender error: {e}")
            await asyncio.sleep(10)

'''
    
    main_pos = content.find('def main():')
    if main_pos != -1:
        content = content[:main_pos] + sender_code + content[main_pos:]
        print("✅ alert_sender_loop added")
else:
    print("✅ alert_sender_loop already exists")

# Dodaj startup hook
if 'application.post_init' not in content:
    print("Adding post_init hook...")
    
    # Znajdź application.run_polling i dodaj PRZED nim
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        if 'application.run_polling' in line:
            # Dodaj hook przed run_polling
            indent = '    '
            new_lines.append(f'{indent}# Start alert sender background task')
            new_lines.append(f'{indent}async def start_alert_sender(app):')
            new_lines.append(f'{indent}    import asyncio')
            new_lines.append(f'{indent}    asyncio.create_task(alert_sender_loop(app))')
            new_lines.append(f'{indent}    logger.info("🔔 Alert Sender started")')
            new_lines.append(f'{indent}')
            new_lines.append(f'{indent}application.post_init = start_alert_sender')
            new_lines.append(f'{indent}')
        
        new_lines.append(line)
    
    content = '\n'.join(new_lines)
    print("✅ post_init hook added")

with open('bot.py', 'w') as f:
    f.write(content)

print("\n✅ DONE!")

