# SNEL Telegram Bot Setup Guide

This guide provides instructions for setting up and running the SNEL Telegram Bot, focusing on stablecoins and real-world assets (RWAs).

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- Git
- A Telegram Bot Token (obtained from BotFather)
- API keys for external services (optional, but recommended)

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/stable-snel-tg.git
cd stable-snel-tg
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file based on the example:

```bash
cp .env.example .env
```

Edit the `.env` file and add your API keys:

```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
COINGECKO_API_KEY=your_coingecko_api_key_here
CRYPTOPANIC_API_KEY=your_cryptopanic_api_key_here
VENICE_API_KEY=your_venice_api_key_here
LOG_LEVEL=INFO
```

### 5. Run the Bot

```bash
python bot.py
```

## Docker Setup

### 1. Build Docker Image

```bash
docker build -t snel-telegram-bot .
```

### 2. Run with Docker Compose

Make sure to set up your environment variables in `.env` first, then run:

```bash
docker-compose up -d
```

## API Keys

For full functionality, you'll need the following API keys:

1. **Telegram Bot Token**: Create a bot through [BotFather](https://t.me/botfather)
2. **Gemini API Key**: Sign up at [Google AI Studio](https://makersuite.google.com/)
3. **CoinGecko API Key**: Register at [CoinGecko](https://www.coingecko.com/api/pricing)
4. **CryptoPanic API Key**: Get from [CryptoPanic](https://cryptopanic.com/developers/api/)
5. **Venice API Key**: Contact the Venice team for access

## Testing

To verify your setup is working correctly:

```bash
# Test the basic functionality
python test_all_handlers.py

# Test the AI integration
python test_ai_local.py
```

## Troubleshooting

### Common Issues

1. **Bot not responding**: Verify your `TELEGRAM_BOT_TOKEN` is correct and the bot is running
2. **API calls failing**: Check that your API keys are valid and correctly formatted
3. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
4. **Permission errors**: Ensure the directories have appropriate permissions

## Next Steps

- Explore the bot's commands by sending `/help` to your bot
- Customize the bot's behavior by modifying handlers in `telegram/handlers/`
- Add new services or extend existing ones in `telegram/services/`

For more detailed information, refer to the main [README.md](README.md) file.