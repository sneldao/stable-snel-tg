from pycoingecko import CoinGeckoAPI
from typing import Dict, List, Optional
import pandas as pd
import matplotlib.pyplot as plt
import io
from datetime import datetime, timedelta
import mplfinance as mpf

class CryptoService:
    def __init__(self):
        self.cg = CoinGeckoAPI()
        
    async def get_price(self, coin_id: str) -> Dict:
        """Get current price for a coin."""
        try:
            data = self.cg.get_price(ids=coin_id, vs_currencies='usd', include_market_cap=True, include_24hr_vol=True)
            return data.get(coin_id, {})
        except Exception as e:
            print(f"Error getting price for {coin_id}: {e}")
            return {}
            
    async def get_detailed_price(self, coin_id: str) -> Dict:
        """Get detailed price information including market data."""
        try:
            data = self.cg.get_coin_by_id(id=coin_id)
            market_data = data.get('market_data', {})
            return {
                'current_price': market_data.get('current_price', {}).get('usd', 0),
                'market_cap': market_data.get('market_cap', {}).get('usd', 0),
                'total_volume': market_data.get('total_volume', {}).get('usd', 0),
                'high_24h': market_data.get('high_24h', {}).get('usd', 0),
                'low_24h': market_data.get('low_24h', {}).get('usd', 0),
                'price_change_24h': market_data.get('price_change_24h', 0),
                'price_change_percentage_24h': market_data.get('price_change_percentage_24h', 0),
                'price_change_percentage_7d': market_data.get('price_change_percentage_7d', 0),
                'price_change_percentage_30d': market_data.get('price_change_percentage_30d', 0),
                'circulating_supply': market_data.get('circulating_supply', 0),
                'total_supply': market_data.get('total_supply', 0),
                'max_supply': market_data.get('max_supply', 0)
            }
        except Exception as e:
            print(f"Error getting detailed price for {coin_id}: {e}")
            return {}
            
    async def get_coin_info(self, coin_id: str) -> Dict:
        """Get detailed information about a coin."""
        try:
            return self.cg.get_coin_by_id(id=coin_id)
        except Exception as e:
            print(f"Error getting info for {coin_id}: {e}")
            return {}
            
    async def get_top_coins(self, limit: int = 30) -> List[Dict]:
        """Get top coins by market cap."""
        try:
            return self.cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=limit, page=1)
        except Exception as e:
            print(f"Error getting top coins: {e}")
            return []
            
    async def get_movers(self, timeframe: str = '24h', direction: str = 'gainers') -> List[Dict]:
        """Get best/worst performing coins."""
        try:
            coins = self.cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=100, page=1)
            if timeframe == '24h':
                key = 'price_change_percentage_24h'
            else:
                key = 'price_change_percentage_7d_in_currency'
                
            sorted_coins = sorted(coins, key=lambda x: x.get(key, 0), reverse=(direction == 'gainers'))
            return sorted_coins[:10]
        except Exception as e:
            print(f"Error getting movers: {e}")
            return []
            
    async def generate_price_chart(self, coin_id: str, days: int = 7) -> Optional[bytes]:
        """Generate a price chart with volume overlay."""
        try:
            # Get historical data
            data = self.cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=days)
            
            # Convert to DataFrame
            df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Add volume data
            volume_df = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])
            volume_df['timestamp'] = pd.to_datetime(volume_df['timestamp'], unit='ms')
            volume_df.set_index('timestamp', inplace=True)
            
            # Create plot
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})
            
            # Price plot
            ax1.plot(df.index, df['price'])
            ax1.set_title(f'{coin_id.upper()} Price - Last {days} Days')
            ax1.set_ylabel('Price (USD)')
            ax1.grid(True)
            
            # Volume plot
            ax2.bar(volume_df.index, volume_df['volume'])
            ax2.set_ylabel('Volume')
            ax2.grid(True)
            
            plt.tight_layout()
            
            # Save to bytes
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            plt.close()
            
            return buf.getvalue()
        except Exception as e:
            print(f"Error generating chart for {coin_id}: {e}")
            return None
            
    async def generate_candlestick_chart(self, coin_id: str, days: int = 7) -> Optional[bytes]:
        """Generate a candlestick chart."""
        try:
            # Get historical data
            data = self.cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=days)
            
            # Convert to DataFrame
            df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            # Resample to daily OHLC
            ohlc = df['price'].resample('D').ohlc()
            
            # Create candlestick chart
            mpf.plot(ohlc, type='candle', style='charles',
                    title=f'{coin_id.upper()} Price - Last {days} Days',
                    ylabel='Price (USD)',
                    savefig=dict(fname='temp.png', dpi=100, bbox_inches='tight'))
            
            # Read the saved image
            with open('temp.png', 'rb') as f:
                image_data = f.read()
                
            return image_data
        except Exception as e:
            print(f"Error generating candlestick chart for {coin_id}: {e}")
            return None 