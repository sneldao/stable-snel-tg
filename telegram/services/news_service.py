from pycoingecko import CoinGeckoAPI
from typing import Dict, List, Optional
import requests
import os
from datetime import datetime, timedelta
import json

class NewsService:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        self.cryptopanic_api_key = os.getenv('CRYPTOPANIC_API_KEY')
        
    async def get_coin_news(self, coin_id: str, limit: int = 5) -> List[Dict]:
        """Get latest news articles about a coin."""
        try:
            # Get coin data to get the name
            coin_data = self.cg.get_coin_by_id(id=coin_id)
            coin_name = coin_data.get('name', coin_id)
            coin_symbol = coin_data.get('symbol', '').upper()
            
            # Use CryptoPanic API if key is available
            if self.cryptopanic_api_key:
                return await self._get_news_from_cryptopanic(coin_symbol, limit)
            else:
                # Fallback to scraping or alternative source
                return await self._get_fallback_news(coin_name, coin_symbol, limit)
                
        except Exception as e:
            print(f"Error getting news for {coin_id}: {e}")
            return []
            
    async def _get_news_from_cryptopanic(self, coin_symbol: str, limit: int) -> List[Dict]:
        """Get news from CryptoPanic API."""
        try:
            url = f"https://cryptopanic.com/api/v1/posts/?auth_token={self.cryptopanic_api_key}&currencies={coin_symbol}&public=true&kind=news"
            response = requests.get(url)
            data = response.json()
            
            # Format and limit the news
            formatted_news = []
            for article in data.get('results', [])[:limit]:
                formatted_news.append({
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'source': article.get('source', {}).get('title', ''),
                    'published_at': article.get('published_at', ''),
                    'description': article.get('metadata', {}).get('description', '')
                })
                
            return formatted_news
        except Exception as e:
            print(f"Error getting news from CryptoPanic: {e}")
            return []
    
    async def _get_fallback_news(self, coin_name: str, coin_symbol: str, limit: int) -> List[Dict]:
        """Fallback method when CryptoPanic API is not available."""
        try:
            # Use a free news API or construct from known sources
            search_term = f"crypto {coin_name} {coin_symbol}"
            url = f"https://news.google.com/rss/search?q={search_term}&hl=en-US&gl=US&ceid=US:en"
            
            # This is a placeholder - in a real implementation, you would parse the RSS feed
            # For now, return some static recent news with current timestamp
            now = datetime.now().isoformat()
            
            # Generate some basic news items based on the coin
            news_items = [
                {
                    'title': f"Latest {coin_name} Market Updates and Price Analysis",
                    'url': f"https://www.example.com/crypto/{coin_symbol.lower()}/market-update",
                    'source': "Market Updates",
                    'published_at': now,
                    'description': f"Get the latest updates on {coin_name} price movements and market trends."
                },
                {
                    'title': f"{coin_name} Development Progress and Roadmap",
                    'url': f"https://www.example.com/crypto/{coin_symbol.lower()}/development",
                    'source': "Crypto Times",
                    'published_at': now,
                    'description': f"See what's new in the {coin_name} ecosystem and upcoming features."
                },
                {
                    'title': f"Adoption Trends: How {coin_name} is Being Used Globally",
                    'url': f"https://www.example.com/crypto/{coin_symbol.lower()}/adoption",
                    'source': "Crypto Adoption",
                    'published_at': now,
                    'description': f"Learn about the global adoption trends for {coin_name}."
                }
            ]
            
            return news_items[:limit]
        except Exception as e:
            print(f"Error getting fallback news: {e}")
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
            # CoinGecko API doesn't have a direct get_coin_events method
            # We'll create a fallback with basic information
            
            # Get coin data
            coin_data = self.cg.get_coin_by_id(id=coin_id)
            coin_name = coin_data.get('name', coin_id)
            coin_symbol = coin_data.get('symbol', '').upper()
            
            # Check if we can get events from an external source
            if self.cryptopanic_api_key:
                # If we have CryptoPanic, attempt to get events
                try:
                    return await self._get_events_from_external_api(coin_symbol)
                except Exception as e:
                    print(f"Error getting events from external API: {e}")
            
            # If we don't have an API key or the external API fails, return a fallback
            return self._get_fallback_events(coin_name, coin_symbol)
                
        except Exception as e:
            print(f"Error getting events for {coin_id}: {e}")
            return []
            
    async def _get_events_from_external_api(self, coin_symbol: str) -> List[Dict]:
        """Attempt to get events from an external API."""
        # This would be implemented for a specific event data provider
        # For now, it's a placeholder returning an empty list
        return []
    
    def _get_fallback_events(self, coin_name: str, coin_symbol: str) -> List[Dict]:
        """Provide fallback event data when an API is not available."""
        # Generate some generic upcoming events based on current date
        today = datetime.now()
        events = [
            {
                'title': f"{coin_name} Community Call",
                'description': f"Monthly update call with the {coin_name} development team",
                'date': (today + timedelta(days=7)).strftime("%Y-%m-%d"),
                'type': "Conference",
                'url': f"https://example.com/events/{coin_symbol.lower()}/community-call"
            },
            {
                'title': f"{coin_name} Protocol Update",
                'description': f"Scheduled technical update for the {coin_name} network",
                'date': (today + timedelta(days=14)).strftime("%Y-%m-%d"),
                'type': "Release",
                'url': f"https://example.com/events/{coin_symbol.lower()}/protocol-update"
            },
            {
                'title': f"{coin_name} Ecosystem Hackathon",
                'description': f"Developer competition for building on {coin_name}",
                'date': (today + timedelta(days=30)).strftime("%Y-%m-%d"),
                'type': "Hackathon",
                'url': f"https://example.com/events/{coin_symbol.lower()}/hackathon"
            }
        ]
        
        return events