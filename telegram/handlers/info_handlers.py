from telegram import Update
from telegram.ext import ContextTypes
from ..services.info_service import InfoService
from typing import Optional

class InfoHandlers:
    def __init__(self):
        self.info_service = InfoService()
        
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /i command - Get general coin information."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /i bitcoin")
            return
            
        coin_id = context.args[0].lower()
        info = await self.info_service.get_coin_info(coin_id)
        
        if not info:
            await update.message.reply_text(f"Could not find information for {coin_id}")
            return
            
        message = (
            f"📊 {info['name']} ({info['symbol']}) Information:\n\n"
            f"Current Price: ${info['current_price']:,.2f}\n"
            f"Market Cap: ${info['market_cap']:,.2f}\n"
            f"24h Volume: ${info['total_volume']:,.2f}\n"
            f"Circulating Supply: {info['circulating_supply']:,.0f}\n"
            f"Total Supply: {info['total_supply']:,.0f}\n"
            f"Max Supply: {info['max_supply']:,.0f}\n\n"
            f"All Time High: ${info['ath']:,.2f} ({info['ath_date']})\n"
            f"All Time Low: ${info['atl']:,.2f} ({info['atl_date']})"
        )
        await update.message.reply_text(message)
        
    async def description_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /des command - Get coin description."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /des bitcoin")
            return
            
        coin_id = context.args[0].lower()
        description = await self.info_service.get_coin_description(coin_id)
        
        if not description:
            await update.message.reply_text(f"Could not find description for {coin_id}")
            return
            
        # Split long descriptions into chunks
        max_length = 4000  # Telegram message limit
        chunks = [description[i:i+max_length] for i in range(0, len(description), max_length)]
        
        for i, chunk in enumerate(chunks):
            if i == 0:
                await update.message.reply_text(f"📝 {coin_id.upper()} Description:\n\n{chunk}")
            else:
                await update.message.reply_text(chunk)
                
    async def development_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /dev command - Get development information."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /dev bitcoin")
            return
            
        coin_id = context.args[0].lower()
        dev_info = await self.info_service.get_development_info(coin_id)
        
        if not dev_info:
            await update.message.reply_text(f"Could not find development information for {coin_id}")
            return
            
        message = (
            f"👨‍💻 {coin_id.upper()} Development Stats:\n\n"
            f"GitHub Repositories: {len(dev_info['github_repos'])}\n"
            f"Forks: {dev_info['forks']}\n"
            f"Stars: {dev_info['stars']}\n"
            f"Subscribers: {dev_info['subscribers']}\n"
            f"Total Issues: {dev_info['total_issues']}\n"
            f"Closed Issues: {dev_info['closed_issues']}\n"
            f"Pull Requests Merged: {dev_info['pull_requests_merged']}\n"
            f"Pull Request Contributors: {dev_info['pull_request_contributors']}"
        )
        await update.message.reply_text(message)
        
    async def team_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /t command - Get team information."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /t bitcoin")
            return
            
        coin_id = context.args[0].lower()
        team = await self.info_service.get_team_info(coin_id)
        
        if not team:
            await update.message.reply_text(f"Could not find team information for {coin_id}")
            return
            
        message = f"👥 {coin_id.upper()} Team:\n\n"
        for member in team:
            message += (
                f"Name: {member.get('name', 'N/A')}\n"
                f"Position: {member.get('position', 'N/A')}\n"
                f"LinkedIn: {member.get('linkedin', 'N/A')}\n"
                f"Twitter: {member.get('twitter', 'N/A')}\n\n"
            )
            
        await update.message.reply_text(message)
        
    async def whitepaper_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /wp command - Find whitepaper."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /wp bitcoin")
            return
            
        coin_id = context.args[0].lower()
        whitepaper_url = await self.info_service.find_whitepaper(coin_id)
        
        if not whitepaper_url:
            await update.message.reply_text(f"Could not find whitepaper for {coin_id}")
            return
            
        await update.message.reply_text(f"📄 {coin_id.upper()} Whitepaper:\n{whitepaper_url}") 