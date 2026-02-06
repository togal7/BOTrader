with open('bot.py', 'r') as f:
    content = f.read()

print("=== ADDING MESSAGE HANDLER ===\n")

# Dodaj import MessageHandler i filters
old_import = "from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes"
new_import = "from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes"

content = content.replace(old_import, new_import)
print("✅ Updated imports")

# Dodaj MessageHandler PRZED CallbackQueryHandler
old_handlers = """    # Callback queries
    application.add_handler(CallbackQueryHandler(button_callback))"""

new_handlers = """    # Message handler (for text search)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Callback queries
    application.add_handler(CallbackQueryHandler(button_callback))"""

content = content.replace(old_handlers, new_handlers)
print("✅ Added MessageHandler")

with open('bot.py', 'w') as f:
    f.write(content)

