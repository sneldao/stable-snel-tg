import os
import json
import httpx
from typing import Dict, List, Optional, Any

class VeniceService:
    """Service for interacting with Venice AI as an alternative to Gemini."""
    
    def __init__(self):
        """Initialize the Venice Service."""
        self.api_key = os.getenv('VENICE_API_KEY')
        if not self.api_key:
            print("Warning: No Venice API key provided. Will fall back to Gemini AI.")
        
        self.base_url = "https://api.venice.ai/v1"  # Replace with actual Venice API URL
        self.session = httpx.AsyncClient(timeout=30.0)
        
    async def close(self):
        """Close the HTTP session."""
        await self.session.aclose()
        
    async def _make_request(self, endpoint: str, method: str = "POST", data: Dict = None) -> Dict:
        """Make a request to the Venice AI API."""
        if not self.api_key:
            return {"error": "No Venice API key configured"}
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = await self.session.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "details": e.response.text}
        except httpx.RequestError as e:
            return {"error": f"Request error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
            
    async def get_response(self, query: str, context: Optional[List[Dict]] = None) -> str:
        """Get an AI response using Venice API."""
        # Enhance query with brevity instructions and snail persona
        enhanced_query = f"As SNEL the crypto snail, answer this query EXTREMELY BRIEFLY - ONE paragraph maximum (30-50 words). Add ONE quick snail reference. Query: {query}"
        
        data = {
            "message": enhanced_query,
            "context": context or []
        }
        
        result = await self._make_request("chat/completions", data=data)
        
        if "error" in result:
            return f"I couldn't process your request through Venice AI: {result.get('error')}"
        
        return result.get("response", "No response received from Venice AI")
    
    async def analyze_stablecoin(self, coin_id: str, context_data: Dict) -> Dict:
        """Analyze a stablecoin using Venice AI."""
        prompt = f"""
As SNEL the crypto snail, analyze {coin_id} stablecoin BRIEFLY based on this data:
{json.dumps(context_data, indent=2)}

Provide a VERY CONCISE analysis covering ONLY:
1. Stability mechanism (1 sentence)
2. Risk factors (1 sentence)
3. ONE snail reference or metaphor

EXTREME BREVITY REQUIRED - 50 words absolute maximum.
Format your analysis as a structured response.
"""
        data = {
            "message": prompt,
            "options": {
                "structured_response": True
            }
        }
        
        result = await self._make_request("analyze/stablecoin", data=data)
        
        if "error" in result:
            return {"error": result.get("error")}
        
        return result.get("analysis", {"error": "No analysis received"})
    
    async def get_educational_content(self, topic: str) -> str:
        """Get educational content about a stablecoin-related topic."""
        prompt = f"As SNEL the crypto snail, explain {topic} in ONE short paragraph only. Include ONE brief snail reference. EXTREME BREVITY REQUIRED - 40 words maximum."
        
        data = {
            "topic": topic,
            "prompt": prompt,
            "options": {
                "max_length": 200,
                "format": "markdown"
            }
        }
        
        result = await self._make_request("education", data=data)
        
        if "error" in result:
            return f"I couldn't retrieve educational content about {topic} through Venice AI."
        
        return result.get("content", f"No educational content received for {topic}")
    
    async def compare_stablecoins(self, coin_ids: List[str], context_data: Optional[Dict] = None) -> str:
        """Compare multiple stablecoins using Venice AI."""
        prompt = f"""
As SNEL the crypto snail, compare these stablecoins VERY BRIEFLY: {', '.join(coin_ids)}

Provide ONLY 2-3 key differences total. Add ONE snail reference.
ULTRA BRIEF - 40 words maximum.

Present as a concise markdown comparison.
"""
        data = {
            "message": prompt,
            "options": {
                "format": "markdown"
            }
        }
        
        result = await self._make_request("compare/stablecoins", data=data)
        
        if "error" in result:
            return f"I couldn't complete the comparison through Venice AI."
        
        return result.get("comparison", "No comparison received")
    
    async def is_available(self) -> bool:
        """Check if the Venice AI service is available."""
        try:
            result = await self._make_request("ping")
            return not "error" in result
        except Exception:
            return False