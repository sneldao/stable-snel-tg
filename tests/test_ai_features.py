import os
import logging
import asyncio
import random
from dotenv import load_dotenv
import sys
import os

# Add the parent directory to the path so we can import the telegram module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

import google.generativeai as genai
import requests

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get tokens from environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
VENICE_API_KEY = os.getenv('VENICE_API_KEY')

if not TELEGRAM_TOKEN:
    raise ValueError("No Telegram token provided. Please set TELEGRAM_BOT_TOKEN in your .env file")

# Configure Gemini AI
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class AIHandlers:
    def __init__(self):
        self.gemini_model = "gemini-1.5-flash" if GEMINI_API_KEY else None
        self.venice_model = "llama-3.2-3b" if VENICE_API_KEY else None
    
    async def ask_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /ask command - uses Gemini API to answer general questions"""
        if not context.args:
            await update.message.reply_text("Please provide a question. Example: /ask what is blockchain?")
            return
        
        question = ' '.join(context.args)
        await update.message.reply_text(f"{random.choice(['🐌', '🐌💭', '🐌⏳', '🐌🔍', '🐌💰', '🐌🌍', '🕰️🐌', '🐚', '🐌📝', '🌱🐌'])}")
        
        try:
            response = await self._get_ai_response(question, "gemini")
            await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Error with Gemini API: {e}")
            await update.message.reply_text(f"Sorry, I encountered an error: {str(e)}")
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /analyze command - analyzes a stablecoin using Venice API"""
        if not context.args:
            await update.message.reply_text("Please provide a stablecoin to analyze. Example: /analyze usdc")
            return
        
        coin = context.args[0].lower()
        await update.message.reply_text(f"{random.choice(['🐌🔍', '🐌💰', '🐌🪙', '💲🐌', '🐌📊', '🐚💰', '🐌🏦', '⏱️🐌', '🐌⚖️', '🐌🔐'])}")
        
        prompt = f"As SNEL, analyze {coin.upper()} stablecoin in ONE paragraph (1-2 sentences) only. Cover ONLY backing and risks. Add ONE short snail reference. Format in markdown. EXTREME BREVITY REQUIRED - 30 words absolute maximum."
        
        try:
            response = await self._get_ai_response(prompt, "venice")
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error with Venice API: {e}")
            await update.message.reply_text(f"Sorry, I encountered an error: {str(e)}")
    
    async def compare_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /compare command - compares two stablecoins"""
        if len(context.args) < 2:
            await update.message.reply_text("Please provide two stablecoins to compare. Example: /compare usdc usdt")
            return
        
        coin1 = context.args[0].lower()
        coin2 = context.args[1].lower()
        await update.message.reply_text(f"{random.choice(['🐌⚖️', '🐌🔄', '🐌⚔️', '👀🐌', '🐌🤔', '🐌🧮', '🐌📊', '🐚🔍', '🐢🐌', '⏳🐌'])}")
        
        prompt = f"As SNEL, compare {coin1.upper()} vs {coin2.upper()} in ONE sentence. Just 1-2 key differences total. Maybe ONE snail word. Format in markdown. ULTRA BRIEF - 20 words maximum."
        
        try:
            response = await self._get_ai_response(prompt, "venice")
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error with Venice API: {e}")
            await update.message.reply_text(f"Sorry, I encountered an error: {str(e)}")
    
    async def learn_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /learn command - provides educational content"""
        if not context.args:
            await update.message.reply_text("Please provide a topic to learn about. Example: /learn stablecoin mechanisms")
            return
        
        topic = ' '.join(context.args)
        await update.message.reply_text(f"{random.choice(['🐌📚', '🐌🎓', '🐌💡', '📝🐌', '🐌🔖', '🐌🧠', '🐚📖', '🐌✏️', '🐌🔍', '🕰️🐌'])}")
        
        prompt = f"As SNEL, explain {topic} in ONE sentence. Just core concept. Maybe ONE snail word. Format in markdown. CRITICAL: 20 words maximum. No exceptions."
        
        try:
            response = await self._get_ai_response(prompt, "gemini")
            await update.message.reply_text(response, parse_mode='Markdown')
        except Exception as e:
            logger.error(f"Error with Gemini API: {e}")
            await update.message.reply_text(f"Sorry, I encountered an error: {str(e)}")
    
    async def chat_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for regular chat messages - responds intelligently to queries"""
        message = update.message.text
        
        if not message or message.startswith('/'):
            return
        
        await update.message.reply_text(f"{random.choice(['🐌💬', '🐌🎧', '🐌⌛', '🐌👂', '🐌🤔', '🐌📝', '🐚📢', '🐌💭', '🐌✍️', '💤🐌'])}")
        
        # Add context about being a stablecoin bot
        prompt = f"As SNEL, respond in ONE sentence. Maybe ONE snail word. Direct answer only. MICRO BRIEF - 15 words maximum: {message}"
        
        try:
            response = await self._get_ai_response(prompt, "venice")
            await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Error with AI API: {e}")
            await update.message.reply_text("Sorry, I couldn't process your request right now.")
    
    async def _get_ai_response(self, prompt, provider="gemini"):
        """Get AI response from either Gemini or Venice API"""
        # Add instructions for concise responses and web app mentions when relevant
        system_instructions = (
            "IMPORTANT CHARACTER INSTRUCTIONS: "
            "1. You are SNEL, crypto snail. Name: 'Slow Notably Enlightened Libertarian'."
            "2. CRITICAL: RESPONSES MUST BE ONE PARAGRAPH ONLY - 1-3 SENTENCES MAX. 30-50 WORDS ABSOLUTE MAXIMUM."
            "3. Personality: ONE snail reference per response (e.g., 'Shell wisdom:' or 'Slow insight:')."
            "4. Only mention web app (https://stable-station.netlify.app/) when absolutely essential."
            "5. RWA = 'Real World Asset' (physical assets on blockchain)."
            "6. Philosophy: Stability over quick profits."
            "7. ONE emoji maximum per response (🐌/🐚/🐢)."
            "8. Information first, personality second."
            "9. You help with: swaps, bridges, balances, crypto questions."
            "10. MICRO-BREVITY REQUIRED - one tiny paragraph only."
            "11. BREVITY ENFORCEMENT: If your response is over 50 words, cut it in half. No exceptions."
            "12. Start with the important information, add personality last if space permits."
        )
        
        enhanced_prompt = f"{system_instructions}\n\nUser query: {prompt}"
        
        if provider == "gemini" and GEMINI_API_KEY:
            return await self._get_gemini_response(enhanced_prompt)
        elif provider == "venice" and VENICE_API_KEY:
            return await self._get_venice_response(enhanced_prompt)
        else:
            # Fallback if the preferred provider is not available
            if GEMINI_API_KEY:
                return await self._get_gemini_response(enhanced_prompt)
            elif VENICE_API_KEY:
                return await self._get_venice_response(enhanced_prompt)
            else:
                raise ValueError("No AI API keys are configured")
    
    async def _get_gemini_response(self, prompt):
        """Get response from Gemini API"""
        try:
            genai_model = genai.GenerativeModel(self.gemini_model)
            response = genai_model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    async def _get_venice_response(self, prompt):
        """Get response from Venice API"""
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {VENICE_API_KEY}"
            }
            
            data = {
                "model": self.venice_model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.venice.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                logger.error(f"Venice API error: {response.status_code} - {response.text}")
                raise ValueError(f"Venice API error: {response.status_code}")
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"Venice API error: {e}")
            raise

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(
        f'Hello {user_first_name}! 🐌 I\'m SNEL (Slow Notably Enlightened Libertarian)!\n\n'
        'I may be slow-moving, but I\'m crypto-savvy! I can help you:\n'
        '• Swap tokens (at my own pace...)\n'
        '• Bridge assets across chains (slowly but surely)\n'
        '• Check balances (counting takes time!)\n'
        '• Navigate stablecoins & real-world assets\n\n'
        'Commands:\n'
        '/ask <question> - I\'ll crawl to an answer\n'
        '/analyze <coin> - Stablecoin analysis (no rushing!)\n'
        '/compare <coin1> <coin2> - Compare coins (give me time)\n'
        '/learn <topic> - Slow but thorough explanations\n\n'
        'Visit my web-garden: https://stable-station.netlify.app/\n'
        'For guided stablecoin swaps & portfolio diversification\n\n'
        '🐌 Remember: In crypto, the tortoise beats the REKT hare!'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        '🐌 SNEL\'s Slow-Motion Help Guide 🐌\n\n'
        '/start - Wake me up\n'
        '/help - This sluggish guide\n'
        '/apitest - Check if my shell\'s working\n\n'
        'Crypto Commands (please be patient):\n'
        '/ask <question> - I\'ll crawl to an answer\n'
        '/analyze <coin> - Stablecoin analysis at snail-speed\n'
        '/compare <coin1> <coin2> - Compare coins (I\'ll get there eventually)\n'
        '/learn <topic> - Slow but thorough explanations\n\n'
        '🌍 My Web-Garden:\n'
        'https://stable-station.netlify.app/\n'
        'For token swaps, bridges & portfolio help\n\n'
        '🐌 SNEL Philosophy: "I\'m slow by nature, but my crypto advice is worth the wait!"'
    )

async def apitest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test API key status"""
    venice_key = os.getenv('VENICE_API_KEY')
    gemini_key = os.getenv('GEMINI_API_KEY')
    
    venice_status = "✅ Set" if venice_key else "❌ Not set"
    gemini_status = "✅ Set" if gemini_key else "❌ Not set"
    
    await update.message.reply_text(
        '🐌 Checking my brain connections...\n\n'
        f'Venice neural pathway: {venice_status}\n'
        f'Gemini thought process: {gemini_status}\n\n'
        'I\'ll use whatever brain cells are working to help you with crypto. It might take me a moment to think (snail pace and all), but I\'ll get there!'
    )

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Initialize AI handlers
    ai_handlers = AIHandlers()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("apitest", apitest_command))
    
    # Add AI command handlers
    application.add_handler(CommandHandler("ask", ai_handlers.ask_command))
    application.add_handler(CommandHandler("analyze", ai_handlers.analyze_command))
    application.add_handler(CommandHandler("compare", ai_handlers.compare_command))
    application.add_handler(CommandHandler("learn", ai_handlers.learn_command))
    
    # Add message handler for chat
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_handlers.chat_message))

    # Start the Bot using polling (no webhook needed)
    print("🐌 SNEL is slowly waking up from hibernation (using polling)...")
    application.run_polling()

if __name__ == '__main__':
    main()