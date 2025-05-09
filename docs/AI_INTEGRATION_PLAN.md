# AI Integration Plan for SNEL Telegram Bot

This document outlines the plan for integrating AI responsivity, personality, and stablecoin ecosystem knowledge into the SNEL Telegram Bot.

## 1. Overview

We've added the following new features to the SNEL Telegram Bot:

- AI-powered responses using Google's Gemini API (primary)
- Venice AI as an alternative/fallback when Gemini is unavailable
- Enhanced understanding of the bot's existing stablecoin data
- Improved bot personality focused on stability and risk-awareness

## 2. New Commands

| Command | Description |
|---------|-------------|
| `/ask <question>` | Ask any question to the AI |
| `/analyze <coin>` | Get AI-powered analysis of a stablecoin |
| `/learn <topic>` | Get educational content about stablecoin topics |
| `/compare <coin1> <coin2>` | Compare multiple stablecoins |
| `/risk <coin>` | Get risk assessment for a stablecoin |
| `/market` | Get a stablecoin market overview |

## 3. Local Testing Plan

### 3.1 Environment Setup

1. Create a local `.env` file with required API keys:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   VENICE_API_KEY=your_venice_api_key_here
   LOG_LEVEL=INFO
   ```

2. Install the new dependencies:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

### 3.2 Component Testing

1. **Test AI Service**
   ```bash
   python3 test_ai.py
   ```
   This script tests the Gemini API integration with the Venice API as a fallback, analyzing stablecoin data and generating educational content.

2. **Test AI Fallback Mechanism**
   The test script verifies that when Gemini API is unavailable or rate-limited, the system will correctly fall back to Venice AI, and finally to pre-written responses if both services fail.

### 3.3 Full Bot Testing

1. **Run the bot locally**
   ```bash
   python3 bot.py
   ```

2. **Test each new command with your Telegram bot**:
   - `/ask What are stablecoins?`
   - `/analyze usdc`
   - `/learn depeg risks`
   - `/compare usdc dai`
   - `/risk usdt`
   - `/market`

3. **Test conversation capabilities** by mentioning the bot in a message.

### 3.4 Integration Testing Checklist

- [ ] AI responses are informative and match the bot's personality
- [ ] Stablecoin analysis provides valuable insights based on existing data
- [ ] Educational content is clear and beginner-friendly
- [ ] Proper error handling when coins are not found
- [ ] Bot responds to mentions with intelligent replies
- [ ] Response formatting is correct (Markdown rendering)
- [ ] Response time is acceptable
- [ ] Fallback mechanism works correctly when primary AI is unavailable

## 4. Deployment Plan

After successful local testing, follow these steps to deploy to the Hetzner server:

1. **Update environment variables on the server**:
   ```bash
   # Update your setup-server-env.sh file (don't commit this file with real keys)
   ./setup-server-env.sh
   ```

2. **Commit and push changes**:
   ```bash
   git add .
   git commit -m "Add AI capabilities and stablecoin ecosystem knowledge"
   git push
   ```

3. **Deploy on the server**:
   ```bash
   ssh snel-bot "/opt/snel-telegram/pull-and-deploy.sh"
   ```

4. **Verify deployment**:
   - Test all new commands on the deployed bot
   - Check logs for any errors:
     ```bash
     ssh snel-bot "docker logs snel-telegram-bot"
     ```

## 5. Future Improvements

- Expand the stablecoin knowledge base
- Improve integration with existing bot data sources
- Add more specialized AI analysis for different stablecoin types
- Create periodic market reports and alerts for depeg events
- Develop user preferences for customizing AI responses
- Implement caching for frequent AI responses to reduce API usage

## 6. Troubleshooting

### Common Issues and Solutions

#### AI Service Errors
- Check that the GEMINI_API_KEY is valid and has sufficient quota
- Verify network connectivity to Google's API servers

#### Venice AI Errors
- The service is configured as a fallback when Gemini is unavailable
- Both APIs have thorough error handling with graceful fallbacks
- The base URL and authentication method can be updated as needed

#### Bot Response Issues
- If markdown formatting fails, check for special characters in responses
- Long responses may be truncated by Telegram; consider paginating if necessary