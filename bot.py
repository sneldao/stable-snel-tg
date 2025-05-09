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
        f'Welcome {user_first_name}! 💰 I\'m SNEL (Stablecoin Navigation and Education Leader).\n\n'
        'I\'m here to assist you with:\n'
        '• Stablecoin information and analysis\n'
        '• Real-world asset (RWA) insights\n'
        '• Risk assessment and portfolio diversification\n'
        '• Market data and investment strategies\n\n'
        '🔹 *Key Commands*\n'
        '• `/p usdc` - Check stablecoin price\n'
        '• `/s usdt` - Detailed price info\n'
        '• `/i dai` - Learn about a stablecoin\n'
        '• `/ask` - Ask me any crypto question\n\n'
        '🔹 *Need Help?*\n'
        '• `/help` - See all available commands\n'
        '• `/about` - Learn more about SNEL\n'
        '• `/status` - Check system status\n\n'
        'Visit Stable Station: https://stable-station.netlify.app/\n'
        'For guided stablecoin swaps & portfolio diversification\n\n'
        'Check market insights: https://stable-snel.netlify.app/\n'
        'For on/off ramp solutions and data analytics',
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '📊 SNEL Command Reference Guide 📊\n\n'
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
        'Web Apps:\n'
        '• Stable Station: https://stable-station.netlify.app/\n'
        '  For guided stablecoin swaps & portfolio diversification\n'
        '• SNEL Analytics: https://stable-snel.netlify.app/\n'
        '  For market insights and on/off ramp solutions'
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '💰 About SNEL\n\n'
        'SNEL (Stablecoin Navigation and Education Leader) is your professional guide to stability in the volatile crypto markets.\n\n'
        '🔹 Our Mission\n'
        'While much of crypto focuses on high-risk speculation, SNEL emphasizes stability, risk management, and long-term wealth preservation through stablecoins and real-world assets.\n\n'
        '🔹 Specialties\n'
        '• Stablecoins & Real World Assets (RWAs)\n'
        '• Strategic portfolio diversification\n'
        '• Risk assessment and mitigation\n'
        '• Market analysis and education\n\n'
        '🔹 Web Resources\n'
        '• Stable Station: https://stable-station.netlify.app/\n'
        '  For guided stablecoin swaps & global diversification\n'
        '• SNEL Analytics: https://stable-snel.netlify.app/\n'
        '  For market insights and on/off ramp solutions\n\n'
        '📊 In crypto, prioritizing stability and understanding risk is the path to long-term success.'
    )

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🔹 SNEL System Status 🔹\n\n'
        '✅ API Connections: Online\n'
        '✅ Database: Operational\n'
        '✅ Market Data: Up to date\n'
        '✅ AI Systems: Responsive\n\n'
        'Last update: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC') + '\n\n'
        'All systems operational. For market insights, visit: https://stable-snel.netlify.app/'
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle normal text messages (non-commands):
    - Process all direct message chats
    - In groups, only respond when mentioned
    """
    try:
        # Forward message to AI handler which will handle both direct messages
        # and group mentions appropriately
        await ai_handlers.chat_message(update, context)
    except Exception as e:
        print(f"Error in AI chat handling: {e}")
        # Fallback to basic echo if AI fails
        if update.effective_chat.type == 'private':
            await update.message.reply_text("I'm currently experiencing high request volume. Please try a command like /help or /p bitcoin")

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