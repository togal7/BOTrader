#!/usr/bin/env python3
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import logger, TELEGRAM_BOT_TOKEN
from handlers import *
# Alert scanner moved to alert_worker.py
from exchanges import exchange_api

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Obsługa błędów"""
    logger.error(f"Exception: {context.error}", exc_info=context.error)

async def shutdown(application: Application):
    """Zamykanie zasobów"""
    logger.info("Zamykanie bota...")
    await exchange_api.close()


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



async def post_init(application):
    """Called after bot starts - safe place for background tasks"""
    logger.info("🔔 Starting alert sender loop...")

def main():
    """Główna funkcja bota"""
    logger.info("🚀 Uruchamianie BOTrader Bot...")
    
    # Aplikacja
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Initialize Alert Scanner
    # Alert Scanner now runs as separate process (alert_worker.py)
    
    # Handlery komend
    application.add_handler(CommandHandler("start", start_command))

    # Admin commands
    
    
    
    # Message handler (for text search)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message), group=1)
    
    # Callback queries
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Error handler
    application.add_error_handler(error_handler)
    
    # Shutdown
    application.post_shutdown = shutdown
    
    # Start polling
    logger.info("✅ Bot uruchomiony!")

    # Start alert scanner in background
    # Register post_init callback

    
    # Start alert sender loop
    # Alert sender will be started via post_init hook

    # Start bot
    logger.info("🚀 Starting polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    

if __name__ == "__main__":
    main()



    # ========================================================================
    # PORTFOLIO MESSAGE HANDLER - HIGHEST PRIORITY (group=0)
    # ========================================================================
    
    async def handle_portfolio_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all Portfolio state messages - PRIORITY HANDLER"""
        user_id = update.message.from_user.id
        user = db.get_user(user_id)
        state = user.get('state', '')
        
        # Only handle Portfolio states
        if not state.startswith('portfolio_'):
            return  # Let other handlers take it
        
        # Import Portfolio handlers
        from handlers import (
            handle_portfolio_add_symbol,
            handle_portfolio_add_entry,
            handle_portfolio_add_size,
            handle_portfolio_add_targets
        )
        
        # Route to appropriate handler
        if state == 'portfolio_add_symbol':
            await handle_portfolio_add_symbol(update.message, user_id, user)
        elif state == 'portfolio_add_entry':
            await handle_portfolio_add_entry(update.message, user_id, user)
        elif state == 'portfolio_add_size':
            await handle_portfolio_add_size(update.message, user_id, user)
        elif state == 'portfolio_add_targets':
            await handle_portfolio_add_targets(update.message, user_id, user)
    
    # Add Portfolio handler with GROUP 0 (before search which is group 1 or default)
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND & filters.ChatType.PRIVATE, handle_portfolio_messages),
        group=0
    )
    

    # ========================================================================
    # PORTFOLIO - ConversationHandler (HIGHEST PRIORITY)
    # ========================================================================
    
    from telegram.ext import ConversationHandler
    from handlers import (
        portfolio_add_start,
        handle_portfolio_add_symbol,
        handle_portfolio_add_entry,
        handle_portfolio_add_size,
        handle_portfolio_add_targets,
        handle_portfolio_type,
        handle_portfolio_leverage,
        finish_portfolio_add
    )
    
    # States
    PORTFOLIO_SYMBOL, PORTFOLIO_TYPE, PORTFOLIO_ENTRY, PORTFOLIO_SIZE, PORTFOLIO_LEVERAGE, PORTFOLIO_TARGETS = range(6)
    
    async def portfolio_symbol_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle symbol input - auto-complete BTC -> BTC/USDT:USDT"""
        user_id = update.message.from_user.id
        user = db.get_user(user_id)
        symbol = update.message.text.upper().strip()
        
        # Auto-complete
        if '/' not in symbol and ':' not in symbol:
            symbol = f"{symbol}/USDT:USDT"
        elif '/' in symbol and ':' not in symbol:
            symbol = f"{symbol}:USDT"
        
        # Save symbol
        if 'portfolio_new' not in user:
            user['portfolio_new'] = {}
        user['portfolio_new']['symbol'] = symbol
        db.save_user(user_id, user)
        
        # Show type selection
        text = f"""➕ ADD POSITION: {symbol}

📝 Step 2/6: Position type"""
        
        keyboard = [
            [InlineKeyboardButton('🚀 LONG', callback_data='portfolio_type_LONG')],
            [InlineKeyboardButton('📉 SHORT', callback_data='portfolio_type_SHORT')],
            [InlineKeyboardButton('❌ Cancel', callback_data='portfolio_cancel')]
        ]
        
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        return PORTFOLIO_TYPE
    
    async def portfolio_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel conversation"""
        query = update.callback_query if update.callback_query else None
        
        text = "❌ Cancelled. Portfolio add cancelled."
        keyboard = [[InlineKeyboardButton('⬅️ Back to Portfolio', callback_data='portfolio_main')]]
        
        if query:
            await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
        
        return ConversationHandler.END
    
    # Build ConversationHandler
    portfolio_conv = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(portfolio_add_start, pattern='^portfolio_add_start$')
        ],
        states={
            PORTFOLIO_SYMBOL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, portfolio_symbol_handler)
            ],
            # Other states handled by existing callbacks
        },
        fallbacks=[
            CallbackQueryHandler(portfolio_cancel, pattern='^portfolio_cancel$'),
            CommandHandler('cancel', portfolio_cancel)
        ],
        name="portfolio_conversation",
        persistent=False
    )
    
    # Add ConversationHandler with HIGHEST priority (group=-2)
    application.add_handler(portfolio_conv, group=-2)
    
