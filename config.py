import os
import logging

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ENV Variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '8074179703:AAHx9eNkbukuVwZvTdVZcj07CAgpZlHRigg')
ADMIN_ID = int(os.getenv('ADMIN_ID', '5157140630'))
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY', 'sk-4209e2bcd0eb49b28025890b26939423')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY', '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')

# Płatności
USDT_TRON_ADDRESS = "TLtQka56LGBdp6jse9dFcBi2oWEvfHMe4S"

# Subskrypcje
FREE_TRIAL_DAYS = 7
SUBSCRIPTION_PRICE = 10  # USDT
SUBSCRIPTION_DAYS = 30

# Giełdy
EXCHANGES = {
    'mexc': {
        'name': 'MEXC Futures',
        'base_url': 'https://contract.mexc.com',
        'enabled': True
    },
    'bybit': {
        'name': 'Bybit',
        'base_url': 'https://api.bybit.com',
        'enabled': True
    },
    'binance': {
        'name': 'Binance Futures',
        'base_url': 'https://fapi.binance.com',
        'enabled': True
    }
}

# Interwały
INTERVALS = {
    '1m': '1 minuta',
    '3m': '3 minuty',
    '5m': '5 minut',
    '15m': '15 minut',
    '30m': '30 minut',
    '1h': '1 godzina',
    '2h': '2 godziny',
    '4h': '4 godziny',
    '6h': '6 godzin',
    '12h': '12 godzin',
    '1d': '1 dzień',
    '3d': '3 dni',
    '1w': '1 tydzień',
    '1M': '1 miesiąc'
}

# Admin IDs (lista)
ADMIN_IDS = [5157140630]

# Timeframes
TIMEFRAMES = {
    '1m': {'label': '1 minuta'},
    '5m': {'label': '5 minut'},
    '15m': {'label': '15 minut'},
    '30m': {'label': '30 minut'},
    '1h': {'label': '1 godzina'},
    '4h': {'label': '4 godziny'},
    '8h': {'label': '8 godzin'},
    '1d': {'label': '1 dzień'},
    '1w': {'label': '1 tydzień'},
    '1M': {'label': '1 miesiąc'}
}

# USDT Address (TRC20)
USDT_ADDRESS = "TLtQka56LGBdp6jse9dFcBi2oWEvfHMe4S"

logger.info("✅ Config complete")
