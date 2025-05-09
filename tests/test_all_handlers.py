import asyncio
import os
from dotenv import load_dotenv
from typing import Dict, List, Any
import time

# Load environment variables before importing handlers
load_dotenv()

# Import handlers
from telegram.handlers.price_handlers import PriceHandlers
from telegram.handlers.info_handlers import InfoHandlers
from telegram.handlers.news_handlers import NewsHandlers
from telegram.handlers.analysis_handlers import AnalysisHandlers
from telegram.handlers.ai_handlers import AIHandlers

# Mock Update and Context classes for testing
class MockMessage:
    def __init__(self, text=None):
        self.text = text
        self.message_id = 123

    async def reply_text(self, text, parse_mode=None, **kwargs):
        print(f"\033[92m✓ Response received:\033[0m {text[:100]}{'...' if len(text) > 100 else ''}")
        return MockMessage()
        
    async def reply_photo(self, photo, caption=None, **kwargs):
        print(f"\033[92m✓ Photo response received\033[0m with caption: {caption}")
        return MockMessage()

class MockUser:
    def __init__(self, first_name="Test User"):
        self.first_name = first_name
        self.id = 12345

class MockChat:
    def __init__(self, id=123456789, type="private"):
        self.id = id
        self.type = type  # private or group

class MockUpdate:
    def __init__(self, message_text=None, chat_type="private"):
        self.message = MockMessage(message_text)
        self.effective_chat = MockChat(type=chat_type)
        self.effective_user = MockUser()

class MockBot:
    def __init__(self):
        self.username = "test_bot"
        
    async def send_chat_action(self, chat_id, action):
        print(f"\033[94m→ Bot action: {action}\033[0m")

class MockContext:
    def __init__(self, args=None):
        self.args = args or []
        self.bot = MockBot()

async def test_handler(handler_func, args=None, message_text=None, chat_type="private"):
    """Generic function to test a handler"""
    update = MockUpdate(message_text, chat_type)
    context = MockContext(args)
    
    print(f"\033[93m\n========== Testing {handler_func.__name__} ==========\033[0m")
    
    if args:
        print(f"\033[94m→ Args: {args}\033[0m")
    
    try:
        start_time = time.time()
        await handler_func(update, context)
        elapsed_time = time.time() - start_time
        print(f"\033[92m✓ Test completed in {elapsed_time:.2f}s\033[0m")
        return True
    except Exception as e:
        print(f"\033[91m✗ Test failed: {str(e)}\033[0m")
        import traceback
        traceback.print_exc()
        return False

async def test_price_handlers():
    """Test price handler functions"""
    print("\033[95m\n===== TESTING PRICE HANDLERS =====\033[0m")
    
    price_handlers = PriceHandlers()
    
    tests = [
        ("price_command", ["bitcoin"]),
        ("detailed_price_command", ["ethereum"]),
        ("top_command", ["10"]),
        ("movers_command", ["24h"]), 
    ]
    
    results = []
    for func_name, args in tests:
        handler_func = getattr(price_handlers, func_name)
        result = await test_handler(handler_func, args)
        results.append(result)
    
    return all(results)

async def test_info_handlers():
    """Test info handler functions"""
    print("\033[95m\n===== TESTING INFO HANDLERS =====\033[0m")
    
    info_handlers = InfoHandlers()
    
    tests = [
        ("info_command", ["usdc"]),
        ("description_command", ["dai"]),
        # Optional tests - can be slow
        # ("development_command", ["ethereum"]),
        # ("team_command", ["ethereum"]),
        # ("whitepaper_command", ["bitcoin"]),
    ]
    
    results = []
    for func_name, args in tests:
        handler_func = getattr(info_handlers, func_name)
        result = await test_handler(handler_func, args)
        results.append(result)
    
    return all(results)

async def test_news_handlers():
    """Test news handler functions"""
    print("\033[95m\n===== TESTING NEWS HANDLERS =====\033[0m")
    
    news_handlers = NewsHandlers()
    
    tests = [
        ("news_command", ["bitcoin"]),
        ("social_command", ["ethereum"]),
        ("events_command", ["usdc"]),
    ]
    
    results = []
    for func_name, args in tests:
        handler_func = getattr(news_handlers, func_name)
        result = await test_handler(handler_func, args)
        results.append(result)
    
    return all(results)

