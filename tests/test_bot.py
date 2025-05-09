import os
import logging
import sys
from dotenv import load_dotenv

# Add the parent directory to the path so we can import the telegram module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get token from environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

if not TOKEN:
    raise ValueError("No token provided. Please set TELEGRAM_BOT_TOKEN in your .env file")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(
        f'Hello {user_first_name}! I am a test bot to verify your Telegram API access works.\n\n'
        'Available commands:\n'
        '/start - Display this welcome message\n'
        '/ping - Check if the bot is responsive\n'
        '/apitest - Test Venice and Gemini API connections\n'
        '/help - Show help information'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        'Test Bot Help:\n\n'
        '/start - Display welcome message\n'
        '/ping - Check if the bot is responsive\n'
        '/apitest - Test Venice and Gemini API connections\n'
        '/help - Show this help information'
    )

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to /ping command to verify the bot is working."""
    await update.message.reply_text('Pong! 🏓 Bot is responsive.')

async def apitest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test the API connections."""
    venice_key = os.getenv('VENICE_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    venice_status = "✅ Set" if venice_key else "❌ Not set"
    gemini_status = "✅ Set" if gemini_key else "❌ Not set"
    
    await update.message.reply_text(
        'API Keys Status:\n\n'
        f'Venice API Key: {venice_status}\n'
        f'Gemini API Key: {gemini_status}\n\n'
        'If both keys are set, you should be ready to use the full bot functionality.\n'
        'Use the main bot.py script to access all features.'
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    await update.message.reply_text(
        f"You said: {update.message.text}\n\n"
        "This is a simple echo response. Try using a command like /help to see available options."
    )

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ping", ping_command))
    application.add_handler(CommandHandler("apitest", apitest_command))
    
    # Add message handler for other text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the Bot using polling (no webhook needed)
    print("Test bot is starting (using polling)...")
    application.run_polling()
    
    # Print information after initialization
    print(f"Bot username: @{application.bot.username}")

if __name__ == '__main__':
    main()