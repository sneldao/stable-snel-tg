from telegram import Update
from telegram.ext import ContextTypes
from ..services.ai_service import AIService
from ..services.venice_service import VeniceService
from ..services.crypto_service import CryptoService
from typing import Dict, List, Optional
import json
import random

class AIHandlers:
    def __init__(self):
        self.venice_service = VeniceService()
        self.ai_service = AIService(venice_service=self.venice_service)
        self.crypto_service = CryptoService()
        
    async def ask_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /ask command - Ask the AI a question."""
        if not context.args:
            await update.message.reply_text("Please ask a question. Example: /ask What are stablecoins?")
            return
            
        query = ' '.join(context.args)
        
        # Send snail thinking emoji
        await update.message.reply_text(f"{random.choice(['🐌💭', '🐌⏳', '🐌🔍', '🐌💰', '🐌🌍', '🕰️🐌', '🐚', '🐌📝', '🌱🐌'])}")
        
        # Send typing indicator to show the bot is processing
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        response = await self.ai_service.get_response(query)
        await update.message.reply_text(response)
        
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /analyze command - Analyze a stablecoin."""
        if not context.args:
            await update.message.reply_text("Please provide a stablecoin to analyze. Example: /analyze usdc")
            return
            
        coin_id = context.args[0].lower()
        
        # Send snail analyzing emoji
        await update.message.reply_text(f"{random.choice(['🐌🔍', '🐌💰', '🐌🪙', '💲🐌', '🐌📊', '🐚💰', '🐌🏦', '⏱️🐌', '🐌⚖️', '🐌🔐'])}")
        
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get comprehensive coin data for context
        price_data = await self.crypto_service.get_detailed_price(coin_id)
        info_data = await self.crypto_service.get_coin_info(coin_id)
        
        # Combine data for context
        context_data = {
            "price_data": price_data,
            "info_data": info_data
        }
        
        # Get AI analysis with context data
        analysis = await self.ai_service.analyze_stablecoin(coin_id, context_data)
        
        # Format message
        if "analysis" in analysis:
            message = f"🔍 *Analysis for {coin_id.upper()}*\n\n{analysis['analysis']}"
        else:
            message = (
                f"🔍 *Analysis for {coin_id.upper()}*\n\n"
                f"*Stability Mechanism:* {analysis.get('stability_mechanism', 'Not available')}\n\n"
                f"*Risk Assessment:*\n{analysis.get('risks', 'Risk data not available')}\n\n"
                f"*Historical Performance:*\n{analysis.get('historical_performance', 'Performance data not available')}\n\n"
                f"*Regulatory Status:*\n{analysis.get('regulatory_status', 'Regulatory data not available')}\n\n"
                f"*Community Trust:*\n{analysis.get('community_trust', 'Trust data not available')}\n\n"
                f"Remember: Slow and steady may not necessarily win the race, but crashing and burning is a sure way to lose it! 🐌"
            )
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    async def learn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /learn command - Get educational content about stablecoins."""
        if not context.args:
            await update.message.reply_text("Please specify a topic to learn about. Example: /learn depeg risks")
            return
            
        topic = ' '.join(context.args)
        
        # Send snail learning emoji
        await update.message.reply_text(f"{random.choice(['🐌📚', '🐌🎓', '🐌💡', '📝🐌', '🐌🔖', '🐌🧠', '🐚📖', '🐌✏️', '🐌🔍', '🕰️🐌'])}")
        
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get educational content
        content = await self.ai_service.get_educational_content(topic)
        
        message = f"📚 *Learning about: {topic}*\n\n{content}"
        await update.message.reply_text(message, parse_mode='Markdown')
        
    async def compare_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /compare command - Compare stablecoins."""
        if len(context.args) < 2:
            await update.message.reply_text("Please provide at least two stablecoins to compare. Example: /compare usdc dai")
            return
            
        coin_ids = [arg.lower() for arg in context.args]
        
        # Send snail comparing emoji
        await update.message.reply_text(f"{random.choice(['🐌⚖️', '🐌🔄', '🐌⚔️', '👀🐌', '🐌🤔', '🐌🧮', '🐌📊', '🐚🔍', '🐢🐌', '⏳🐌'])}")
        
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get comparison from AI
        comparison = await self.ai_service.compare_stablecoins(coin_ids)
        
        message = f"⚖️ *Stablecoin Comparison*\n\n{comparison}"
        await update.message.reply_text(message, parse_mode='Markdown')
        
    async def risk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /risk command - Get risk assessment for a stablecoin."""
        if not context.args:
            await update.message.reply_text("Please provide a stablecoin for risk assessment. Example: /risk usdt")
            return
            
        coin_id = context.args[0].lower()
        
        # Send snail risk assessment emoji
        await update.message.reply_text(f"{random.choice(['🐌⚠️', '🐌🛡️', '🐚🔍', '🐌🔐', '🐌⚖️', '🐌🚨', '🐌🔒', '🐌⛔', '🐌📊', '🕰️🐌'])}")
        
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get comprehensive coin data for risk assessment
        price_data = await self.crypto_service.get_detailed_price(coin_id)
        info_data = await self.crypto_service.get_coin_info(coin_id)
        
        # Combine data for context
        context_data = {
            "price_data": price_data,
            "info_data": info_data
        }
        
        # Create risk assessment prompt for AI
        risk_prompt = f"As SNEL the crypto snail, briefly assess the risks for stablecoin {coin_id}. Include: depeg risk, regulatory risk, smart contract risk, counterparty risk, and overall risk score. KEEP IT EXTREMELY BRIEF - ONE short paragraph maximum. Add ONE snail reference."
            
        # Get risk assessment from AI
        risk_response = await self.ai_service.get_response(risk_prompt, context=[context_data])
        
        # Format message with the AI's response
        message = (
            f"⚠️ *Risk Assessment for {coin_id.upper()}*\n\n"
            f"{risk_response}"
        )
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    async def market_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /market command - Get stablecoin market overview."""
        # Send snail market emoji
        await update.message.reply_text(f"{random.choice(['🐌🌍', '🐌📈', '🐌💹', '🐌🏦', '🐌💰', '🐌🪙', '🐚📊', '🐌💱', '🐌🌐', '🕰️🐌'])}")
        
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get market data from CoinGecko
        top_coins = await self.crypto_service.get_top_coins(limit=50)
        
        # Filter for stablecoins (approximate method - could be improved)
        stablecoins = [coin for coin in top_coins if 
                       any(stable_term in coin.get('id', '').lower() for stable_term in 
                           ['usd', 'usdt', 'usdc', 'dai', 'busd', 'frax', 'tusd', 'gusd', 'stable']) or
                       abs(coin.get('price_change_percentage_24h', 100)) < 1.0]  # Low volatility is a stablecoin indicator
        
        # Calculate market data
        stablecoin_market_cap = sum(coin.get('market_cap', 0) for coin in stablecoins)
        stablecoin_volume = sum(coin.get('total_volume', 0) for coin in stablecoins)
        
        # Get total market data
        total_market_cap = sum(coin.get('market_cap', 0) for coin in top_coins)
        
        # Create market summary
        market_data = {
            "total_market_cap_usd": stablecoin_market_cap,
            "daily_volume_usd": stablecoin_volume,
            "stablecoin_dominance": stablecoin_market_cap / total_market_cap if total_market_cap > 0 else 0,
            "stablecoins": stablecoins[:10]  # Top 10 stablecoins
        }
        
        # Create market overview prompt for AI
        market_prompt = f"As SNEL the crypto snail, provide a VERY BRIEF overview of the stablecoin market based on this data: {json.dumps(market_data, indent=2)}. Include ONLY key insights on market cap, volume, and trends. MAXIMUM ONE PARAGRAPH with 1-2 sentences. Add ONE snail reference if possible."
        
        # Get market overview from AI
        market_response = await self.ai_service.get_response(market_prompt)
        
        # Format message
        message = (
            f"🌍 *Stablecoin Market Overview*\n\n"
            f"*Total Market Cap:* ${market_data.get('total_market_cap_usd', 0)/1e9:.2f}B\n"
            f"*Daily Volume:* ${market_data.get('daily_volume_usd', 0)/1e9:.2f}B\n"
            f"*Stablecoin Market Dominance:* {market_data.get('stablecoin_dominance', 0)*100:.1f}%\n\n"
            f"{market_response}"
        )
        
        await update.message.reply_text(message, parse_mode='Markdown')
        
    async def chat_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle text messages not directed at specific commands."""
        # Don't process empty messages
        if not update.message or not update.message.text:
            return
            
        message_text = update.message.text.strip()
        
        # Check if this is a direct message (private chat)
        is_direct_message = update.effective_chat.type == 'private'
        
        # Check if the bot was mentioned in a group chat
        bot_username = context.bot.username
        is_mentioned = bot_username and f"@{bot_username}" in message_text
        
        # Only respond in direct messages or when mentioned in groups
        if not (is_direct_message or is_mentioned):
            return
            
        # If mentioned, remove the bot username from the message
        query = message_text
        if is_mentioned:
            query = message_text.replace(f"@{bot_username}", "").strip()
            
        # If the query is empty after processing, use a default greeting
        if not query:
            query = "Hello"
            
        # Send snail chat emoji
        await update.message.reply_text(f"{random.choice(['🐌💬', '🐌🎧', '🐌⌛', '🐌👂', '🐌🤔', '🐌📝', '🐚📢', '🐌💭', '🐌✍️', '💤🐌'])}")
        
        # Send typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Get AI response
        response = await self.ai_service.get_response(query)
        
        await update.message.reply_text(response)