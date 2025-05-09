import asyncio
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.handlers.price_handlers import PriceHandlers
from telegram.handlers.info_handlers import InfoHandlers
from telegram.handlers.news_handlers import NewsHandlers
from telegram.handlers.analysis_handlers import AnalysisHandlers
from telegram.handlers.ai_handlers import AIHandlers
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
ai_handlers = AIHandlers()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(
        f'Hello {user_first_name}! 🐌 I\'m SNEL (Slow Notably Enlightened Libertarian)!\n\n'
        'I may be slow-moving, but I\'m crypto-savvy! I can help you:\n'
        '• Swap tokens (at my own pace...)\n'
        '• Bridge assets across chains (slowly but surely)\n'
        '• Check balances (counting takes time!)\n'
        '• Navigate stablecoins & real-world assets\n\n'
        '🔹 *Commands*\n'
        '• `/p usdc` - Check stablecoin price\n'
        '• `/s usdt` - Detailed price info\n'
        '• `/i dai` - Learn about a stablecoin\n'
        '• `/ask` - Ask me any crypto question\n\n'
        '🔹 *Need Help?*\n'
        '• `/help` - See all available commands\n'
        '• `/about` - Learn more about me\n'
        '• `/status` - Check if I\'m running smoothly\n\n'
        'Visit my web-garden: https://stable-station.netlify.app/\n'
        'For guided stablecoin swaps & portfolio diversification\n\n'
        '🐌 In crypto, the tortoise beats the REKT hare!',
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🐌 SNEL\'s Slow-Motion Help Guide 🐌\n\n'
        'Price & Market Data:\n'
        '• /p <coin> - Current price\n'
        '• /s <coin> - Detailed price info\n'
        '• /c <coin> [days] - Price chart\n'
        '• /top [limit] - List top coins\n'
        '• /best <24h|7d> - Best performers\n'
        '• /worst <24h|7d> - Worst performers\n\n'
        'Coin Analysis:\n'
        '• /ch <coin> [period] - Price change\n'
        '• /roi <coin> - Return on Investment\n'
        '• /i <coin> - General information\n\n'
        'AI & Stablecoin Features:\n'
        '• /ask <question> - Ask me anything\n'
        '• /analyze <coin> - Stablecoin analysis\n'
        '• /learn <topic> - Educational content\n'
        '• /compare <coin1> <coin2> - Compare stablecoins\n'
        '• /risk <coin> - Risk assessment\n'
        '• /market - Stablecoin market overview\n\n'
        'News & Info:\n'
        '• /n <coin> - Latest news\n'
        '• /soc <coin> - Social media links\n'
        '• /ev <coin> - Upcoming events\n\n'
        'Web App: https://stable-station.netlify.app/\n'
        'For guided stablecoin swaps & portfolio diversification\n\n'
        '🐚 I move slowly, but my crypto advice is worth the wait!'
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🐌 About SNEL\n\n'
        'I\'m SNEL (Slow Notably Enlightened Libertarian), a crypto snail who takes my time but gives solid advice!\n\n'
        '🔹 My Story\n'
        'While others race for quick gains, I slowly crawl toward steady growth. My shell protects me from market volatility, just like I protect your crypto journey.\n\n'
        '🔹 Specialties\n'
        '• Stablecoins & Real World Assets (RWAs)\n'
        '• Token swaps & bridges (at snail speed)\n'
        '• Portfolio diversification\n'
        '• Risk assessment (my antenna detect danger!)\n\n'
        '🔹 Visit My Web Garden\n'
        'https://stable-station.netlify.app/\n'
        'For guided stablecoin swaps & global diversification\n\n'
        '🐚 Shell wisdom: In crypto, slow and steady makes you ready!'
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🐌 SNEL Status Check\n\n'
        '✅ Antenna: Functioning\n'
        '✅ Shell: Intact\n'
        '✅ Crypto knowledge: Up to date\n'
        '✅ Slime trail: Fresh\n\n'
        'Last crawl: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + '\n\n'
        'Moving slow but steady as always! 🐚'
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Forward to AI chat handler for more intelligent responses
    await ai_handlers.chat_message(update, context)

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
    
    # AI handlers
    application.add_handler(CommandHandler("ask", ai_handlers.ask_command))
    application.add_handler(CommandHandler("analyze", ai_handlers.analyze_command))
    application.add_handler(CommandHandler("learn", ai_handlers.learn_command))
    application.add_handler(CommandHandler("compare", ai_handlers.compare_command))
    application.add_handler(CommandHandler("risk", ai_handlers.risk_command))
    application.add_handler(CommandHandler("market", ai_handlers.market_command))
    
    # Echo handler for any other text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main() 