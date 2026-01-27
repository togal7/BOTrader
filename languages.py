#!/usr/bin/env python3
"""
System wielojęzyczny - 10 języków
"""
from config import logger

LANGUAGES = {
    'pl': {'name': '🇵🇱 Polski', 'code': 'pl'},
    'en': {'name': '🇬🇧 English', 'code': 'en'},
    'es': {'name': '🇪🇸 Español', 'code': 'es'},
    'de': {'name': '🇩🇪 Deutsch', 'code': 'de'},
    'fr': {'name': '🇫🇷 Français', 'code': 'fr'},
    'it': {'name': '🇮🇹 Italiano', 'code': 'it'},
    'pt': {'name': '🇵🇹 Português', 'code': 'pt'},
    'ru': {'name': '🇷🇺 Русский', 'code': 'ru'},
    'tr': {'name': '🇹🇷 Türkçe', 'code': 'tr'},
    'zh': {'name': '🇨🇳 中文', 'code': 'zh'}
}

TRANSLATIONS = {
    # MENU
    'search_pair': {
        'pl': '🔍 Wyszukaj parę',
        'en': '🔍 Search Pair',
        'es': '🔍 Buscar Par',
        'de': '🔍 Paar Suchen',
        'fr': '🔍 Rechercher Paire',
        'it': '🔍 Cerca Coppia',
        'pt': '🔍 Buscar Par',
        'ru': '🔍 Найти Пару',
        'tr': '🔍 Çift Ara',
        'zh': '🔍 搜索交易对'
    },
    'scan_extremes': {
        'pl': '📊 Skaner ekstremów',
        'en': '📊 Extremes Scanner',
        'es': '📊 Escáner de Extremos',
        'de': '📊 Extremscanner',
        'fr': '📊 Scanner d\'Extrêmes',
        'it': '📊 Scanner Estremi',
        'pt': '📊 Scanner de Extremos',
        'ru': '📊 Сканер Экстремумов',
        'tr': '📊 Uç Değer Tarayıcı',
        'zh': '📊 极值扫描器'
    },
    'ai_signals': {
        'pl': '🎯 Sygnały AI',
        'en': '🎯 AI Signals',
        'es': '🎯 Señales IA',
        'de': '🎯 KI-Signale',
        'fr': '🎯 Signaux IA',
        'it': '🎯 Segnali IA',
        'pt': '🎯 Sinais IA',
        'ru': '🎯 ИИ Сигналы',
        'tr': '🎯 Yapay Zeka Sinyalleri',
        'zh': '🎯 AI信号'
    },
    'settings': {
        'pl': '⚙️ Ustawienia',
        'en': '⚙️ Settings',
        'es': '⚙️ Configuración',
        'de': '⚙️ Einstellungen',
        'fr': '⚙️ Paramètres',
        'it': '⚙️ Impostazioni',
        'pt': '⚙️ Configurações',
        'ru': '⚙️ Настройки',
        'tr': '⚙️ Ayarlar',
        'zh': '⚙️ 设置'
    },
    
    # ANALYSIS
    'signal': {
        'pl': 'SYGNAŁ',
        'en': 'SIGNAL',
        'es': 'SEÑAL',
        'de': 'SIGNAL',
        'fr': 'SIGNAL',
        'it': 'SEGNALE',
        'pt': 'SINAL',
        'ru': 'СИГНАЛ',
        'tr': 'SİNYAL',
        'zh': '信号'
    },
    'entry': {
        'pl': 'Wejście',
        'en': 'Entry',
        'es': 'Entrada',
        'de': 'Einstieg',
        'fr': 'Entrée',
        'it': 'Entrata',
        'pt': 'Entrada',
        'ru': 'Вход',
        'tr': 'Giriş',
        'zh': '入场'
    },
    
    # SIMPLE EXPLANATIONS
    'explain_rsi': {
        'pl': '📚 RSI (Relative Strength Index) - wskaźnik siły trendu. Poniżej 30 = wyprzedanie (dobry moment na kupno), powyżej 70 = wykupienie (może być korekta).',
        'en': '📚 RSI shows trend strength. Below 30 = oversold (good buy opportunity), above 70 = overbought (correction possible).',
        'es': '📚 RSI muestra fuerza de tendencia. Debajo 30 = sobrevendido (buena oportunidad), arriba 70 = sobrecomprado (corrección posible).',
        'de': '📚 RSI zeigt Trendstärke. Unter 30 = überverkauft (gute Kaufgelegenheit), über 70 = überkauft (Korrektur möglich).',
        'fr': '📚 RSI montre la force de tendance. Sous 30 = survendu (bonne opportunité), au-dessus 70 = suracheté (correction possible).',
        'it': '📚 RSI mostra forza del trend. Sotto 30 = ipervenduto (buona opportunità), sopra 70 = ipercomprato (correzione possibile).',
        'pt': '📚 RSI mostra força da tendência. Abaixo 30 = sobrevendido (boa oportunidade), acima 70 = sobrecomprado (correção possível).',
        'ru': '📚 RSI показывает силу тренда. Ниже 30 = перепроданность (хорошая возможность), выше 70 = перекупленность (возможна коррекция).',
        'tr': '📚 RSI trend gücünü gösterir. 30\'un altı = aşırı satım (iyi fırsat), 70\'in üstü = aşırı alım (düzeltme olabilir).',
        'zh': '📚 RSI显示趋势强度。低于30=超卖（买入机会），高于70=超买（可能回调）。'
    },
    'explain_ema': {
        'pl': '📚 EMA (Exponential Moving Average) - linia trendu. Gdy cena powyżej EMA = trend wzrostowy, poniżej = spadkowy.',
        'en': '📚 EMA is a trend line. Price above EMA = uptrend, below = downtrend.',
        'es': '📚 EMA es línea de tendencia. Precio arriba EMA = tendencia alcista, debajo = bajista.',
        'de': '📚 EMA ist Trendlinie. Preis über EMA = Aufwärtstrend, unter = Abwärtstrend.',
        'fr': '📚 EMA est ligne de tendance. Prix au-dessus EMA = tendance haussière, en dessous = baissière.',
        'it': '📚 EMA è linea di tendenza. Prezzo sopra EMA = trend rialzista, sotto = ribassista.',
        'pt': '📚 EMA é linha de tendência. Preço acima EMA = tendência de alta, abaixo = baixa.',
        'ru': '📚 EMA - линия тренда. Цена выше EMA = восходящий тренд, ниже = нисходящий.',
        'tr': '📚 EMA trend çizgisidir. Fiyat EMA üstünde = yükseliş trendi, altında = düşüş.',
        'zh': '📚 EMA是趋势线。价格高于EMA=上升趋势，低于=下降趋势。'
    },
    'explain_volume': {
        'pl': '📚 Wolumen - ile monet zostało kupionych/sprzedanych. Wysoki wolumen = silny ruch, niski = słaby.',
        'en': '📚 Volume - how many coins were traded. High volume = strong move, low = weak.',
        'es': '📚 Volumen - cuántas monedas se negociaron. Alto volumen = movimiento fuerte, bajo = débil.',
        'de': '📚 Volumen - wie viele Münzen gehandelt wurden. Hohes Volumen = starke Bewegung, niedriges = schwach.',
        'fr': '📚 Volume - combien de pièces échangées. Volume élevé = mouvement fort, faible = faible.',
        'it': '📚 Volume - quante monete sono state scambiate. Volume alto = movimento forte, basso = debole.',
        'pt': '📚 Volume - quantas moedas foram negociadas. Volume alto = movimento forte, baixo = fraco.',
        'ru': '📚 Объем - сколько монет торговалось. Высокий объем = сильное движение, низкий = слабое.',
        'tr': '📚 Hacim - kaç coin işlem gördü. Yüksek hacim = güçlü hareket, düşük = zayıf.',
        'zh': '📚 成交量-交易了多少币。高成交量=强劲走势，低=弱势。'
    },
    
    # DISCLAIMER
    'disclaimer': {
        'pl': """
⚠️ WAŻNE - ZASTRZEŻENIE PRAWNE:

Bot BOTrader dostarcza informacje edukacyjne i analizy techniczne oparte na algorytmach AI. To NIE JEST porada finansowa ani inwestycyjna.

Handel kryptowalutami i kontraktami futures wiąże się z wysokim ryzykiem utraty kapitału. Możesz stracić więcej niż zainwestowałeś.

• Nie gwarantujemy zysków ani trafności sygnałów
• Wszystkie decyzje handlowe podejmujesz na własną odpowiedzialność
• Zawsze przeprowadzaj własną analizę przed inwestycją
• Inwestuj tylko środki, których utratę możesz zaakceptować
• Skonsultuj się z profesjonalnym doradcą finansowym

Używając tego bota akceptujesz pełną odpowiedzialność za swoje decyzje inwestycyjne.""",
        'en': """
⚠️ IMPORTANT - LEGAL DISCLAIMER:

BOTrader bot provides educational information and AI-powered technical analysis. This is NOT financial or investment advice.

Cryptocurrency and futures trading involves high risk of capital loss. You can lose more than you invested.

• We do not guarantee profits or signal accuracy
• All trading decisions are your sole responsibility
• Always conduct your own analysis before investing
• Only invest funds you can afford to lose
• Consult with a professional financial advisor

By using this bot you accept full responsibility for your investment decisions.""",
        'es': """
⚠️ IMPORTANTE - DESCARGO DE RESPONSABILIDAD:

Bot BOTrader proporciona información educativa y análisis técnico con IA. Esto NO ES asesoramiento financiero.

El comercio de criptomonedas y futuros implica alto riesgo. Puede perder más de lo invertido.

• No garantizamos ganancias ni precisión de señales
• Todas las decisiones comerciales son su responsabilidad
• Siempre realice su propio análisis antes de invertir
• Solo invierta fondos que pueda permitirse perder
• Consulte con un asesor financiero profesional

Al usar este bot acepta toda la responsabilidad por sus decisiones.""",
        'ru': """
⚠️ ВАЖНО - ЮРИДИЧЕСКОЕ ПРЕДУПРЕЖДЕНИЕ:

Бот BOTrader предоставляет образовательную информацию и технический анализ на основе ИИ. Это НЕ финансовая консультация.

Торговля криптовалютами и фьючерсами связана с высоким риском потери капитала.

• Мы не гарантируем прибыль или точность сигналов
• Все торговые решения принимаются на ваш риск
• Всегда проводите собственный анализ перед инвестированием
• Инвестируйте только те средства, потерю которых можете позволить
• Проконсультируйтесь с профессиональным финансовым консультантом

Используя этот бот, вы принимаете полную ответственность за свои решения."""
    }
}

def t(key: str, lang: str = 'pl', **kwargs) -> str:
    """Get translation"""
    text = TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get('pl', key))
    return text.format(**kwargs) if kwargs else text

def get_user_language(user_data: dict) -> str:
    """Get user's language, default Polish"""
    return user_data.get('language', 'pl')

logger.info("✅ Language system initialized")
