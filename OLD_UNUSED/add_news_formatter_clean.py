"""
Add news formatter - clean version
"""

with open('handlers.py', 'r') as f:
    content = f.read()

import re

# Funkcja formatująca newsy
news_formatter = '''
def format_news_section(analysis):
    """Format news sentiment section"""
    news = analysis.get('news_sentiment')
    
    if not news:
        return "📭 Brak danych o newsach"
    
    # Fear & Greed
    fg = news.get('fear_greed')
    fg_text = ""
    if fg:
        value = fg['value']
        classification = fg['classification']
        
        if value < 20:
            emoji = "😨"
        elif value < 40:
            emoji = "😟"
        elif value < 60:
            emoji = "😐"
        elif value < 80:
            emoji = "😊"
        else:
            emoji = "🤑"
        
        fg_text = f"😱 Fear & Greed: {value}/100 {emoji} ({classification})"
    
    # News sentiment
    overall = news.get('overall_sentiment', 'neutral')
    positive_pct = news.get('positive_pct', 0)
    negative_pct = news.get('negative_pct', 0)
    news_count = news.get('news_count', 0)
    
    sentiment_emoji = {
        'positive': '✅',
        'negative': '❌',
        'neutral': '⚪'
    }
    
    news_text = f"""📊 Sentiment newsów (24h): {sentiment_emoji.get(overall, '⚪')} {overall.upper()}
   Pozytywne: {positive_pct}% | Negatywne: {negative_pct}%
   Znalezionych newsów: {news_count}"""
    
    # Top news
    top_news = news.get('top_news', [])
    news_list = ""
    if top_news:
        news_list = "\\n\\n📰 Najnowsze newsy:"
        for item in top_news[:3]:
            title = item['title'][:50] + "..." if len(item['title']) > 50 else item['title']
            sentiment = item.get('sentiment', 'neutral')
            sent_emoji = sentiment_emoji.get(sentiment, '⚪')
            news_list += f"\\n   {sent_emoji} {title}"
    
    return fg_text + "\\n" + news_text + news_list
'''

# Znajdź format_analysis_report i dodaj przed nią
pattern = r'(def format_analysis_report\()'
replacement = news_formatter + '\n\n\\1'

content = re.sub(pattern, replacement, content, count=1)

# Dodaj wywołanie w format_analysis_report
pattern = r'(text = f""".*?🎚️ Tryb:.*?\n\n)'
replacement = r'\1📰 NEWSY I SENTYMENT:\n{format_news_section(analysis)}\n\n'

if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, replacement, content, flags=re.DOTALL, count=1)
    print("✅ Added news section to report")

with open('handlers.py', 'w') as f:
    f.write(content)

print("✅ News formatter added cleanly")