async def test_analysis_handlers():
    """Test analysis handler functions"""
    print("\033[95m\n===== TESTING ANALYSIS HANDLERS =====\033[0m")
    
    analysis_handlers = AnalysisHandlers()
    
    tests = [
        ("price_change_command", ["bitcoin", "7d"]),
        ("roi_command", ["ethereum"]),
        ("ath_command", ["bitcoin"]),
    ]
    
    results = []
    for func_name, args in tests:
        handler_func = getattr(analysis_handlers, func_name)
        result = await test_handler(handler_func, args)
        results.append(result)
    
    return all(results)

async def test_ai_handlers():
    """Test AI handler functions"""
    print("\033[95m\n===== TESTING AI HANDLERS =====\033[0m")
    
    ai_handlers = AIHandlers()
    
    tests = [
        ("ask_command", ["What is a stablecoin?"]),
        # Optional tests - can take longer
        # ("analyze_command", ["usdc"]),
        # ("learn_command", ["depeg risk"]),
        # ("compare_command", ["usdc", "dai"]),
        # ("risk_command", ["usdt"]),
        # ("market_command", []),
    ]
    
    results = []
    for func_name, args in tests:
        handler_func = getattr(ai_handlers, func_name)
        result = await test_handler(handler_func, args)
        results.append(result)
    
    # Test chat_message with direct message
    result = await test_handler(
        ai_handlers.chat_message,
        message_text="Tell me about Bitcoin",
        chat_type="private"
    )
    results.append(result)
    
    # Test chat_message with group mention
    result = await test_handler(
        ai_handlers.chat_message,
        message_text="@test_bot Tell me about Ethereum",
        chat_type="group"
    )
    results.append(result)
    
    return all(results)

async def check_api_keys():
    """Check for required API keys"""
    print("\033[95m\n===== CHECKING API KEYS =====\033[0m")
    
    api_keys = {
        "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN"),
        "COINGECKO_API_KEY": os.getenv("COINGECKO_API_KEY"),
        "CRYPTOPANIC_API_KEY": os.getenv("CRYPTOPANIC_API_KEY"),
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY"),
        "VENICE_API_KEY": os.getenv("VENICE_API_KEY")
    }
    
    for key, value in api_keys.items():
        status = "✓ Set" if value else "✗ Missing"
        color = "\033[92m" if value else "\033[91m"
        print(f"{color}{status}\033[0m {key}")
    
    # Important keys check
    if not api_keys["TELEGRAM_BOT_TOKEN"]:
        print("\033[91m! TELEGRAM_BOT_TOKEN is required for bot operation\033[0m")
    
    if not api_keys["GEMINI_API_KEY"]:
        print("\033[91m! GEMINI_API_KEY is required for AI functionality\033[0m")
    
    if not api_keys["COINGECKO_API_KEY"]:
        print("\033[93m? COINGECKO_API_KEY is recommended to avoid rate limits\033[0m")

async def main():
    print("\033[1m\033[95m🧪 SNEL TELEGRAM BOT HANDLER TEST 🧪\033[0m")
    
    # Check API keys first
    await check_api_keys()
    
    # Run tests with a delay between each to avoid rate limits
    test_results = {}
    
    print("\n\033[93mRunning handler tests sequentially with delays to avoid rate limits...\033[0m")
    
    # Test each handler group
    test_results["price"] = await test_price_handlers()
    time.sleep(2)  # Delay to avoid rate limits
    
    test_results["info"] = await test_info_handlers()
    time.sleep(2)
    
    test_results["news"] = await test_news_handlers()
    time.sleep(2)
    
    test_results["analysis"] = await test_analysis_handlers()
    time.sleep(2)
    
    test_results["ai"] = await test_ai_handlers()
    
    # Print summary
    print("\n\033[95m===== TEST SUMMARY =====\033[0m")
    for handler_type, result in test_results.items():
        status = "\033[92m✓ PASSED\033[0m" if result else "\033[91m✗ FAILED\033[0m"
        print(f"{handler_type.upper()} Handlers: {status}")
    
    all_passed = all(test_results.values())
    overall = "\033[92mPASSED\033[0m" if all_passed else "\033[91mFAILED\033[0m"
    print(f"\nOverall Test Result: {overall}")
    
    if not all_passed:
        print("\n\033[93mTroubleshooting Tips:\033[0m")
        print("1. Check if API keys are properly set in your .env file")
        print("2. Ensure you have internet connectivity")
        print("3. Some APIs may have rate limits or be temporarily down")
        print("4. Look at specific test errors above for more details")

if __name__ == "__main__":
    asyncio.run(main())