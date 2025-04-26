import asyncio
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.handlers.price_handlers import PriceHandlers
from telegram.handlers.info_handlers import InfoHandlers
from telegram.handlers.news_handlers import NewsHandlers
from telegram.handlers.analysis_handlers import AnalysisHandlers
from datetime import datetime

# Load environment variables
load_dotenv()

# Get the token from environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    raise ValueError("No token provided. Please set TELEGRAM_BOT_TOKEN in your .env file")

# Initialize handlers
price_handlers = PriceHandlers()
info_handlers = InfoHandlers()
news_handlers = NewsHandlers()
analysis_handlers = AnalysisHandlers()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '👋 Welcome to the Crypto Info Bot!\n\n'
        'I can help you with:\n'
        '• Real-time cryptocurrency prices\n'
        '• Market data and charts\n'
        '• Coin information and statistics\n'
        '• News and events\n'
        '• Technical analysis\n\n'
        'Type /help to see all available commands and features.'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '📚 Available Commands:\n\n'
        'Price Commands:\n'
        '• /p <coin> - Get current price\n'
        '• /s <coin> - Get detailed price info\n'
        '• /c <coin> [days] - Get price chart\n'
        '• /cs <coin> [days] - Get candlestick chart\n\n'
        'Market Commands:\n'
        '• /top [limit] - List top coins\n'
        '• /best <24h|7d> - Best performers\n'
        '• /worst <24h|7d> - Worst performers\n\n'
        'Information Commands:\n'
        '• /i <coin> - General information\n'
        '• /des <coin> - Coin description\n'
        '• /dev <coin> - Development info\n'
        '• /t <coin> - Team information\n'
        '• /wp <coin> - Find whitepaper\n\n'
        'News & Events:\n'
        '• /n <coin> - Latest news\n'
        '• /soc <coin> - Social media links\n'
        '• /ev <coin> - Upcoming events\n\n'
        'Technical Analysis:\n'
        '• /ch <coin> [period] - Price change\n'
        '• /roi <coin> - Return on Investment\n'
        '• /ath <coin> - All Time High analysis\n\n'
        'Utility Commands:\n'
        '• /about - About the bot\n'
        '• /help - Show this help message\n'
        '• /status - Check bot status'
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🤖 About Crypto Info Bot\n\n'
        'A comprehensive cryptocurrency information bot that provides:\n\n'
        '• Real-time price data and market statistics\n'
        '• Technical analysis with price charts\n'
        '• Detailed coin information and team data\n'
        '• News, events, and social media links\n'
        '• Development metrics and whitepaper links\n\n'
        'Data powered by CoinGecko API\n'
        'Built with Python and python-telegram-bot'
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '✅ Bot Status: Online\n\n'
        'All systems operational\n'
        'API connections: Active\n'
        'Last update: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

def main():
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("status", status_command))
    
    # Price handlers
    application.add_handler(CommandHandler("p", price_handlers.price_command))
    application.add_handler(CommandHandler("s", price_handlers.detailed_price_command))
    application.add_handler(CommandHandler("c", price_handlers.chart_command))
    application.add_handler(CommandHandler("cs", price_handlers.candlestick_command))
    application.add_handler(CommandHandler("top", price_handlers.top_command))
    application.add_handler(CommandHandler("best", price_handlers.movers_command))
    application.add_handler(CommandHandler("worst", price_handlers.movers_command))
    
    # Info handlers
    application.add_handler(CommandHandler("i", info_handlers.info_command))
    application.add_handler(CommandHandler("des", info_handlers.description_command))
    application.add_handler(CommandHandler("dev", info_handlers.development_command))
    application.add_handler(CommandHandler("t", info_handlers.team_command))
    application.add_handler(CommandHandler("wp", info_handlers.whitepaper_command))
    
    # News handlers
    application.add_handler(CommandHandler("n", news_handlers.news_command))
    application.add_handler(CommandHandler("soc", news_handlers.social_command))
    application.add_handler(CommandHandler("ev", news_handlers.events_command))
    
    # Analysis handlers
    application.add_handler(CommandHandler("ch", analysis_handlers.price_change_command))
    application.add_handler(CommandHandler("roi", analysis_handlers.roi_command))
    application.add_handler(CommandHandler("ath", analysis_handlers.ath_command))
    
    # Echo handler for any other text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main() 