from telegram import Update
from telegram.ext import ContextTypes
from ..services.crypto_service import CryptoService
from typing import Optional

class PriceHandlers:
    def __init__(self):
        self.crypto_service = CryptoService()
        
    async def price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /p command - Get current price for a coin."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /p bitcoin")
            return
            
        coin_id = context.args[0].lower()
        price_data = await self.crypto_service.get_price(coin_id)
        
        if not price_data:
            await update.message.reply_text(f"Could not find price data for {coin_id}")
            return
            
        message = (
            f"💰 {coin_id.upper()} Price:\n"
            f"${price_data.get('usd', 'N/A'):,.2f}\n"
            f"24h Volume: ${price_data.get('usd_24h_vol', 'N/A'):,.2f}\n"
            f"Market Cap: ${price_data.get('usd_market_cap', 'N/A'):,.2f}"
        )
        await update.message.reply_text(message)
        
    async def detailed_price_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /s command - Get detailed price information."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /s bitcoin")
            return
            
        coin_id = context.args[0].lower()
        price_data = await self.crypto_service.get_detailed_price(coin_id)
        
        if not price_data:
            await update.message.reply_text(f"Could not find detailed price data for {coin_id}")
            return
            
        # Default to 0 for any None values
        current_price = price_data.get('current_price', 0) or 0
        market_cap = price_data.get('market_cap', 0) or 0
        total_volume = price_data.get('total_volume', 0) or 0
        high_24h = price_data.get('high_24h', 0) or 0
        low_24h = price_data.get('low_24h', 0) or 0
        price_change_24h = price_data.get('price_change_percentage_24h', 0) or 0
        price_change_7d = price_data.get('price_change_percentage_7d', 0) or 0
        price_change_30d = price_data.get('price_change_percentage_30d', 0) or 0
        circulating_supply = price_data.get('circulating_supply', 0) or 0
        total_supply = price_data.get('total_supply', 0) or 0
        max_supply = price_data.get('max_supply', 0) or 0
            
        message = (
            f"📊 {coin_id.upper()} Detailed Price Info:\n\n"
            f"Current Price: ${current_price:,.2f}\n"
            f"Market Cap: ${market_cap:,.2f}\n"
            f"24h Volume: ${total_volume:,.2f}\n"
            f"24h High: ${high_24h:,.2f}\n"
            f"24h Low: ${low_24h:,.2f}\n"
            f"24h Change: {price_change_24h:+.2f}%\n"
            f"7d Change: {price_change_7d:+.2f}%\n"
            f"30d Change: {price_change_30d:+.2f}%\n\n"
            f"Circulating Supply: {circulating_supply:,.0f}\n"
            f"Total Supply: {total_supply:,.0f}\n"
            f"Max Supply: {max_supply:,.0f}"
        )
        await update.message.reply_text(message)
        
    async def chart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /c command - Get price chart for a coin."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /c bitcoin")
            return
            
        coin_id = context.args[0].lower()
        days = 7  # Default to 7 days
        
        if len(context.args) > 1:
            try:
                days = int(context.args[1])
            except ValueError:
                await update.message.reply_text("Invalid number of days. Using default (7 days)")
                
        chart_data = await self.crypto_service.generate_price_chart(coin_id, days)
        
        if not chart_data:
            await update.message.reply_text(f"Could not generate chart for {coin_id}")
            return
            
        await update.message.reply_photo(chart_data, caption=f"{coin_id.upper()} Price Chart - Last {days} Days")
        
    async def candlestick_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /cs command - Get candlestick chart for a coin."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /cs bitcoin")
            return
            
        coin_id = context.args[0].lower()
        days = 7  # Default to 7 days
        
        if len(context.args) > 1:
            try:
                days = int(context.args[1])
            except ValueError:
                await update.message.reply_text("Invalid number of days. Using default (7 days)")
                
        chart_data = await self.crypto_service.generate_candlestick_chart(coin_id, days)
        
        if not chart_data:
            await update.message.reply_text(f"Could not generate candlestick chart for {coin_id}")
            return
            
        await update.message.reply_photo(chart_data, caption=f"{coin_id.upper()} Candlestick Chart - Last {days} Days")
        
    async def top_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /top command - Get top coins by market cap."""
        limit = 30  # Default to top 30
        
        if context.args:
            try:
                limit = int(context.args[0])
            except ValueError:
                await update.message.reply_text("Invalid number. Using default (30 coins)")
                
        coins = await self.crypto_service.get_top_coins(limit)
        
        if not coins:
            await update.message.reply_text("Could not fetch top coins data")
            return
            
        message = "📊 Top Coins by Market Cap:\n\n"
        for i, coin in enumerate(coins, 1):
            price_change = coin.get('price_change_percentage_24h', 0)
            if price_change is None:
                price_change = 0
                
            message += (
                f"{i}. {coin['symbol'].upper()}: ${coin['current_price']:,.2f}\n"
                f"   24h: {price_change:+.2f}%\n"
            )
            
        await update.message.reply_text(message)
        
    async def movers_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /best and /worst commands - Get best/worst performing coins."""
        if not context.args:
            await update.message.reply_text("Please specify timeframe: 24h or 7d")
            return
            
        timeframe = context.args[0].lower()
        if timeframe not in ['24h', '7d']:
            await update.message.reply_text("Invalid timeframe. Use 24h or 7d")
            return
            
        # Check if command is /best or /worst
        direction = 'gainers'  # Default
        if update.message and update.message.text:
            if update.message.text.startswith('/worst'):
                direction = 'losers'
                
        coins = await self.crypto_service.get_movers(timeframe, direction)
        
        if not coins:
            await update.message.reply_text(f"Could not fetch {direction} data")
            return
            
        title = "Gainers" if direction == 'gainers' else "Losers"
        message = f"📈 Top {title} ({timeframe}):\n\n"
        
        for i, coin in enumerate(coins, 1):
            change_key = 'price_change_percentage_24h' if timeframe == '24h' else 'price_change_percentage_7d_in_currency'
            price_change = coin.get(change_key, 0)
            if price_change is None:
                price_change = 0
                
            message += (
                f"{i}. {coin['symbol'].upper()}: ${coin['current_price']:,.2f}\n"
                f"   Change: {price_change:+.2f}%\n"
            )
            
        await update.message.reply_text(message)