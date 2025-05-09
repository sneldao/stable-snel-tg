import asyncio
from pycoingecko import CoinGeckoAPI
import time

async def test_get_price():
    print("Testing basic price fetch...")
    try:
        cg = CoinGeckoAPI()
        # Test with Bitcoin
        print("Fetching Bitcoin price...")
        data = cg.get_price(ids='bitcoin', vs_currencies='usd', include_market_cap=True, include_24hr_vol=True)
        print(f"Bitcoin data: {data}")
        
        # Test with a stablecoin
        print("\nFetching USDC price...")
        data = cg.get_price(ids='usd-coin', vs_currencies='usd', include_market_cap=True, include_24hr_vol=True)
        print(f"USDC data: {data}")
        
        return True
    except Exception as e:
        print(f"Error in test_get_price: {e}")
        return False

async def test_get_detailed_price():
    print("\nTesting detailed price information...")
    try:
        cg = CoinGeckoAPI()
        # Test with Bitcoin
        print("Fetching detailed Bitcoin info...")
        data = cg.get_coin_by_id(id='bitcoin')
        market_data = data.get('market_data', {})
        
        print(f"Bitcoin current price: ${market_data.get('current_price', {}).get('usd', 0):,.2f}")
        print(f"Bitcoin market cap: ${market_data.get('market_cap', {}).get('usd', 0):,.2f}")
        print(f"Bitcoin 24h change: {market_data.get('price_change_percentage_24h', 0):+.2f}%")
        
        return True
    except Exception as e:
        print(f"Error in test_get_detailed_price: {e}")
        return False

async def test_get_top_coins():
    print("\nTesting top coins fetch...")
    try:
        cg = CoinGeckoAPI()
        print("Fetching top 5 coins...")
        coins = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=5, page=1)
        
        for i, coin in enumerate(coins, 1):
            print(f"{i}. {coin['name']} (${coin['current_price']:,.2f}) - 24h: {coin.get('price_change_percentage_24h', 0):+.2f}%")
        
        return True
    except Exception as e:
        print(f"Error in test_get_top_coins: {e}")
        return False

async def test_api_rate_limits():
    print("\nTesting API rate limits...")
    try:
        cg = CoinGeckoAPI()
        # Make multiple requests in quick succession
        for i in range(1, 6):
            print(f"Request {i}...")
            cg.get_price(ids='bitcoin', vs_currencies='usd')
            time.sleep(1)  # Small delay to avoid hammering the API
        
        print("Rate limit test passed!")
        return True
    except Exception as e:
        print(f"Error in test_api_rate_limits: {e}")
        return False

async def main():
    print("=== CoinGecko API Test ===")
    
    # Run tests
    tests = [
        test_get_price(),
        test_get_detailed_price(),
        test_get_top_coins(),
        test_api_rate_limits()
    ]
    
    results = await asyncio.gather(*tests)
    
    # Summary
    print("\n=== Test Summary ===")
    all_passed = all(results)
    print(f"Tests passed: {sum(results)}/{len(results)}")
    print(f"Overall status: {'SUCCESS' if all_passed else 'FAILURE'}")
    
    if not all_passed:
        print("\nSuggestions:")
        print("1. Check your internet connection")
        print("2. The CoinGecko API may be rate-limited (free tier has limitations)")
        print("3. The API might be experiencing downtime")
        print("4. Consider adding API key handling for premium access")

if __name__ == "__main__":
    asyncio.run(main())