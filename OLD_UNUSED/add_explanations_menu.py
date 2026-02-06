"""
Add explanations menu for signal confidence
"""

with open('handlers.py', 'r') as f:
    content = f.read()

print("=== ADDING EXPLANATIONS MENU ===\n")

# 1. Dodaj menu główne wyjaśnień
explanations_menu_code = '''
async def explanations_menu(query, user_id, user):
    """Main explanations menu"""
    text = """ℹ️ WYJAŚNIENIA

Dowiedz się jak działa BOTrader:

📊 Sygnały i Analiza
📈 Wskaźniki Techniczne
🎯 Alerty i Powiadomienia
⚙️ Ustawienia"""

    keyboard = [
        [InlineKeyboardButton("📊 Sygnały i Analiza", callback_data='explain_signals')],
        [InlineKeyboardButton("📈 Wskaźniki Techniczne", callback_data='explain_indicators')],
        [InlineKeyboardButton("🎯 Alerty", callback_data='explain_alerts')],
        [InlineKeyboardButton("⚙️ Ustawienia", callback_data='explain_settings')],
        [InlineKeyboardButton('⬅️ Menu Główne', callback_data='back_main')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def explain_signals(query, user_id, user):
    """Explain signal confidence"""
    text = """📊 SYGNAŁY I PEWNOŚĆ

🎯 JAK LICZONA JEST PEWNOŚĆ?

Pewność sygnału (0-100%) bazuje na:

1️⃣ RSI (30%):
   • Oversold (<30) → BUY
   • Overbought (>70) → SELL
   • Im bardziej ekstremalne, tym wyższa pewność

2️⃣ EMA Cross (25%):
   • Szybka EMA > Wolna → BUY
   • Szybka EMA < Wolna → SELL
   • Świeży cross = wyższa pewność

3️⃣ MACD (25%):
   • MACD > Signal → BUY
   • MACD < Signal → SELL
   • Silny cross = wyższa pewność

4️⃣ Volume (20%):
   • Wysoki wolumen potwierdza sygnał
   • Volume > średnia = bonus

📈 POZIOMY CONFIDENCE:

• 90-100% = Bardzo silny sygnał 💎
• 80-89% = Silny sygnał ⭐
• 70-79% = Dobry sygnał ✅
• 60-69% = Średni sygnał ⚠️
• <60% = Słaby sygnał ❌

💡 WSKAZÓWKA:
Najlepsze sygnały to 80%+ z potwierdzeniem
na kilku interwałach (15m, 1h, 4h)."""

    keyboard = [
        [InlineKeyboardButton('📈 Wskaźniki szczegółowo', callback_data='explain_indicators')],
        [InlineKeyboardButton('⬅️ Wyjaśnienia', callback_data='explanations_menu')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def explain_indicators(query, user_id, user):
    """Explain technical indicators"""
    text = """📈 WSKAŹNIKI TECHNICZNE

🔍 CO ANALIZUJEMY?

📊 RSI (Relative Strength Index):
• Zakres: 0-100
• <30 = Oversold (wyprzedanie)
• >70 = Overbought (wykupienie)
• Najlepsze sygnały przy ekstremach

📉 EMA (Exponential Moving Average):
• Krótka (9) i długa (21)
• Cross = zmiana trendu
• Golden Cross = silny BUY
• Death Cross = silny SELL

🌊 MACD (Moving Average Convergence):
• Momentum indicator
• Cross linii = zmiana kierunku
• Histogram = siła trendu

📊 Volume (Wolumen):
• Potwierdza ruchy cenowe
• Wysoki volume = silny sygnał
• Niski volume = słaby ruch

💰 Bollinger Bands:
• Zmienność ceny
• Dotknięcie dolnej = oversold
• Dotknięcie górnej = overbought

🎯 AI Deep Analysis:
• DeepSeek AI analizuje wszystkie dane
• Wykrywa wzorce i struktury
• Dodaje kontekst rynkowy"""

    keyboard = [
        [InlineKeyboardButton('🎯 Jak używać alertów?', callback_data='explain_alerts')],
        [InlineKeyboardButton('⬅️ Wyjaśnienia', callback_data='explanations_menu')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def explain_alerts(query, user_id, user):
    """Explain alerts system"""
    text = """🎯 SYSTEM ALERTÓW

🔔 RODZAJE ALERTÓW:

1️⃣ RSI Extremes:
   • Oversold (<30) - potencjalny BUY
   • Overbought (>70) - potencjalny SELL

2️⃣ Duże Wzrosty/Spadki:
   • Próg domyślny: ±15%
   • Dostosuj w ustawieniach

3️⃣ Nagłe Zmiany:
   • Profile: 5%, 10%, 15%, 20%, 25%
   • Im niższy, tym więcej alertów

4️⃣ Sygnały AI:
   • Min. confidence: 70%
   • Najlepsze okazje

⚙️ USTAWIENIA:

📊 Częstotliwość skanowania:
   • 5 min - bardzo czułe
   • 15 min - balans ⭐
   • 30 min - spokojniejsze

🎯 Zakres skanowania:
   • Top 50 - szybkie
   • Top 100 - balans ⭐
   • Top 200 - pełne

💡 WSKAZÓWKI:

✅ Włącz 2-3 typy alertów
✅ Dostosuj progi do stylu tradingu
✅ Sprawdzaj alerty na telefonie
❌ Nie włączaj wszystkiego naraz"""

    keyboard = [
        [InlineKeyboardButton('⚙️ Idź do ustawień', callback_data='alerts_settings')],
        [InlineKeyboardButton('⬅️ Wyjaśnienia', callback_data='explanations_menu')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def explain_settings(query, user_id, user):
    """Explain settings"""
    text = """⚙️ USTAWIENIA BOTA

🌍 JĘZYK:
• Polski, English, Español i więcej
• Zmień w: Ustawienia → Język

⏱️ INTERWAŁ DOMYŚLNY:
• Preferowany timeframe dla analiz
• Np. 15m dla day trading
• 4h dla swing trading

📊 GIEŁDA:
• MEXC Futures (domyślnie)
• Najwięcej par do wyboru

🔔 ALERTY:
• Włącz/wyłącz każdy typ osobno
• Dostosuj progi i częstotliwość
• Historia ostatnich alertów

💎 PREMIUM:
• Bez limitów skanowania
• Wszystkie funkcje AI
• Priorytetowe alerty"""

    keyboard = [
        [InlineKeyboardButton('⚙️ Otwórz ustawienia', callback_data='settings')],
        [InlineKeyboardButton('⬅️ Wyjaśnienia', callback_data='explanations_menu')]
    ]
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
'''

# Dodaj na końcu handlers.py
content = content.rstrip() + '\n\n' + explanations_menu_code + '\n'

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ Added explanations menu functions")

