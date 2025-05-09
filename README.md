# 🐌 SNEL - Stablecoin & RWA Information Bot

A Telegram bot focused on stablecoins and real-world assets (RWAs), providing reliable market data and educational resources. Built with a philosophy of slow, steady growth and risk awareness.

## 🔹 Philosophy

SNEL (Slow Notably Enlightened Libertarian) is a comically slow but knowledgeable crypto snail who helps users navigate the world of stablecoins and RWAs. 

SNEL is designed for those who prioritize stability over speculation. 
While the crypto world chases 100x gains, we focus on:

- Reliable stablecoin information
- Real-world asset (RWA) tracking
- Market stability indicators
- Security best practices
- AI-powered education and risk assessment
- Cautious, slow and steady approach to wealth preservation

## 🔹 Features

### Price & Market Data

- `/p <coin>` - Get current price
- `/s <coin>` - Get detailed price info
- `/c <coin> [days]` - Get price chart
- `/cs <coin> [days]` - Get candlestick chart
- `/top [limit]` - List top coins
- `/best <24h|7d>` - Best performers
- `/worst <24h|7d>` - Worst performers

### Technical Analysis

- `/ch <coin> [period]` - Price change analysis
- `/roi <coin>` - Return on Investment
- `/ath <coin>` - All Time High analysis

### Coin Information

- `/i <coin>` - General information
- `/des <coin>` - Coin description
- `/dev <coin>` - Development info
- `/t <coin>` - Team information
- `/wp <coin>` - Find whitepaper

### News & Community

- `/n <coin>` - Latest news
- `/soc <coin>` - Social media links
- `/ev <coin>` - Upcoming events

### AI & Stablecoin Features

- `/ask <question>` - Ask about anything
- `/analyze <coin>` - AI analysis of a stablecoin
- `/learn <topic>` - Educational content
- `/compare <coin1> <coin2>` - Compare stablecoins
- `/risk <coin>` - Stablecoin risk assessment
- `/market` - Stablecoin market overview

### Utility Commands

- `/about` - About the bot
- `/help` - Show help message
- `/status` - Check bot status

## 🔹 Project Structure

```
stable-snel-tg/
├── bot.py                 # Main bot code
├── requirements.txt       # Python dependencies
├── requirements-local.txt # Dependencies for local development
├── .env.example           # Example environment variables
├── docs/                  # Documentation
│   ├── AI_CAPABILITIES.md # Details on AI features
│   ├── VENICE_API.md      # Venice API guide
│   ├── AI_INTEGRATION_PLAN.md
│   └── direnv_instructions.md
├── scripts/               # Utility scripts
│   ├── load_env.sh        # Load environment variables
│   ├── fix-venv.sh        # Fix virtual environment issues
│   └── shell_integration.sh
├── telegram/              # Bot modules
│   ├── handlers/          # Command handlers
│   └── services/          # Business logic services
└── tests/                 # Test scripts
    ├── test_ai.py         # AI integration tests
    ├── test_ai_features.py # AI-focused test bot
    ├── test_api_keys.sh   # API key tests
    └── test_bot.py        # Basic test bot
```


## 🔹 Setup

1. Clone the repository
2. Create a `.env.prod` file with your API keys:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   VENICE_API_KEY=your_venice_api_key_here
   LOG_LEVEL=INFO
   ```
3. Copy `scripts/setup-server-env.example.sh` to `scripts/setup-server-env.sh` and update it with your bot token and API keys
4. Run `./scripts/setup-server-env.sh` to set up the environment on the server
5. Run `./deploy.sh` to deploy the bot

### Local Testing

For local development and testing:

1. Run `./scripts/setup-local-env.sh` to set up your local environment
2. Load environment variables: `source scripts/load_env.sh`
3. Test the AI integration: `python tests/test_ai.py`
4. Run the bot locally: `python bot.py`

## 🔹 Development

The bot is organized into several components:

- **Handlers**: Process commands and user interactions
- **Services**: Provide business logic and external API integration
  - `crypto_service.py`: CoinGecko API integration
  - `info_service.py`: Cryptocurrency information
  - `news_service.py`: News and social media info
  - `ai_service.py`: Gemini AI integration
  - `venice_service.py`: Venice API for stablecoin data

## 🔹 Deployment

The bot is deployed using a two-step process:

1. Push changes to GitHub:

   ```bash
   git add .
   git commit -m "your message"
   git push
   ```

2. Deploy on the server:
   ```bash
   ssh snel-bot "/opt/snel-telegram/pull-and-deploy.sh"
   ```

## 🔹 Security

- Environment variables are stored in `.env` on the server
- Sensitive files are gitignored
- Docker container runs with minimal permissions
- Setup scripts containing sensitive information are excluded from git

## 🔹 Web App Integration

SNEL can guide users to our web app: [Stable Station](https://stable-station.netlify.app/) for:
- Agent-guided swaps into stablecoins
- Global stablecoin diversification
- Portfolio management

## 🔹 Contact & Support

- Farcaster: @papa
- Lens: @papajams

## 🔹 License

MIT.

---

🐌 Shell wisdom: In crypto, slow and steady makes you ready!

---

Remember: Slow and steady may not necessarily win the race, but crashing and burning is a sure way to lose it! 🌱
