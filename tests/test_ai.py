import asyncio
import os
import json
from dotenv import load_dotenv
from telegram.services.ai_service import AIService
from telegram.services.venice_service import VeniceService
from telegram.services.crypto_service import CryptoService

# Load environment variables
load_dotenv()

# Mock data for testing when APIs are unavailable
MOCK_PRICE_DATA = {
    "current_price": 1.0,
    "market_cap": 42000000000,
    "total_volume": 13000000000,
    "high_24h": 1.01,
    "low_24h": 0.99,
    "price_change_24h": 0.001,
    "price_change_percentage_24h": 0.1,
    "price_change_percentage_7d": 0.05,
    "price_change_percentage_30d": 0.2,
    "circulating_supply": 40000000000,
    "total_supply": 45000000000,
    "max_supply": 50000000000
}

MOCK_INFO_DATA = {
    "id": "usdc",
    "symbol": "usdc",
    "name": "USD Coin",
    "description": {
        "en": "USD Coin is a fully collateralized US dollar stablecoin developed by CENTRE, the open source project."
    },
    "market_data": MOCK_PRICE_DATA,
    "categories": ["stablecoin", "fiat-backed"],
}

async def test_ai_service():
    """Test the AI service integration with Gemini and Venice fallback."""
    print("Testing AI Service...")
    
    try:
        # Initialize services
        venice_service = VeniceService()
        ai_service = AIService(venice_service=venice_service)
        crypto_service = CryptoService()
        
        # Get some sample coin data for context (or use mock data if API fails)
        print("\nGetting sample data for context...")
        try:
            usdc_price_data = await crypto_service.get_detailed_price("usdc")
            if not usdc_price_data or "error" in usdc_price_data:
                print("⚠️ Using mock price data for USDC")
                usdc_price_data = MOCK_PRICE_DATA
                
            usdc_info_data = await crypto_service.get_coin_info("usdc")
            if not usdc_info_data or "error" in usdc_info_data:
                print("⚠️ Using mock info data for USDC")
                usdc_info_data = MOCK_INFO_DATA
                
            usdc_data = {
                "price_data": usdc_price_data,
                "info_data": usdc_info_data
            }
            print("✅ Sample data prepared successfully!")
        except Exception as e:
            print(f"⚠️ Could not get sample data: {e}")
            print("⚠️ Using mock data instead")
            usdc_data = {
                "price_data": MOCK_PRICE_DATA,
                "info_data": MOCK_INFO_DATA
            }
        
        # Test basic response
        print("\n1. Testing basic response...")
        try:
            response = await ai_service.get_response("What are stablecoins?")
            print(f"Response: {response[:300]}...\n")
        except Exception as e:
            print(f"⚠️ Error in basic response test: {e}")
            print("⚠️ AI response test completed with errors\n")
        
        # Test stablecoin analysis
        print("2. Testing stablecoin analysis...")
        try:
            analysis = await ai_service.analyze_stablecoin("usdc", usdc_data)
            print(f"Analysis: {str(analysis)[:300]}...\n")
        except Exception as e:
            print(f"⚠️ Error in stablecoin analysis test: {e}")
            print("⚠️ Analysis test completed with errors\n")
        
        # Test educational content
        print("3. Testing educational content...")
        try:
            education = await ai_service.get_educational_content("depeg risk")
            print(f"Educational content: {education[:300]}...\n")
        except Exception as e:
            print(f"⚠️ Error in educational content test: {e}")
            print("⚠️ Educational content test completed with errors\n")
        
        # Test stablecoin comparison
        print("4. Testing stablecoin comparison...")
        try:
            # Prepare mock data for comparison to avoid API calls
            coins_data = {
                "usdc": usdc_data,
                "usdt": {
                    "price_data": MOCK_PRICE_DATA,
                    "info_data": {**MOCK_INFO_DATA, "id": "usdt", "symbol": "usdt", "name": "Tether"}
                },
                "dai": {
                    "price_data": MOCK_PRICE_DATA,
                    "info_data": {**MOCK_INFO_DATA, "id": "dai", "symbol": "dai", "name": "Dai"}
                }
            }
            comparison = await ai_service.compare_stablecoins(["usdc", "usdt", "dai"], coins_data)
            print(f"Comparison: {comparison[:300]}...\n")
        except Exception as e:
            print(f"⚠️ Error in stablecoin comparison test: {e}")
            print("⚠️ Comparison test completed with errors\n")
        
        print("✅ AI Service tests completed!")
        
    except Exception as e:
        print(f"❌ Error testing AI service: {e}")

async def test_venice_service():
    """Test the Venice service as an AI fallback."""
    print("\nTesting Venice Service...")
    
    try:
        venice_service = VeniceService()
        sample_data = {"price_data": MOCK_PRICE_DATA, "info_data": MOCK_INFO_DATA}
        
        # Check if Venice API is available
        try:
            is_available = await venice_service.is_available()
            print(f"Venice API availability: {'✅ Available' if is_available else '❌ Not available'}")
        except Exception as e:
            print(f"❌ Error checking Venice API availability: {e}")
            is_available = False
        
        if not is_available:
            print("⚠️ Skipping Venice API tests as the service is not available")
            print("✅ Venice Service tests completed (skipped)!")
            return
        
        # Test AI capabilities
        print("\n1. Testing Venice AI response...")
        try:
            response = await venice_service.get_response("What are stablecoins?")
            print(f"Venice AI response: {response[:300]}...\n")
        except Exception as e:
            print(f"⚠️ Error testing Venice AI response: {e}\n")
        
        # Test stablecoin analysis
        print("2. Testing Venice stablecoin analysis...")
        try:
            analysis = await venice_service.analyze_stablecoin("usdc", sample_data)
            print(f"Venice analysis: {str(analysis)[:300]}...\n")
        except Exception as e:
            print(f"⚠️ Error testing Venice analysis: {e}\n")
        
        # Test educational content
        print("3. Testing Venice educational content...")
        try:
            education = await venice_service.get_educational_content("depeg risk")
            print(f"Venice educational content: {education[:300]}...\n")
        except Exception as e:
            print(f"⚠️ Error testing Venice educational content: {e}\n")
        
        print("✅ Venice Service tests completed!")
        
    except Exception as e:
        print(f"❌ Error testing Venice service: {e}")
    finally:
        await venice_service.close()

async def main():
    print("🐌 SNEL Bot - AI Integration Test")
    print("=" * 50)
    
    # Check environment variables
    gemini_key = os.getenv('GEMINI_API_KEY')
    venice_key = os.getenv('VENICE_API_KEY')
    
    print(f"GEMINI_API_KEY: {'✅ Present' if gemini_key else '❌ Missing'}")
    print(f"VENICE_API_KEY: {'✅ Present' if venice_key else '❌ Missing'}")
    print("=" * 50)
    
    if not gemini_key and not venice_key:
        print("⚠️ Both GEMINI_API_KEY and VENICE_API_KEY are missing. The bot will use fallback responses.")
    elif not gemini_key:
        print("⚠️ GEMINI_API_KEY is missing. Venice will be used as the primary AI service.")
    elif not venice_key:
        print("⚠️ VENICE_API_KEY is missing. Gemini will be used without fallback.")
    
    await test_ai_service()
    await test_venice_service()

if __name__ == "__main__":
    asyncio.run(main())