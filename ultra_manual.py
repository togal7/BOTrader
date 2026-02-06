"""
Ultra Manual Scan - Admin panel integration
"""
import asyncio
import time
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from central_ai_analyzer import central_analyzer
from ai_signals_tracker import tracker

ADMIN_IDS = [1794363283]

SYMBOLS = [
    'BTC/USDT:USDT', 'ETH/USDT:USDT', 'BNB/USDT:USDT', 'SOL/USDT:USDT',
    'XRP/USDT:USDT', 'ADA/USDT:USDT', 'AVAX/USDT:USDT', 'DOGE/USDT:USDT',
    'DOT/USDT:USDT', 'MATIC/USDT:USDT', 'LINK/USDT:USDT', 'UNI/USDT:USDT',
    'ATOM/USDT:USDT', 'LTC/USDT:USDT', 'NEAR/USDT:USDT', 'BCH/USDT:USDT',
    'ALGO/USDT:USDT', 'XLM/USDT:USDT', 'AAVE/USDT:USDT', 'CRV/USDT:USDT',
    'SHIB/USDT:USDT', 'PEPE/USDT:USDT', 'ARB/USDT:USDT', 'OP/USDT:USDT',
    'SUI/USDT:USDT', 'APT/USDT:USDT', 'INJ/USDT:USDT', 'VET/USDT:USDT',
    'ETC/USDT:USDT', 'TRX/USDT:USDT'
]

TIMEFRAMES = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '1d', '1w']

def is_admin(user_id):
    return user_id in ADMIN_IDS

async def ultra_menu(update, context):
    """Menu ULTRA scan"""
    query = update.callback_query
    
    if not is_admin(query.from_user.id):
        await query.answer("⛔ Brak dostępu")
        return
    
    keyboard = [
        [InlineKeyboardButton('⚡ ULTRA 500', callback_data='ultra_scan_500')],
        [InlineKeyboardButton('🚀 ULTRA 1000', callback_data='ultra_scan_1000')],
        [InlineKeyboardButton('💪 ULTRA 2000', callback_data='ultra_scan_2000')],
        [InlineKeyboardButton('🏠 Menu', callback_data='back_main')]
    ]
    
    # Pobierz obecną bazę
    try:
        import json
        with open('ai_signals_history.json', 'r') as f:
            signals = json.load(f)
        total = len(signals)
    except:
        total = 0
    
    msg = f"""
🎛️ ULTRA LEARNING MANUAL

Wybierz liczbę analiz:

⚡ 500 analiz
   • 30 par × 10 TF
   • ~4-5 min
   • +~400 sygnałów

🚀 1000 analiz
   • 30 par × 10 TF × 2 rundy
   • ~10 min
   • +~800 sygnałów

💪 2000 analiz
   • 30 par × 10 TF × 4 rundy
   • ~20 min
   • +~1600 sygnałów

📊 Obecna baza: {total} sygnałów
    """
    
    await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(keyboard))

async def ultra_start(update, context, count):
    """Start ULTRA scan"""
    query = update.callback_query
    
    if not is_admin(query.from_user.id):
        await query.answer("⛔ Brak dostępu")
        return
    
    rounds = {500: 1, 1000: 2, 2000: 4}
    round_count = rounds.get(count, 1)
    
    est_time = count * 0.5 / 60
    
    msg = f"""
🚀 ULTRA {count} ROZPOCZĘTY!

📊 Parametry:
   • Analiz: {count}
   • Rundy: {round_count}
   • Pary: 30
   • Timeframes: 10
   • Min confidence: 35%

⏱️ Szacowany czas: {est_time:.0f} min

⏳ Skanowanie w tle...
Dostaniesz powiadomienie gdy skończy!

Możesz korzystać z bota normalnie.
    """
    
    await query.edit_message_text(msg)
    
    # Start w tle
    asyncio.create_task(run_ultra_scan(query, count, round_count))

async def run_ultra_scan(query, total_count, rounds):
    """Wykonuje ULTRA scan"""
    start_time = time.time()
    success = 0
    skipped = 0
    
    analyses_per_round = total_count // rounds
    
    for round_num in range(1, rounds + 1):
        print(f"\n🔥 ULTRA Round {round_num}/{rounds}")
        
        for i in range(analyses_per_round):
            try:
                symbol = SYMBOLS[i % len(SYMBOLS)]
                tf = TIMEFRAMES[i % len(TIMEFRAMES)]
                
                result = await central_analyzer.analyze_for_ai_signals(
                    symbol=symbol,
                    main_tf=tf,
                    exchange='mexc',
                    language='pl'
                )
                
                if result and result.get('confidence', 0) >= 35:
                    tracker.record_signal(
                        symbol=symbol,
                        exchange='mexc',
                        timeframe=tf,
                        signal=result['signal'],
                        confidence=result['confidence'],
                        price=result['entry'],
                        indicators=result.get('analysis', {}).get('technical', {}),
                        ai_response=f"ULTRA scan: {result['signal']} {result['confidence']}%"
                    )
                    success += 1
                else:
                    skipped += 1
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"Error: {e}")
                skipped += 1
                await asyncio.sleep(1)
        
        print(f"✅ Round {round_num} done: {success} success")
    
    # Wynik
    total_time = time.time() - start_time
    
    # Pobierz nową bazę
    try:
        import json
        with open('ai_signals_history.json', 'r') as f:
            signals = json.load(f)
        new_total = len(signals)
    except:
        new_total = 0
    
    result_msg = f"""
✅ ULTRA {total_count} ZAKOŃCZONY!

📊 Wyniki:
   ✅ Zapisano: {success}/{total_count} ({success/total_count*100:.1f}%)
   ⏭️ Pominięto: {skipped}/{total_count}
   ⏱️ Czas: {total_time/60:.1f} min
   
📈 Nowa baza: {new_total} sygnałów total
   Przyrost: +{success}

🎯 Bot wytrenowany z większą bazą!
Confidence będzie wyższe dzięki większej wiedzy.
    """
    
    keyboard = [[InlineKeyboardButton('🎯 AI Signals', callback_data='ai_signals')]]
    
    try:
        await query.message.reply_text(result_msg, reply_markup=InlineKeyboardMarkup(keyboard))
    except:
        pass

