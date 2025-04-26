from pycoingecko import CoinGeckoAPI
from typing import Dict, List, Optional
import requests
from datetime import datetime, timedelta

class NewsService:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        
    async def get_coin_news(self, coin_id: str, limit: int = 5) -> List[Dict]:
        """Get latest news articles about a coin."""
        try:
            # Get coin data to get the name
            coin_data = self.cg.get_coin_by_id(id=coin_id)
            coin_name = coin_data.get('name', coin_id)
            
            # Get news from CoinGecko
            news = self.cg.get_coin_news(coin_name)
            
            # Format and limit the news
            formatted_news = []
            for article in news[:limit]:
                formatted_news.append({
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', ''),
                    'published_at': article.get('published_at', ''),
                    'description': article.get('description', '')
                })
                
            return formatted_news
        except Exception as e:
            print(f"Error getting news for {coin_id}: {e}")
            return []
            
    async def get_social_media(self, coin_id: str) -> Dict:
        """Get social media presence and engagement."""
        try:
            data = self.cg.get_coin_by_id(id=coin_id)
            links = data.get('links', {})
            
            return {
                'homepage': links.get('homepage', []),
                'blockchain_site': links.get('blockchain_site', []),
                'official_forum_url': links.get('official_forum_url', []),
                'chat_url': links.get('chat_url', []),
                'announcement_url': links.get('announcement_url', []),
                'twitter_screen_name': links.get('twitter_screen_name', ''),
                'facebook_username': links.get('facebook_username', ''),
                'telegram_channel_identifier': links.get('telegram_channel_identifier', ''),
                'subreddit_url': links.get('subreddit_url', ''),
                'repos_url': links.get('repos_url', {})
            }
        except Exception as e:
            print(f"Error getting social media for {coin_id}: {e}")
            return {}
            
    async def get_events(self, coin_id: str) -> List[Dict]:
        """Get upcoming events for a coin."""
        try:
            # Get coin data to get the name
            coin_data = self.cg.get_coin_by_id(id=coin_id)
            coin_name = coin_data.get('name', coin_id)
            
            # Get events from CoinGecko
            events = self.cg.get_coin_events(coin_name)
            
            # Format the events
            formatted_events = []
            for event in events:
                formatted_events.append({
                    'title': event.get('title', ''),
                    'description': event.get('description', ''),
                    'date': event.get('date', ''),
                    'type': event.get('type', ''),
                    'url': event.get('url', '')
                })
                
            return formatted_events
        except Exception as e:
            print(f"Error getting events for {coin_id}: {e}")
            return [] 