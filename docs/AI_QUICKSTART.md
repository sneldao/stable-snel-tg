# SNEL Bot AI Integration: Quick Start Guide

This guide will help you quickly set up and test the new AI capabilities of the SNEL Telegram Bot on your local machine.

## Prerequisites

- Python 3.8 or higher
- A Telegram bot token (from [@BotFather](https://t.me/BotFather))
- A Google Gemini API key (from [Google AI Studio](https://ai.google.dev/))
- Optional: Venice API key (if available)

## 1. Initial Setup

### Clone the repository (if you haven't already)
```bash
git clone https://github.com/your-username/stable-snel-tg.git
cd stable-snel-tg
```

### Run the setup script
```bash
./setup-local-env.sh
```

This script will:
- Create a `.env` file with your API keys
- Set up a virtual environment
- Install all required dependencies

## 2. Testing the AI Integration

### Test the AI service components
```bash
python3 test_ai.py
```

This runs tests for:
- AI responses with Gemini API
- Stablecoin analysis functionality
- Education content generation
- Mock Venice API data (if no real API is available)

### Run the bot locally
```bash
python3 bot.py
```

## 3. Testing Commands in Telegram

Open Telegram and start a chat with your bot. Try these commands:

1. Basic interaction:
   ```
   /ask What makes a good stablecoin?
   ```

2. Stablecoin analysis:
   ```
   /analyze usdc
   ```

3. Educational content:
   ```
   /learn depeg risks
   ```

4. Compare stablecoins:
   ```
   /compare usdc dai
   ```

5. Risk assessment:
   ```
   /risk usdt
   ```

6. Market overview:
   ```
   /market
   ```

7. Chat with the bot by mentioning its username:
   ```
   @your_bot_username What do you think about algorithmic stablecoins?
   ```

## 4. Troubleshooting

### Common Issues

#### "No module named 'google.generativeai'"
Run the setup script again or manually install the package:
```bash
python3 -m pip install google-generativeai
```

#### "API key not found" errors
Make sure your `.env` file contains the correct API keys:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
VENICE_API_KEY=your_venice_api_key_here
```

#### Slow or no responses from the AI
- Check your internet connection
- Verify your Gemini API key quota hasn't been exceeded
- Try with shorter, simpler queries first

## 5. Next Steps

After successful testing:
1. Update your production environment variables on the server
2. Commit and push your changes
3. Deploy to your production server

For more detailed information:
- [AI Capabilities Documentation](AI_CAPABILITIES.md)
- [Venice API Integration](VENICE_API.md)
- [AI Integration Plan](../AI_INTEGRATION_PLAN.md)

Remember: Slow and steady may not necessarily win the race, but crashing and burning is a sure way to lose it! 🐌