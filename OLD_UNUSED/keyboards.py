from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import EXCHANGES, INTERVALS, USDT_TRON_ADDRESS

def main_menu_keyboard(is_admin=False):
    """Główne menu"""
    keyboard = [
        [InlineKeyboardButton("🔍 Wyszukaj parę", callback_data="search_pair")],
        [InlineKeyboardButton("🔥 Skaner ekstremów", callback_data="scan_extremes")],
        [InlineKeyboardButton("📊 Sygnały AI", callback_data="ai_signals")],
        [InlineKeyboardButton("⚙️ Ustawienia", callback_data="settings")],
        [InlineKeyboardButton("💳 Subskrypcja", callback_data="subscription")]
    ]
    
    if is_admin:
        keyboard.append([InlineKeyboardButton("👑 Panel Admina", callback_data="admin_panel")])
    
    return InlineKeyboardMarkup(keyboard)

def exchanges_keyboard():
    """Wybór giełdy"""
    keyboard = []
    for ex_id, ex_data in EXCHANGES.items():
        if ex_data['enabled']:
            keyboard.append([InlineKeyboardButton(
                f"📈 {ex_data['name']}", 
                callback_data=f"exchange_{ex_id}"
            )])
    
    keyboard.append([InlineKeyboardButton("◀️ Powrót", callback_data="back_main")])
    return InlineKeyboardMarkup(keyboard)

def intervals_keyboard():
    """Wybór interwału"""
    keyboard = []
    row = []
    
    for interval, label in INTERVALS.items():
        row.append(InlineKeyboardButton(interval, callback_data=f"interval_{interval}"))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    
    if row:
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("◀️ Powrót", callback_data="settings")])
    return InlineKeyboardMarkup(keyboard)

def scan_type_keyboard():
    """Typ skanowania"""
    keyboard = [
        [InlineKeyboardButton("📈 Największe wzrosty", callback_data="scan_gainers")],
        [InlineKeyboardButton("📉 Największe spadki", callback_data="scan_losers")],
        [InlineKeyboardButton("◀️ Powrót", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def signal_keyboard(symbol):
    """Akcje po sygnale"""
    keyboard = [
        [InlineKeyboardButton("🔄 Odśwież sygnał", callback_data=f"refresh_signal_{symbol}")],
        [InlineKeyboardButton("◀️ Menu główne", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def settings_keyboard():
    """Ustawienia"""
    keyboard = [
        [InlineKeyboardButton("🏦 Zmień giełdę", callback_data="change_exchange")],
        [InlineKeyboardButton("⏱ Zmień interwał", callback_data="change_interval")],
        [InlineKeyboardButton("◀️ Powrót", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def subscription_keyboard():
    """Subskrypcja"""
    keyboard = [
        [InlineKeyboardButton("💰 Przedłuż subskrypcję (10 USDT)", callback_data="extend_sub")],
        [InlineKeyboardButton("ℹ️ Instrukcja płatności", callback_data="payment_info")],
        [InlineKeyboardButton("◀️ Powrót", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_keyboard():
    """Panel admina"""
    keyboard = [
        [InlineKeyboardButton("📊 Statystyki", callback_data="admin_stats")],
        [InlineKeyboardButton("👤 Zarządzaj użytkownikami", callback_data="admin_users")],
        [InlineKeyboardButton("🎁 Dodaj dni użytkownikowi", callback_data="admin_add_days")],
        [InlineKeyboardButton("◀️ Powrót", callback_data="back_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    """Przycisk powrotu"""
    return InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Powrót", callback_data="back_main")]])
