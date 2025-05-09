import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

class TestAIServices:
    async def test_gemini_api(self):
        """Test if Gemini API is working correctly"""
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("❌ GEMINI_API_KEY is not set in environment variables")
            return False
            
        print(f"✓ GEMINI_API_KEY found (starts with: {api_key[:5]}...)")
        
        try:
            # Configure the Gemini API
            genai.configure(api_key=api_key)
            
            # Try both model versions
            models_to_try = ['gemini-1.5-pro', 'gemini-1.0-pro']
            
            for model_name in models_to_try:
                try:
                    print(f"Testing {model_name}...")
                    model = genai.GenerativeModel(model_name)
                    
                    # Simple test query
                    response = model.generate_content("Hello, respond with a very short greeting")
                    
                    print(f"✓ {model_name} response: {response.text}")
                    return True
                except Exception as e:
                    print(f"❌ Error with {model_name}: {str(e)}")
            
            print("❌ All Gemini models failed")
            return False
            
        except Exception as e:
            print(f"❌ Failed to configure Gemini API: {str(e)}")
            return False
    
    async def test_venice_api(self):
        """Test if Venice API is working correctly"""
        api_key = os.getenv('VENICE_API_KEY')
        
        if not api_key:
            print("❌ VENICE_API_KEY is not set in environment variables")
            return False
            
        print(f"✓ VENICE_API_KEY found (starts with: {api_key[:5]}...)")
        
        try:
            import requests
            
            # Test fetching models list
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get("https://api.venice.ai/api/v1/models", headers=headers)
            
            if response.status_code == 200:
                print(f"✓ Venice API models list: {response.json()['data'][0]['id']}")
                
                # Test simple chat completion
                url = "https://api.venice.ai/api/v1/chat/completions"
                data = {
                    "model": "llama-3.2-3b",
                    "messages": [{"role": "user", "content": "Hello, respond with a very short greeting"}],
                    "temperature": 0.7
                }
                
                response = requests.post(url, json=data, headers=headers)
                if response.status_code == 200:
                    content = response.json()['choices'][0]['message']['content']
                    print(f"✓ Venice API chat response: {content}")
                    return True
                else:
                    print(f"❌ Venice API chat completion failed: {response.status_code} - {response.text}")
                    return False
            else:
                print(f"❌ Venice API models list request failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Failed to test Venice API: {str(e)}")
            return False
    
    async def test_environment(self):
        """Test general environment setup"""
        print("\n==== Environment Variables ====")
        for var in ['TELEGRAM_BOT_TOKEN', 'GEMINI_API_KEY', 'VENICE_API_KEY', 'LOG_LEVEL']:
            value = os.getenv(var)
            if value:
                if var.endswith('_KEY') or var.endswith('_TOKEN'):
                    print(f"✓ {var} is set (starts with: {value[:5]}...)")
                else:
                    print(f"✓ {var} is set to: {value}")
            else:
                print(f"❌ {var} is not set")
    
    async def run_all_tests(self):
        """Run all tests"""
        print("\n==== Testing Environment ====")
        await self.test_environment()
        
        print("\n==== Testing Gemini API ====")
        gemini_result = await self.test_gemini_api()
        
        print("\n==== Testing Venice API ====")
        venice_result = await self.test_venice_api()
        
        print("\n==== Test Summary ====")
        print(f"Gemini API: {'✓ Working' if gemini_result else '❌ Failed'}")
        print(f"Venice API: {'✓ Working' if venice_result else '❌ Failed'}")
        
        if gemini_result and venice_result:
            print("\n✅ All API tests passed. If the bot is still not responding to AI commands, check the code integration.")
        else:
            print("\n❌ Some API tests failed. Fix the issues above to get AI functionality working.")

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Run the tests
    tester = TestAIServices()
    asyncio.run(tester.run_all_tests())