# Venice AI Integration

## Overview

The Venice AI service functions as an alternative/fallback to Google's Gemini API, providing AI capabilities when Gemini is unavailable, rate-limited, or experiencing issues. This ensures the SNEL Bot always has access to AI functionality for analyzing stablecoin data and answering user queries.

## Integration Architecture

The AI system in SNEL Bot uses a layered approach:

1. **Primary AI**: Google's Gemini API (when available)
2. **Secondary AI**: Venice API (when Gemini fails or is unavailable)
3. **Fallback Responses**: Pre-written responses when both AI services are unavailable

This architecture provides redundancy and ensures users always receive helpful responses.

## Current Implementation Status

The current implementation includes:
- A service layer (`VeniceService`) that handles API communication with Venice
- Automatic failover from Gemini to Venice when needed
- Consistent response formatting regardless of which AI service is used

## API Endpoints

The Venice AI service implements the following endpoints:

| Endpoint | Description |
|----------|-------------|
| `chat/completions` | Get AI responses to user messages |
| `analyze/stablecoin` | Analyze a stablecoin with AI |
| `education` | Generate educational content about stablecoin topics |
| `compare/stablecoins` | Compare multiple stablecoins |
| `ping` | Check if the Venice API is available |

## Authentication

The Venice API requires an API key for authentication. The key should be set in the environment variables:

```
VENICE_API_KEY=your_venice_api_key_here
```

## Working with Existing Bot Data

Both AI services (Gemini and Venice) leverage the extensive data already available through the bot's existing commands. When analyzing stablecoins or responding to user queries, the AI services:

1. Gather data from CoinGecko and other existing sources
2. Format the data as context for the AI
3. Use the AI to interpret and explain the data in a user-friendly way
4. Present the AI's insights alongside the raw data when appropriate

## Future Enhancements

Planned enhancements for the Venice AI integration include:
- Improved context formatting for more accurate responses
- Specialized prompt engineering for stablecoin analysis
- Storing frequent AI responses for faster access
- Training with stablecoin-specific knowledge

## Testing

To test the Venice AI integration:
1. Set the `VENICE_API_KEY` in your environment variables
2. Run the test script: `python test_ai.py`
3. Check that the Venice service can process AI requests
4. Test fallback from Gemini to Venice by temporarily removing the Gemini API key

## Troubleshooting

Common issues:
- **"No Venice API key configured"**: Set the VENICE_API_KEY environment variable
- **"HTTP error"**: Check your internet connection and API key validity
- **"Request error"**: The API server may be unavailable, the service will fall back to predefined responses
- **"Unexpected error"**: Check logs for details, may indicate a parsing or data structure issue

When both Gemini and Venice are unavailable, the bot will use pre-defined fallback responses to ensure it can still provide useful information to users.