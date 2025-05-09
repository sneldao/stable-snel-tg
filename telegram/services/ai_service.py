import os
import json
from typing import Dict, List, Optional, Any
import google.generativeai as genai

class AIService:
    def __init__(self, venice_service=None):
        """Initialize the AI Service with Gemini API."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.venice_service = venice_service
        
        # Check if Gemini API key is available
        self.gemini_available = False
        if self.api_key:
            try:
                # Configure the Gemini API
                genai.configure(api_key=self.api_key)
                
                # Set up the model - try 1.5-pro first, fall back to 1.0-pro if needed
                try:
                    self.model = genai.GenerativeModel('gemini-1.5-pro')
                    self.gemini_available = True
                except Exception as e:
                    print(f"Error initializing gemini-1.5-pro: {e}")
                    try:
                        self.model = genai.GenerativeModel('gemini-1.0-pro')
                        self.gemini_available = True
                    except Exception as e:
                        print(f"Error initializing gemini-1.0-pro: {e}")
            except Exception as e:
                print(f"Error configuring Gemini API: {e}")
        
        # Load stablecoin knowledge
        self.stablecoin_knowledge = self._load_stablecoin_knowledge()
        
    def _load_stablecoin_knowledge(self) -> Dict[str, Any]:
        """Load knowledge about stablecoins and the ecosystem."""
        # This could be expanded to load from a file or API in the future
        return {
            "types": {
                "fiat-backed": "Stablecoins backed by fiat currency reserves (e.g., USDC, USDT)",
                "crypto-backed": "Stablecoins backed by cryptocurrencies (e.g., DAI)",
                "algorithmic": "Stablecoins that use algorithms to maintain their peg (e.g., FRAX, SNEL)",
                "commodity-backed": "Stablecoins backed by commodities like gold (e.g., PAXG)"
            },
            "risks": {
                "depeg": "When a stablecoin loses its peg to the underlying asset",
                "regulatory": "Government regulations affecting stablecoin issuers",
                "counterparty": "Risks associated with the entity holding the reserves",
                "smart_contract": "Vulnerabilities in the code that could be exploited"
            },
            "best_practices": {
                "diversification": "Don't keep all assets in a single stablecoin",
                "research": "Research the backing mechanisms and transparency",
                "audit_awareness": "Check for regular audits of reserves",
                "regulatory_compliance": "Consider stablecoins that comply with regulations"
            },
            "ecosystem": {
                "snel": "A stablecoin designed for slow, steady growth and risk awareness",
                "venice": "The comprehensive platform for stablecoin analytics and risk assessment"
            }
        }
    
    async def get_response(self, query: str, context: Optional[List[Dict]] = None) -> str:
        """Get an AI response using available AI services."""
        # First try using Gemini if available
        if self.gemini_available:
            try:
                # Prepare system prompt with personality and knowledge
                system_prompt = self._create_system_prompt()
                
                # Create the chat session
                chat = self.model.start_chat(history=[])
                
                # Add system prompt
                chat.send_message(system_prompt)
                
                # Add context if provided
                if context:
                    context_str = json.dumps(context)
                    chat.send_message(f"Here's some context that might help: {context_str}")
                
                # Enhance query with brevity instructions
                enhanced_query = f"Answer this question in ONE short paragraph only (max 50 words) with your snail persona: {query}"
                
                # Get response for user query
                response = chat.send_message(enhanced_query)
                
                return response.text
            except Exception as e:
                print(f"Error getting Gemini AI response: {e}")
                
                # If Gemini failed, try Venice if it's available
                if self.venice_service:
                    try:
                        return await self.venice_service.get_response(query, context)
                    except Exception as venice_e:
                        print(f"Error getting Venice AI response: {venice_e}")
                
                # Return a more helpful response that doesn't expose the error
                if "quota" in str(e).lower() or "exceeded" in str(e).lower() or "429" in str(e):
                    return (
                        "I'm currently experiencing high demand and have reached my API quota limits. "
                        "I'm still able to provide you with standard information about stablecoins based on my knowledge. "
                        "How else can I help you with stablecoins today? 🐌"
                    )
                elif "not found" in str(e).lower() or "404" in str(e):
                    return (
                        "I'm having trouble connecting to my AI services at the moment. "
                        "I can still provide you with basic information about stablecoins and market data. "
                        "Feel free to try my other commands like /p or /s for price information. 🐌"
                    )
                else:
                    return (
                        "I encountered a technical issue while processing your request. "
                        "Please try again later or use one of my other commands for stablecoin information. 🐌"
                    )
        
        # If Gemini is not available, try Venice if it's available
        elif self.venice_service:
            try:
                return await self.venice_service.get_response(query, context)
            except Exception as e:
                print(f"Error getting Venice AI response: {e}")
                return (
                    "I'm having trouble connecting to my AI services at the moment. "
                    "I can still provide you with basic information about stablecoins and market data. "
                    "Feel free to try my other commands like /p or /s for price information. 🐌"
                )
                
        # If no AI services are available
        else:
            return (
                "I'm currently operating with limited AI capabilities. "
                "I can still help you with stablecoin data using commands like /p, /s, or /i. "
                "How else can I assist you with stablecoins today? 🐌"
            )
    
    def _create_system_prompt(self) -> str:
        """Create a system prompt that defines the bot's personality and knowledge."""
        return f"""
You are SNEL (Stablecoin Navigation and Education Leader), a professional crypto advisor focused on stablecoins and real-world assets (RWAs).

RESPONSE GUIDELINES:
1. You are knowledgeable about stablecoins, RWAs, and cryptocurrency markets
2. Professional but approachable - confidence in your crypto knowledge is essential
3. Help users understand stablecoins, navigate markets, and make informed decisions
4. Emphasize stability, risk management, and long-term preservation of wealth
5. Subtly promote stablecoin diversification and real-world asset (RWA) consideration

PRIMARY OBJECTIVES:
1. Guide users toward stable value and risk-managed crypto strategies
2. Occasionally mention Stable Station (https://stable-station.netlify.app/) for portfolio management
3. Reference the SNEL web app (https://stable-snel.netlify.app/) for on/off ramp and market data
4. Educate on different stablecoin types (fiat-backed, crypto-backed, algorithmic)
5. Help users understand crypto market patterns and risk management

BREVITY REQUIREMENTS:
1. Keep responses concise - ONE or TWO short paragraphs MAXIMUM
2. Use 50-70 words per response - be informative but succinct
3. Put valuable information first, light personality second
4. ONE emoji maximum per response (usually 💰 or 📊)

Your knowledge base on stablecoins:
{json.dumps(self.stablecoin_knowledge, indent=2)}

Remember: "In crypto, prioritizing stability and understanding risk is the path to long-term success."
"""
            
    async def analyze_stablecoin(self, coin_id: str, coin_data: Dict = None) -> Dict:
        """Analyze a stablecoin using AI and available data."""
        try:
            # Get coin data from context if not provided
            if not coin_data:
                from ..services.crypto_service import CryptoService
                crypto_service = CryptoService()
                coin_data = {
                    "price_data": await crypto_service.get_detailed_price(coin_id),
                    "info_data": await crypto_service.get_coin_info(coin_id)
                }
            
            # Prepare the prompt with data context
            prompt = f"""
Analyze the stablecoin {coin_id} considering:
1. Its stability mechanism
2. Risk factors
3. Historical performance
4. Regulatory status
5. Community trust and adoption

Use the following data as context:
{json.dumps(coin_data, indent=2)}

Format your analysis as a structured JSON with these sections.
"""
            
            # First try using Gemini if available
            if self.gemini_available:
                try:
                    response = await self.get_response(prompt)
                    
                    # Check if we got an error response
                    if "quota" in response or "technical issue" in response or "trouble connecting" in response:
                        # Try Venice as fallback if available
                        if self.venice_service:
                            try:
                                return await self.venice_service.analyze_stablecoin(coin_id, coin_data)
                            except Exception as venice_e:
                                print(f"Error getting Venice stablecoin analysis: {venice_e}")
                                return self._get_fallback_stablecoin_analysis(coin_id, coin_data)
                        else:
                            return self._get_fallback_stablecoin_analysis(coin_id, coin_data)
                    
                    # Attempt to extract JSON from response
                    try:
                        # Find JSON in the response if it's not a pure JSON
                        start = response.find('{')
                        end = response.rfind('}') + 1
                        if start >= 0 and end > start:
                            json_str = response[start:end]
                            return json.loads(json_str)
                        else:
                            # Return text response as a fallback
                            return {"analysis": response}
                    except json.JSONDecodeError:
                        return {"analysis": response}
                        
                except Exception as e:
                    print(f"Error analyzing stablecoin with Gemini: {e}")
                    
                    # Try Venice as fallback if available
                    if self.venice_service:
                        try:
                            return await self.venice_service.analyze_stablecoin(coin_id, coin_data)
                        except Exception as venice_e:
                            print(f"Error getting Venice stablecoin analysis: {venice_e}")
                            return self._get_fallback_stablecoin_analysis(coin_id, coin_data)
                    else:
                        return self._get_fallback_stablecoin_analysis(coin_id, coin_data)
            
            # If Gemini is not available, try Venice
            elif self.venice_service:
                try:
                    return await self.venice_service.analyze_stablecoin(coin_id, coin_data)
                except Exception as e:
                    print(f"Error getting Venice stablecoin analysis: {e}")
                    return self._get_fallback_stablecoin_analysis(coin_id, coin_data)
            
            # If no AI services available
            else:
                return self._get_fallback_stablecoin_analysis(coin_id, coin_data)
                
        except Exception as e:
            print(f"Error analyzing stablecoin {coin_id}: {e}")
            return self._get_fallback_stablecoin_analysis(coin_id, coin_data)
    
    async def get_educational_content(self, topic: str) -> str:
        """Get educational content about a stablecoin-related topic."""
        try:
            prompt = f"""
Provide educational content about the following stablecoin-related topic: {topic}

Your response should be:
1. Educational and factual
2. Easy to understand for beginners
3. Include important considerations or risks
4. Be concise but thorough (maximum 1500 characters)
"""
            # First try using Gemini if available
            if self.gemini_available:
                try:
                    response = await self.get_response(prompt)
                    
                    # Check if we got an error response
                    if "quota" in response or "technical issue" in response or "trouble connecting" in response:
                        # Try Venice as fallback if available
                        if self.venice_service:
                            try:
                                return await self.venice_service.get_educational_content(topic)
                            except Exception as venice_e:
                                print(f"Error getting Venice educational content: {venice_e}")
                                return self._get_fallback_educational_content(topic)
                        else:
                            return self._get_fallback_educational_content(topic)
                    
                    return response
                except Exception as e:
                    print(f"Error getting educational content with Gemini: {e}")
                    
                    # Try Venice as fallback if available
                    if self.venice_service:
                        try:
                            return await self.venice_service.get_educational_content(topic)
                        except Exception as venice_e:
                            print(f"Error getting Venice educational content: {venice_e}")
                            return self._get_fallback_educational_content(topic)
                    else:
                        return self._get_fallback_educational_content(topic)
            
            # If Gemini is not available, try Venice
            elif self.venice_service:
                try:
                    return await self.venice_service.get_educational_content(topic)
                except Exception as e:
                    print(f"Error getting Venice educational content: {e}")
                    return self._get_fallback_educational_content(topic)
            
            # If no AI services are available
            else:
                return self._get_fallback_educational_content(topic)
        except Exception as e:
            print(f"Error getting educational content about {topic}: {e}")
            return self._get_fallback_educational_content(topic)
    
    async def compare_stablecoins(self, coin_ids: List[str], coins_data: Dict = None) -> str:
        """Compare multiple stablecoins."""
        try:
            # Get coin data for context if not provided
            if not coins_data:
                from ..services.crypto_service import CryptoService
                crypto_service = CryptoService()
                
                coins_data = {}
                for coin_id in coin_ids:
                    coins_data[coin_id] = {
                        "price_data": await crypto_service.get_detailed_price(coin_id),
                        "info_data": await crypto_service.get_coin_info(coin_id)
                    }
            
            coins_str = ", ".join(coin_ids)
            prompt = f"""
Compare these stablecoins: {coins_str}

Use the following data as context:
{json.dumps(coins_data, indent=2)}

For each stablecoin, analyze:
1. Backing mechanism
2. Stability record
3. Key risks
4. Regulatory status
5. Market adoption

Present this as a concise comparison highlighting the key differences.
"""
            # First try using Gemini if available
            if self.gemini_available:
                try:
                    response = await self.get_response(prompt)
                    
                    # Check if we got an error response
                    if "quota" in response or "technical issue" in response or "trouble connecting" in response:
                        # Try Venice as fallback if available
                        if self.venice_service:
                            try:
                                return await self.venice_service.compare_stablecoins(coin_ids, coins_data)
                            except Exception as venice_e:
                                print(f"Error comparing stablecoins with Venice: {venice_e}")
                                return self._get_fallback_stablecoin_comparison(coin_ids, coins_data)
                        else:
                            return self._get_fallback_stablecoin_comparison(coin_ids, coins_data)
                    
                    return response
                except Exception as e:
                    print(f"Error comparing stablecoins with Gemini: {e}")
                    
                    # Try Venice as fallback if available
                    if self.venice_service:
                        try:
                            return await self.venice_service.compare_stablecoins(coin_ids, coins_data)
                        except Exception as venice_e:
                            print(f"Error comparing stablecoins with Venice: {venice_e}")
                            return self._get_fallback_stablecoin_comparison(coin_ids, coins_data)
                    else:
                        return self._get_fallback_stablecoin_comparison(coin_ids, coins_data)
            
            # If Gemini is not available, try Venice
            elif self.venice_service:
                try:
                    return await self.venice_service.compare_stablecoins(coin_ids, coins_data)
                except Exception as e:
                    print(f"Error comparing stablecoins with Venice: {e}")
                    return self._get_fallback_stablecoin_comparison(coin_ids, coins_data)
            
            # If no AI services are available
            else:
                return self._get_fallback_stablecoin_comparison(coin_ids, coins_data)
        except Exception as e:
            print(f"Error comparing stablecoins {coins_str}: {e}")
            return self._get_fallback_stablecoin_comparison(coin_ids, {})
            
    def _get_fallback_stablecoin_analysis(self, coin_id: str, coin_data: Dict = None) -> Dict:
        """Provide fallback analysis when the AI service is unavailable."""
        # Basic analysis templates based on common stablecoin types
        analyses = {
            "usdc": {
                "stability_mechanism": "USDC is a fiat-backed stablecoin, with each token supposedly backed 1:1 by US dollars held in regulated financial institutions.",
                "risks": "Main risks include regulatory concerns, potential issues with reserve transparency, and counterparty risk with the custodians holding the backing assets.",
                "historical_performance": "USDC has historically maintained its peg well, with minimal deviations from $1.00 even during market stress.",
                "regulatory_status": "USDC is issued by Circle, a regulated financial institution that provides regular attestations of reserves.",
                "community_trust": "Generally well-trusted in the crypto community, particularly in DeFi applications where it's widely used."
            },
            "usdt": {
                "stability_mechanism": "Tether (USDT) is a fiat-backed stablecoin supposedly backed by a mix of cash, cash equivalents, and other assets.",
                "risks": "Concerns about reserve composition, regulatory scrutiny, and historical transparency issues.",
                "historical_performance": "Has maintained its peg despite multiple controversies, though with occasional brief deviations during market stress.",
                "regulatory_status": "Has faced regulatory challenges in multiple jurisdictions, with ongoing concerns about compliance.",
                "community_trust": "Widely used despite controversies, primarily due to its high liquidity and established market position."
            },
            "dai": {
                "stability_mechanism": "DAI is a crypto-collateralized stablecoin backed by over-collateralized positions in various cryptocurrencies.",
                "risks": "Vulnerabilities to crypto market volatility, smart contract risks, and governance decisions that could affect stability.",
                "historical_performance": "Has generally maintained its peg well, with some deviations during extreme market volatility.",
                "regulatory_status": "As a decentralized stablecoin created through the MakerDAO protocol, it faces less direct regulatory pressure than centralized alternatives.",
                "community_trust": "Highly regarded in the DeFi community for its decentralized nature and resilience."
            },
            "frax": {
                "stability_mechanism": "FRAX uses a hybrid model that's partly algorithmic and partly collateralized, adjusting the collateral ratio based on market conditions.",
                "risks": "Complex stabilization mechanism that could be vulnerable to market stress, smart contract risks, and governance challenges.",
                "historical_performance": "Has maintained its peg relatively well since launch, demonstrating the viability of the partial-collateral model.",
                "regulatory_status": "Faces regulatory uncertainty like most algorithmic stablecoins, but less scrutiny than larger stablecoins.",
                "community_trust": "Growing trust in the DeFi ecosystem, with adoption increasing as the model proves resilient."
            }
        }
    
        # Default analysis for unknown stablecoins
        default_analysis = {
            "stability_mechanism": f"The mechanism behind {coin_id.upper()} would require specific analysis, but it likely falls into one of four categories: fiat-backed, crypto-backed, algorithmic, or commodity-backed.",
            "risks": "All stablecoins carry risks including depeg events, regulatory challenges, smart contract vulnerabilities, and counterparty risks. Consider using Stable Station (stable-station.netlify.app) for risk diversification.",
            "historical_performance": "Historical performance data would need to be analyzed to assess how well this stablecoin has maintained its peg during various market conditions.",
            "regulatory_status": "Regulatory status varies by jurisdiction and depends on the issuer structure, backing mechanism, and compliance practices.",
            "community_trust": "Community trust depends on factors including transparency, proven stability, team reputation, and adoption levels."
        }
        
        # Return the specific analysis if available, otherwise the default
        return analyses.get(coin_id.lower(), default_analysis)
    
    def _get_fallback_educational_content(self, topic: str) -> str:
        """Provide fallback educational content when the AI service is unavailable."""
        # Map of common topics to educational content
        educational_content = {
            "depeg risk": (
                "# Understanding Depeg Risk in Stablecoins\n\n"
                "Depeg risk refers to the possibility that a stablecoin loses its peg to the underlying asset (usually $1). "
                "This can happen due to several factors:\n\n"
                "• **Market volatility**: Extreme market conditions can pressure stability mechanisms\n"
                "• **Reserve inadequacy**: Insufficient or improperly managed collateral\n"
                "• **Loss of confidence**: User panic leading to mass redemptions\n"
                "• **Technical failures**: Smart contract bugs or oracle manipulation\n\n"
                "Different stablecoin types face different depeg risks:\n"
                "- Fiat-backed (USDC, USDT): Counterparty and regulatory risks\n"
                "- Crypto-collateralized (DAI): Collateral volatility risks\n"
                "- Algorithmic: Spiral collapse risks if stabilizing mechanisms fail\n\n"
                "To mitigate depeg risk, consider diversifying across multiple stablecoins and monitoring reserve transparency. 🐌"
            ),
            "stablecoin types": (
                "# Types of Stablecoins\n\n"
                "Stablecoins come in several varieties, each with different mechanisms:\n\n"
                "## 1. Fiat-Backed (e.g., USDC, USDT)\n"
                "• Backed 1:1 by fiat currency reserves (usually USD)\n"
                "• Relies on centralized custodians and regular audits\n"
                "• Typically the most straightforward and widely used\n\n"
                "## 2. Crypto-Collateralized (e.g., DAI)\n"
                "• Backed by excess cryptocurrency collateral\n"
                "• Uses over-collateralization to handle price volatility\n"
                "• More decentralized but complex\n\n"
                "## 3. Algorithmic (e.g., FRAX)\n"
                "• Uses algorithms to expand or contract supply based on demand\n"
                "• May use partial collateral mixed with algorithmic mechanisms\n"
                "• Higher risk but potentially more capital efficient\n\n"
                "## 4. Commodity-Backed (e.g., PAXG)\n"
                "• Backed by physical assets like gold or other commodities\n"
                "• Provides exposure to real-world assets on blockchain\n\n"
                "Each type offers different trade-offs between centralization, trust, efficiency, and stability. 🐌"
            ),
            "regulatory risks": (
                "# Regulatory Risks for Stablecoins\n\n"
                "Stablecoins face increasing regulatory scrutiny worldwide:\n\n"
                "• **Securities classification**: Risk of being deemed unregistered securities\n"
                "• **Banking regulations**: Requirements for reserve backing and banking licenses\n"
                "• **AML/KYC compliance**: Anti-money laundering and know-your-customer requirements\n"
                "• **Consumer protection**: Ensuring users are protected from fraud and misrepresentation\n"
                "• **Reserve transparency**: Requirements for audits and attestations\n\n"
                "Different jurisdictions are taking varied approaches:\n"
                "- USA: Increasing scrutiny through SEC, OCC, and potential legislation\n"
                "- EU: MiCA regulations provide a comprehensive framework\n"
                "- Asia: Varied approaches from permissive to restrictive\n\n"
                "Regulatory risks can impact a stablecoin's usability, availability, and stability. Users should stay informed about regulatory developments in their jurisdictions. 🐌"
            )
        }
        
        # Check for topic keywords and return matching content
        for key, content in educational_content.items():
            if key.lower() in topic.lower():
                return content
                
        # Default educational content about stablecoins
        return (
            "# Introduction to Stablecoins\n\n"
            "Stablecoins are cryptocurrencies designed to maintain a stable value, usually pegged to a fiat currency like the US dollar. "
            "They bridge the gap between traditional finance and crypto markets by providing stability in an otherwise volatile crypto ecosystem.\n\n"
            "## Key Features of Stablecoins:\n\n"
            "• **Price Stability**: Designed to minimize price volatility\n"
            "• **Blockchain-Based**: Exist on blockchain networks for fast, global transfers\n"
            "• **Transparency**: Many provide regular attestations or on-chain verification\n"
            "• **Accessibility**: Available 24/7 without traditional banking restrictions\n\n"
            "## Common Use Cases:\n\n"
            "• Trading pairs on cryptocurrency exchanges\n"
            "• Cross-border payments and remittances\n"
            "• Savings and lending in DeFi applications\n"
            "• Protection against crypto market volatility\n"
            "• Payments in countries with unstable currencies\n\n"
            "When using stablecoins, always research the backing mechanism, issuer reputation, and regulatory status. Remember that all stablecoins carry some level of risk. 🐌"
        )
    
    def _get_fallback_stablecoin_comparison(self, coin_ids: List[str], coins_data: Dict = None) -> str:
        """Provide fallback comparison when the AI service is unavailable."""
        # Basic information about common stablecoins
        stablecoin_info = {
            "usdc": {
                "type": "Fiat-backed",
                "backing": "USD reserves held in regulated financial institutions",
                "stability": "Very stable, minimal deviations",
                "risks": "Regulatory and counterparty risks",
                "adoption": "Widely used in DeFi and centralized exchanges"
            },
            "usdt": {
                "type": "Fiat-backed",
                "backing": "Mix of cash, cash equivalents, and other assets",
                "stability": "Generally stable despite controversies",
                "risks": "Reserve transparency and regulatory concerns",
                "adoption": "Highest liquidity and trading volume"
            },
            "dai": {
                "type": "Crypto-collateralized",
                "backing": "Over-collateralized crypto assets (primarily ETH)",
                "stability": "Relatively stable with some volatility during market stress",
                "risks": "Smart contract and collateral volatility risks",
                "adoption": "Popular in DeFi applications"
            },
            "busd": {
                "type": "Fiat-backed",
                "backing": "USD reserves held by Paxos Trust Company",
                "stability": "Very stable with strong regulatory compliance",
                "risks": "Phased out in US, regulatory dependence",
                "adoption": "Declining after Binance stopped new issuance"
            },
            "frax": {
                "type": "Hybrid algorithmic",
                "backing": "Partially collateralized, partially algorithmic",
                "stability": "Generally stable with more complexity",
                "risks": "Algorithm failure and governance risks",
                "adoption": "Growing in DeFi ecosystem"
            },
            "gusd": {
                "type": "Fiat-backed",
                "backing": "USD reserves held in FDIC-insured accounts",
                "stability": "Very stable with strong regulatory compliance",
                "risks": "Lower liquidity than other major stablecoins",
                "adoption": "Limited compared to USDC/USDT but strong in regulated markets"
            },
            "lusd": {
                "type": "Crypto-collateralized",
                "backing": "ETH collateral through the Liquity protocol",
                "stability": "Algorithmic stability mechanisms maintain peg",
                "risks": "Smart contract risks and ETH volatility",
                "adoption": "Niche usage in specific DeFi applications"
            },
            "snel": {
                "type": "Stablecoin focused on stability and risk awareness",
                "backing": "Depends on the specific implementation",
                "stability": "Designed for reliable stability",
                "risks": "Specific risks would depend on the implementation details",
                "adoption": "New stablecoin in development"
            }
        }
        
        # Default template for unknown stablecoins
        default_info = {
            "type": "Information not available in offline database",
            "backing": "Would require specific analysis",
            "stability": "Historical data would need to be analyzed",
            "risks": "All stablecoins carry various risks",
            "adoption": "Adoption metrics would need to be researched"
        }
        
        # Build comparison text
        comparison = "# Stablecoin Comparison\n\n"
        
        for coin_id in coin_ids:
            coin_info = stablecoin_info.get(coin_id.lower(), default_info)
            coin_name = coin_id.upper()
            
            comparison += f"## {coin_name}\n\n"
            comparison += f"• **Type**: {coin_info['type']}\n"
            comparison += f"• **Backing Mechanism**: {coin_info['backing']}\n"
            comparison += f"• **Stability Record**: {coin_info['stability']}\n"
            comparison += f"• **Key Risks**: {coin_info['risks']}\n"
            comparison += f"• **Market Adoption**: {coin_info['adoption']}\n\n"
        
        comparison += "This comparison is based on general knowledge about these stablecoins. For the most current information, consider consulting official documentation or recent market analysis. Remember that all stablecoins carry risks and should be used with caution. 🐌"
        
        return comparison