"""
Admin Panel dla BOTrader
Dodaje przyciski do ręcznego skanowania w Telegram
"""

# Admin user IDs (dodaj swoje Telegram ID)
ADMIN_IDS = [1794363283]  # Twoje ID

def is_admin(user_id):
    return user_id in ADMIN_IDS

# Callback dla admin menu
async def admin_menu(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    
    if not is_admin(user_id):
        await query.answer("⛔ Brak dostępu")
        return
    
    keyboard = [
        [InlineKeyboardButton('⚡ Quick Scan (1h TOP10)', callback_data='admin_scan_quick')],
        [InlineKeyboardButton('🚀 Medium Scan (1h+4h TOP20)', callback_data='admin_scan_medium')],
        [InlineKeyboardButton('💪 Full Scan (All TF TOP30)', callback_data='admin_scan_full')],
        [InlineKeyboardButton('⚙️ Custom Scan', callback_data='admin_scan_custom')],
        [InlineKeyboardButton('🏠 Menu główne', callback_data='back_main')]
    ]
    
    msg = """
🎛️ PANEL ADMINA

Wybierz tryb skanowania:

⚡ Quick: 1h × TOP10 (~2 min)
🚀 Medium: 1h+4h × TOP20 (~8 min)
💪 Full: Wszystkie TF × TOP30 (~45 min)
⚙️ Custom: Wybierz parametry

📊 Obecna baza: {total} sygnałów
    """.format(total=len(tracker.signals_db))
    
    await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))


import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from central_ai_analyzer import central_analyzer
from ai_signals_tracker import tracker
import time

SYMBOLS_TOP10 = [
    'BTC/USDT:USDT', 'ETH/USDT:USDT', 'BNB/USDT:USDT', 'SOL/USDT:USDT',
    'XRP/USDT:USDT', 'ADA/USDT:USDT', 'AVAX/USDT:USDT', 'DOGE/USDT:USDT',
    'DOT/USDT:USDT', 'MATIC/USDT:USDT'
]

SYMBOLS_TOP20 = SYMBOLS_TOP10 + [
    'LINK/USDT:USDT', 'UNI/USDT:USDT', 'ATOM/USDT:USDT', 'LTC/USDT:USDT',
    'NEAR/USDT:USDT', 'FTM/USDT:USDT', 'ALGO/USDT:USDT', 'XLM/USDT:USDT',
    'AAVE/USDT:USDT', 'CRV/USDT:USDT'
]

SYMBOLS_TOP30 = SYMBOLS_TOP20 + [
    'SHIB/USDT:USDT', 'PEPE/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT',
    'SUI/USDT:USDT', 'APT/USDT:USDT', 'INJ/USDT:USDT', 'TIA/USDT:USDT',
    'FIL/USDT:USDT', 'SAND/USDT:USDT'
]

async def admin_start_scan(update, context, scan_type):
    query = update.callback_query
    
    if not is_admin(query.from_user.id):
        await query.answer("⛔ Brak dostępu")
        return
    
    # Config dla różnych typów
    configs = {
        'quick': {
            'timeframes': ['1h'],
            'symbols': SYMBOLS_TOP10,
            'min_conf': 40,
            'name': 'Quick Scan'
        },
        'medium': {
            'timeframes': ['1h', '4h'],
            'symbols': SYMBOLS_TOP20,
            'min_conf': 40,
            'name': 'Medium Scan'
        },
        'full': {
            'timeframes': ['15m', '30m', '1h', '4h', '1d'],
            'symbols': SYMBOLS_TOP30,
            'min_conf': 35,
            'name': 'Full Scan'
        }
    }
    
    if scan_type not in configs:
        await query.answer("❌ Nieznany typ")
        return
    
    config = configs[scan_type]
    total = len(config['timeframes']) * len(config['symbols'])
    est_time = total * 0.5 / 60
    
    msg = f"""
🚀 {config['name']}

📊 Parametry:
  • Interwały: {', '.join(config['timeframes'])}
  • Pary: {len(config['symbols'])}
  • Min confidence: {config['min_conf']}%
  • Total analiz: {total}
  • Szacowany czas: {est_time:.1f} min

⏳ Skanowanie rozpoczęte...
Powiadomię Cię gdy skończy!
    """
    
    await query.edit_message_text(msg)
    
    # Start skanowania w tle
    asyncio.create_task(run_scan(query, config))

async def run_scan(query, config):
    """Uruchamia skanowanie w tle"""
    start_time = time.time()
    success = 0
    skipped = 0
    
    for tf in config['timeframes']:
        for symbol in config['symbols']:
            try:
                result = await central_analyzer.analyze_for_ai_signals(
                    symbol=symbol,
                    main_tf=tf,
                    exchange='mexc',
                    language='pl'
                )
                
                if result and result.get('confidence', 0) >= config['min_conf']:
                    tracker.record_signal(
                        symbol=symbol,
                        exchange='mexc',
                        timeframe=tf,
                        signal=result['signal'],
                        confidence=result['confidence'],
                        price=result['entry'],
                        indicators=result.get('analysis', {}).get('technical', {}),
                        ai_response=f"Admin scan: {result['signal']} {result['confidence']}%"
                    )
                    success += 1
                else:
                    skipped += 1
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                skipped += 1
                await asyncio.sleep(1)
    
    # Wyślij wynik
    total_time = time.time() - start_time
    total = success + skipped
    
    result_msg = f"""
✅ {config['name']} ZAKOŃCZONY!

📊 Wyniki:
  ✅ Zapisano: {success}/{total} ({success/total*100:.1f}%)
  ⏭️ Pominięto: {skipped}/{total}
  ⏱️ Czas: {total_time/60:.1f} min
  
📈 Nowa baza: {len(tracker.signals_db)} sygnałów total

Kliknij AI Signals aby zobaczyć nowe sygnały!
    """
    
    keyboard = [[InlineKeyboardButton('🎯 AI Signals', callback_data='ai_signals')]]
    
    await query.message.reply_text(result_msg, reply_markup=InlineKeyboardMarkup(keyboard))

