import asyncio
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.handlers.price_handlers import PriceHandlers
from telegram.handlers.info_handlers import InfoHandlers

# Load environment variables
load_dotenv()

# Get the token from environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    raise ValueError("No token provided. Please set TELEGRAM_BOT_TOKEN in your .env file")

# Initialize handlers
price_handlers = PriceHandlers()
info_handlers = InfoHandlers()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '👋 Hello! I am your crypto information bot.\n\n'
        'Available commands:\n'
        'Price Commands:\n'
        '/p <coin> - Get current price\n'
        '/s <coin> - Get detailed price info\n'
        '/c <coin> [days] - Get price chart\n'
        '/cs <coin> [days] - Get candlestick chart\n'
        '/top [limit] - Get top coins\n'
        '/best <24h|7d> - Get best performers\n'
        '/worst <24h|7d> - Get worst performers\n\n'
        'Information Commands:\n'
        '/i <coin> - Get general information\n'
        '/des <coin> - Get coin description\n'
        '/dev <coin> - Get development info\n'
        '/t <coin> - Get team information\n'
        '/wp <coin> - Find whitepaper\n\n'
        '/help - Show this help message'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start_command(update, context)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

def main():
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    
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
    
    # Echo handler for any other text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main() 