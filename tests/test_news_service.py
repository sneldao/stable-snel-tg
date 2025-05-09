import asyncio
from typing import Dict, List
import os
from dotenv import load_dotenv
from telegram.services.news_service import NewsService

# Load environment variables
load_dotenv()

async def test_get_coin_news():
    """Test fetching news for a coin."""
    print("\n=== Testing get_coin_news ===")
    try:
        news_service = NewsService()
        
        # Test Bitcoin news
        print("Fetching news for Bitcoin...")
        btc_news = await news_service.get_coin_news("bitcoin", limit=3)
        
        if btc_news:
            print(f"✅ Successfully retrieved {len(btc_news)} news articles")
            for i, article in enumerate(btc_news, 1):
                print(f"\n{i}. {article.get('title')}")
                print(f"   Source: {article.get('source')}")
                print(f"   Published: {article.get('published_at')}")
        else:
            print("❌ Failed to retrieve news articles")
            
        # Test stablecoin news
        print("\nFetching news for USDC...")
        usdc_news = await news_service.get_coin_news("usd-coin", limit=2)
        
        if usdc_news:
            print(f"✅ Successfully retrieved {len(usdc_news)} news articles")
            for i, article in enumerate(usdc_news, 1):
                print(f"\n{i}. {article.get('title')}")
                print(f"   Source: {article.get('source')}")
        else:
            print("❌ Failed to retrieve news or no recent articles found")
            
        return True
    except Exception as e:
        print(f"❌ Error in test_get_coin_news: {e}")
        return False

async def test_get_social_media():
    """Test fetching social media links for a coin."""
    print("\n=== Testing get_social_media ===")
    try:
        news_service = NewsService()
        
        # Test Bitcoin social media
        print("Fetching social media links for Bitcoin...")
        btc_social = await news_service.get_social_media("bitcoin")
        
        if btc_social:
            print("✅ Successfully retrieved social media links")
            print(f"Twitter: {btc_social.get('twitter_screen_name')}")
            print(f"Reddit: {btc_social.get('subreddit_url')}")
            print(f"Telegram: {btc_social.get('telegram_channel_identifier')}")
            if btc_social.get('chat_url'):
                print(f"Chat URL: {btc_social.get('chat_url')[0] if btc_social.get('chat_url') else 'N/A'}")
        else:
            print("❌ Failed to retrieve social media links")
            
        return True
    except Exception as e:
        print(f"❌ Error in test_get_social_media: {e}")
        return False

async def test_get_events():
    """Test fetching upcoming events for a coin."""
    print("\n=== Testing get_events ===")
    try:
        news_service = NewsService()
        
        # Test Bitcoin events
        print("Fetching events for Bitcoin...")
        btc_events = await news_service.get_events("bitcoin")
        
        if btc_events:
            print(f"✅ Successfully retrieved {len(btc_events)} events")
            for i, event in enumerate(btc_events[:3], 1):
                print(f"\n{i}. {event.get('title')}")
                print(f"   Date: {event.get('date')}")
                print(f"   Type: {event.get('type')}")
        else:
            print("❌ No upcoming events found or failed to retrieve events")
            
        return True
    except Exception as e:
        print(f"❌ Error in test_get_events: {e}")
        return False

async def check_api_keys():
    """Check for required API keys."""
    print("\n=== Checking Required API Keys ===")
    
    # Check for CoinGecko API Key
    coingecko_api_key = os.getenv('COINGECKO_API_KEY')
    if coingecko_api_key:
        print("✅ COINGECKO_API_KEY is set")
    else:
        print("❓ COINGECKO_API_KEY is not set - may be using free tier with rate limits")
    
    # Check for CryptoPanic API Key
    cryptopanic_api_key = os.getenv('CRYPTOPANIC_API_KEY')
    if cryptopanic_api_key:
        print("✅ CRYPTOPANIC_API_KEY is set")
    else:
        print("⚠️ CRYPTOPANIC_API_KEY is not set - news functionality may be limited")
    
    # Other potential API keys
    news_api_key = os.getenv('NEWS_API_KEY')
    if news_api_key:
        print("✅ NEWS_API_KEY is set")
    else:
        print("ℹ️ NEWS_API_KEY is not set (may not be required)")

async def main():
    print("🔍 Testing NewsService Functionality")
    
    # First check API keys
    await check_api_keys()
    
    # Run all tests
    tests = [
        test_get_coin_news(),
        test_get_social_media(),
        test_get_events()
    ]
    
    results = await asyncio.gather(*tests)
    
    # Summary
    success_count = sum(1 for r in results if r)
    print(f"\n=== Test Summary: {success_count}/{len(tests)} tests passed ===")
    
    if success_count < len(tests):
        print("\nTroubleshooting Tips:")
        print("1. Check if you need a CryptoPanic API key for better news results")
        print("2. CoinGecko free tier has rate limits - consider adding COINGECKO_API_KEY")
        print("3. Some APIs might be experiencing downtime")
        print("4. Update your .env file with required API keys")
        print("\nRecommended .env entries:")
        print("COINGECKO_API_KEY=your_key_here")
        print("CRYPTOPANIC_API_KEY=your_key_here")

if __name__ == "__main__":
    asyncio.run(main())