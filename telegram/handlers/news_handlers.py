from telegram import Update
from telegram.ext import ContextTypes
from ..services.news_service import NewsService
from typing import Optional

class NewsHandlers:
    def __init__(self):
        self.news_service = NewsService()
        
    async def news_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /n command - Get latest news about a coin."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /n bitcoin")
            return
            
        coin_id = context.args[0].lower()
        news = await self.news_service.get_coin_news(coin_id)
        
        if not news:
            await update.message.reply_text(f"Could not find news for {coin_id}")
            return
            
        message = f"📰 Latest News for {coin_id.upper()}:\n\n"
        for i, article in enumerate(news, 1):
            message += (
                f"{i}. {article['title']}\n"
                f"   Source: {article['source']}\n"
                f"   Published: {article['published_at']}\n"
                f"   {article['url']}\n\n"
            )
            
        await update.message.reply_text(message)
        
    async def social_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /soc command - Get social media details."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /soc bitcoin")
            return
            
        coin_id = context.args[0].lower()
        social = await self.news_service.get_social_media(coin_id)
        
        if not social:
            await update.message.reply_text(f"Could not find social media info for {coin_id}")
            return
            
        message = f"🌐 {coin_id.upper()} Social Media & Links:\n\n"
        
        if social['homepage']:
            message += f"🌍 Homepage: {social['homepage'][0]}\n"
        if social['blockchain_site']:
            message += f"🔗 Blockchain Explorer: {social['blockchain_site'][0]}\n"
        if social['official_forum_url']:
            message += f"💬 Forum: {social['official_forum_url'][0]}\n"
        if social['chat_url']:
            message += f"💭 Chat: {social['chat_url'][0]}\n"
        if social['announcement_url']:
            message += f"📢 Announcements: {social['announcement_url'][0]}\n"
        if social['twitter_screen_name']:
            message += f"🐦 Twitter: @{social['twitter_screen_name']}\n"
        if social['facebook_username']:
            message += f"👥 Facebook: {social['facebook_username']}\n"
        if social['telegram_channel_identifier']:
            message += f"📱 Telegram: {social['telegram_channel_identifier']}\n"
        if social['subreddit_url']:
            message += f"📱 Reddit: {social['subreddit_url']}\n"
            
        await update.message.reply_text(message)
        
    async def events_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /ev command - Get upcoming events."""
        if not context.args:
            await update.message.reply_text("Please provide a coin ID. Example: /ev bitcoin")
            return
            
        coin_id = context.args[0].lower()
        events = await self.news_service.get_events(coin_id)
        
        if not events:
            await update.message.reply_text(f"Could not find events for {coin_id}")
            return
            
        message = f"📅 Upcoming Events for {coin_id.upper()}:\n\n"
        for i, event in enumerate(events, 1):
            message += (
                f"{i}. {event['title']}\n"
                f"   Type: {event['type']}\n"
                f"   Date: {event['date']}\n"
                f"   {event['description']}\n"
                f"   {event['url']}\n\n"
            )
            
        await update.message.reply_text(message) 