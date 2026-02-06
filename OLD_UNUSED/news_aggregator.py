"""
News Aggregator - Free sources only
Aggregates crypto news from multiple free sources
"""

import asyncio
import aiohttp
import feedparser
import logging
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json

logger = logging.getLogger(__name__)

class NewsAggregator:
    """Aggregate news from free sources"""
    
    def __init__(self):
        self.sources = {
            'rss': [
                'https://www.coindesk.com/arc/outboundfeeds/rss/',
                'https://cointelegraph.com/rss',
                'https://decrypt.co/feed',
                'https://bitcoinmagazine.com/.rss/full/',
                'https://www.theblock.co/rss.xml',
            ],
            'fear_greed': 'https://api.alternative.me/fng/',
        }
    
    async def get_fear_greed_index(self):
        """Get Fear & Greed Index (FREE, unlimited)"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.sources['fear_greed']) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        value = int(data['data'][0]['value'])
                        classification = data['data'][0]['value_classification']
                        
                        logger.info(f"Fear & Greed Index: {value} ({classification})")
                        
                        return {
                            'value': value,
                            'classification': classification,
                            'timestamp': datetime.now().isoformat()
                        }
        except Exception as e:
            logger.error(f"Fear & Greed API error: {e}")
            return None
    
    async def get_rss_news(self, hours=24):
        """Get news from RSS feeds"""
        all_news = []
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        for feed_url in self.sources['rss']:
            try:
                # Parse RSS feed
                feed = feedparser.parse(feed_url)
                source_name = feed.feed.get('title', 'Unknown')
                
                for entry in feed.entries[:10]:  # Last 10 from each
                    # Parse publish date
                    pub_date = None
                    if hasattr(entry, 'published_parsed'):
                        pub_date = datetime(*entry.published_parsed[:6])
                    
                    # Filter by time
                    if pub_date and pub_date < cutoff_time:
                        continue
                    
                    news_item = {
                        'title': entry.get('title', ''),
                        'link': entry.get('link', ''),
                        'published': pub_date.isoformat() if pub_date else None,
                        'source': source_name,
                        'summary': entry.get('summary', '')[:200]
                    }
                    
                    all_news.append(news_item)
                
                logger.info(f"Got {len([n for n in all_news if n['source'] == source_name])} news from {source_name}")
                
            except Exception as e:
                logger.error(f"RSS feed error {feed_url}: {e}")
        
        return all_news
    
    def analyze_sentiment_simple(self, text):
        """Simple keyword-based sentiment analysis"""
        positive_keywords = [
            'bullish', 'rally', 'surge', 'gain', 'profit', 'moon', 
            'adoption', 'institutional', 'breakthrough', 'partnership',
            'upgrade', 'growth', 'positive', 'buy', 'accumulate', 'strong'
        ]
        
        negative_keywords = [
            'bearish', 'crash', 'dump', 'loss', 'scam', 'hack',
            'regulation', 'ban', 'sec', 'lawsuit', 'fraud', 'bear',
            'sell', 'decline', 'drop', 'fall', 'weak', 'fud'
        ]
        
        text_lower = text.lower()
        
        positive_count = sum(1 for keyword in positive_keywords if keyword in text_lower)
        negative_count = sum(1 for keyword in negative_keywords if keyword in text_lower)
        
        if positive_count > negative_count:
            return 'positive', positive_count - negative_count
        elif negative_count > positive_count:
            return 'negative', negative_count - positive_count
        else:
            return 'neutral', 0
    
    async def get_aggregated_sentiment(self, symbol='BTC', hours=24):
        """Get aggregated sentiment for a symbol"""
        
        # 1. Get Fear & Greed
        fear_greed = await self.get_fear_greed_index()
        
        # 2. Get RSS news
        news = await self.get_rss_news(hours=hours)
        
        # 3. Filter for symbol
        symbol_keywords = {
            'BTC': ['bitcoin', 'btc'],
            'ETH': ['ethereum', 'eth'],
            'SOL': ['solana', 'sol'],
            'BNB': ['binance', 'bnb'],
        }
        
        keywords = symbol_keywords.get(symbol.upper(), [symbol.lower()])
        
        relevant_news = []
        for item in news:
            text = (item['title'] + ' ' + item.get('summary', '')).lower()
            if any(kw in text for kw in keywords):
                relevant_news.append(item)
        
        # 4. Analyze sentiment
        sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
        sentiment_scores = []
        
        for item in relevant_news:
            text = item['title'] + ' ' + item.get('summary', '')
            sentiment, score = self.analyze_sentiment_simple(text)
            sentiments[sentiment] += 1
            sentiment_scores.append(score)
            
            item['sentiment'] = sentiment
            item['sentiment_score'] = score
        
        # 5. Calculate overall sentiment
        total = len(relevant_news)
        
        if total > 0:
            positive_pct = (sentiments['positive'] / total) * 100
            negative_pct = (sentiments['negative'] / total) * 100
            
            if positive_pct > negative_pct + 20:
                overall = 'positive'
            elif negative_pct > positive_pct + 20:
                overall = 'negative'
            else:
                overall = 'neutral'
        else:
            overall = 'neutral'
            positive_pct = 0
            negative_pct = 0
        
        return {
            'symbol': symbol,
            'overall_sentiment': overall,
            'positive_pct': round(positive_pct, 1),
            'negative_pct': round(negative_pct, 1),
            'news_count': total,
            'sentiments': sentiments,
            'fear_greed': fear_greed,
            'top_news': relevant_news[:5],  # Top 5 relevant
            'timestamp': datetime.now().isoformat()
        }
    
    def calculate_confidence_impact(self, sentiment_data, trading_mode='balanced'):
        """Calculate how news sentiment affects confidence"""
        
        impact = 0
        
        # 1. Fear & Greed Index impact
        if sentiment_data.get('fear_greed'):
            fg_value = sentiment_data['fear_greed']['value']
            
            if trading_mode == 'conservative':
                # Conservative: Extreme Fear/Greed wpływa mocno
                if fg_value < 20:  # Extreme Fear
                    impact += 10  # Buying opportunity
                elif fg_value > 80:  # Extreme Greed
                    impact -= 15  # Overbought warning
                elif 40 <= fg_value <= 60:  # Neutral
                    impact += 5  # Safe zone
            
            elif trading_mode == 'balanced':
                if fg_value < 25:
                    impact += 5
                elif fg_value > 75:
                    impact -= 10
            
            elif trading_mode == 'aggressive':
                # Aggressive: High greed = momentum!
                if fg_value > 70:
                    impact += 10  # Ride the wave
                elif fg_value < 30:
                    impact += 5
        
        # 2. News sentiment impact
        overall = sentiment_data.get('overall_sentiment', 'neutral')
        positive_pct = sentiment_data.get('positive_pct', 0)
        negative_pct = sentiment_data.get('negative_pct', 0)
        
        if trading_mode == 'conservative':
            # Conservative: Negative news = strong penalty
            if overall == 'positive':
                impact += 10
            elif overall == 'negative':
                impact -= 25  # Strong penalty
        
        elif trading_mode == 'balanced':
            if overall == 'positive':
                impact += 5
            elif overall == 'negative':
                impact -= 10
        
        elif trading_mode == 'aggressive':
            # Aggressive: Positive = boost, negative = ignore FUD
            if overall == 'positive':
                impact += 15  # Big boost
            elif overall == 'negative':
                impact -= 5  # Small penalty (ignore FUD)
        
        return impact

# Global instance
news_aggregator = NewsAggregator()

