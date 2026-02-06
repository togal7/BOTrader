from datetime import datetime
from config import USDT_TRON_ADDRESS

def format_price(price: float) -> str:
    """Formatuje cenę"""
    if price >= 1000:
        return f"{price:,.2f}"
    elif price >= 1:
        return f"{price:.4f}"
    else:
        return f"{price:.8f}"

def format_percent(value: float) -> str:
    """Formatuje procent"""
    emoji = "🟢" if value > 0 else "🔴" if value < 0 else "⚪"
    return f"{emoji} {value:+.2f}%"

def format_subscription_status(end_date: str, is_blocked: bool) -> str:
    """Formatuje status subskrypcji"""
    if is_blocked:
        return "❌ ZABLOKOWANY"
    
    end = datetime.fromisoformat(end_date)
    now = datetime.now()
    
    if end < now:
        return "⏰ WYGASŁA"
    
    days_left = (end - now).days
    
    if days_left == 0:
        return "⚠️ WYGASA DZIŚ"
    elif days_left < 3:
        return f"⚠️ Zostało {days_left} dni"
    else:
        return f"✅ Aktywna ({days_left} dni)"

def build_payment_instructions() -> str:
    """Instrukcja płatności"""
    return f"""💳 INSTRUKCJA PŁATNOŚCI

1️⃣ Wyślij 10 USDT (TRC20) na adres:
{USDT_TRON_ADDRESS}

2️⃣ Po wysłaniu, wyślij botowi:
- Hash transakcji (TxID)
- Screenshot z portfela

3️⃣ Admin aktywuje subskrypcję w ciągu 24h

⚠️ WAŻNE:
- Tylko sieć TRON (TRC20)
- Dokładnie 10 USDT
- Nie wysyłaj innych tokenów"""

def format_signal_message(symbol: str, ai_result: dict, price: float, change: float) -> str:
    """Formatuje wiadomość z sygnałem - ULEPSZONA WERSJA"""
    from datetime import datetime
    
    # Pobierz dane
    signal = ai_result.get('signal', {})
    if isinstance(signal, dict):
        direction = signal.get('direction', 'NEUTRAL')
    else:
        direction = signal
    
    confidence = ai_result.get('confidence', 0)
    entry = ai_result.get('entry', price)
    tp1 = ai_result.get('tp1', 0)
    tp2 = ai_result.get('tp2', 0) 
    tp3 = ai_result.get('tp3', 0)
    sl = ai_result.get('sl', 0)
    rr = ai_result.get('rr_ratio', 0)
    reasons = ai_result.get('reasons', [])
    
    # Emoji
    emoji = {'LONG': '🚀', 'SHORT': '📉', 'NEUTRAL': '⚪'}.get(direction, '❓')
    
    # Format ceny
    def f(p):
        if p > 100:
            return f"${p:.2f}"
        elif p > 1:
            return f"${p:.4f}"
        else:
            return f"${p:.6f}"
    
    # Procent
    def p(a, b):
        return ((b-a)/a*100) if a != 0 else 0
    
    # Buduj wiadomość
    msg = f"""{emoji} SYGNAŁ AI - {symbol.replace('/USDT:USDT', '').replace(':USDT', '')}

🎯 {direction} | Pewność: {confidence}%

💰 Wejście: {f(entry)}
📊 24h: {change:+.2f}%

🎯 Take Profit:
  TP1: {f(tp1)} ({p(entry,tp1):+.1f}%)
  TP2: {f(tp2)} ({p(entry,tp2):+.1f}%)
  TP3: {f(tp3)} ({p(entry,tp3):+.1f}%)

🛡 Stop Loss: {f(sl)} ({p(entry,sl):+.1f}%)
📊 R/R: {rr:.1f}x

🕐 {datetime.now().strftime('%H:%M:%S')}"""
    
    # Dodaj powody jeśli są
    if reasons and len(reasons) > 0:
        msg += "\n\n💡 Analiza:\n"
        for r in reasons[:3]:
            msg += f"• {r}\n"
    
    msg += "\n⚠️ To nie jest porada finansowa. DYOR."
    
    return msg

