from pycoingecko import CoinGeckoAPI
from typing import Dict, Optional, List
import requests
from bs4 import BeautifulSoup

class InfoService:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        
    async def get_coin_info(self, coin_id: str) -> Dict:
        """Get general information about a coin."""
        try:
            data = self.cg.get_coin_by_id(id=coin_id)
            return {
                'name': data.get('name', ''),
                'symbol': data.get('symbol', '').upper(),
                'current_price': data.get('market_data', {}).get('current_price', {}).get('usd', 0),
                'market_cap': data.get('market_data', {}).get('market_cap', {}).get('usd', 0),
                'total_volume': data.get('market_data', {}).get('total_volume', {}).get('usd', 0),
                'circulating_supply': data.get('market_data', {}).get('circulating_supply', 0),
                'total_supply': data.get('market_data', {}).get('total_supply', 0),
                'max_supply': data.get('market_data', {}).get('max_supply', 0),
                'ath': data.get('market_data', {}).get('ath', {}).get('usd', 0),
                'ath_date': data.get('market_data', {}).get('ath_date', {}).get('usd', ''),
                'atl': data.get('market_data', {}).get('atl', {}).get('usd', 0),
                'atl_date': data.get('market_data', {}).get('atl_date', {}).get('usd', '')
            }
        except Exception as e:
            print(f"Error getting coin info for {coin_id}: {e}")
            return {}
            
    async def get_coin_description(self, coin_id: str) -> str:
        """Get detailed description of a coin."""
        try:
            data = self.cg.get_coin_by_id(id=coin_id)
            return data.get('description', {}).get('en', 'No description available')
        except Exception as e:
            print(f"Error getting description for {coin_id}: {e}")
            return 'Error fetching description'
            
    async def get_development_info(self, coin_id: str) -> Dict:
        """Get development information including GitHub stats."""
        try:
            data = self.cg.get_coin_by_id(id=coin_id)
            return {
                'github_repos': data.get('developer_data', {}).get('repos', []),
                'forks': data.get('developer_data', {}).get('forks', 0),
                'stars': data.get('developer_data', {}).get('stars', 0),
                'subscribers': data.get('developer_data', {}).get('subscribers', 0),
                'total_issues': data.get('developer_data', {}).get('total_issues', 0),
                'closed_issues': data.get('developer_data', {}).get('closed_issues', 0),
                'pull_requests_merged': data.get('developer_data', {}).get('pull_requests_merged', 0),
                'pull_request_contributors': data.get('developer_data', {}).get('pull_request_contributors', 0)
            }
        except Exception as e:
            print(f"Error getting development info for {coin_id}: {e}")
            return {}
            
    async def get_team_info(self, coin_id: str) -> List[Dict]:
        """Get team information for a coin."""
        try:
            data = self.cg.get_coin_by_id(id=coin_id)
            return data.get('team', [])
        except Exception as e:
            print(f"Error getting team info for {coin_id}: {e}")
            return []
            
    async def find_whitepaper(self, coin_id: str) -> Optional[str]:
        """Find whitepaper URL for a coin."""
        try:
            data = self.cg.get_coin_by_id(id=coin_id)
            links = data.get('links', {})
            
            # Check common whitepaper locations
            if 'whitepaper' in links:
                return links['whitepaper']
            elif 'whitepaper_link' in links:
                return links['whitepaper_link']
            elif 'whitepaper_url' in links:
                return links['whitepaper_url']
                
            # If not found in direct links, try to find in homepage
            if 'homepage' in links and links['homepage']:
                try:
                    response = requests.get(links['homepage'])
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Look for common whitepaper link patterns
                    for link in soup.find_all('a'):
                        href = link.get('href', '').lower()
                        if 'whitepaper' in href or 'white-paper' in href:
                            return href
                except Exception as e:
                    print(f"Error searching homepage for whitepaper: {e}")
                    
            return None
        except Exception as e:
            print(f"Error finding whitepaper for {coin_id}: {e}")
            return None 