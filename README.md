# 🐌 SNEL - Stablecoin & RWA Information Bot

A Telegram bot focused on stablecoins and real-world assets (RWAs), providing reliable market data and educational resources. Built with a philosophy of slow, steady growth and risk awareness. Features advanced caching, error handling with retries, rate limiting, and monitoring.

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
│   ├── services/          # Business logic services
│   │   ├── crypto_service.py            # Basic crypto data service
│   │   ├── enhanced_crypto_service.py   # Enhanced service with caching and retries
│   │   ├── info_service.py              # Cryptocurrency information
│   │   ├── news_service.py              # News and social media info
│   │   ├── ai_service.py                # Gemini AI integration
│   │   └── venice_service.py            # Venice API for stablecoin data
│   └── utils/             # Utility functions
│       ├── cache.py       # Caching system with persistence
│       ├── retries.py     # Error handling with retries and circuit breaker
│       ├── logging.py     # Advanced logging utilities
│       ├── metrics.py     # Performance and monitoring metrics
│       ├── startup.py     # Application startup utilities
│       └── limits/        # Rate limiting implementation
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

For detailed setup instructions, see [docs/SETUP.md](docs/SETUP.md).

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
  - `enhanced_crypto_service.py`: Extended service with caching and retries
  - `info_service.py`: Cryptocurrency information
  - `news_service.py`: News and social media info
  - `ai_service.py`: Gemini AI integration
  - `venice_service.py`: Venice API for stablecoin data
- **Utils**: Utility functions and infrastructure
  - `cache.py`: In-memory caching with persistence
  - `retries.py`: Automatic retries with circuit breaker pattern
  - `metrics.py`: Performance monitoring and reporting
  - `logging.py`: Structured and configurable logging
  - `limits`: Rate limiting for external APIs

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
- Circuit breakers prevent cascading failures
- Rate limiting protects against API abuse and quota exhaustion

## 🔹 Reliability Features

- **Caching System**: Improves performance and reduces API calls
  - In-memory cache with configurable TTL
  - Disk persistence to survive restarts
  - Automatic cleanup of expired entries
  
- **Error Handling**: Robust handling of failures
  - Automatic retries with exponential backoff
  - Circuit breaker pattern to prevent cascading failures
  - Intelligent handling of rate limits and temporary errors
  
- **Rate Limiting**: Smart throttling of external API requests
  - Token bucket algorithm for precise rate control
  - Fair sharing of resources when under contention
  - Service-specific limits based on API requirements
  
- **Monitoring**: Comprehensive metrics and reporting
  - API call performance tracking
  - Cache efficiency monitoring
  - Circuit breaker status tracking
  - Human-readable reports for analysis

For detailed information on these features, see [docs/UTILITIES.md](docs/UTILITIES.md).

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

## 🔹 AI Enhancement Roadmap

Our vision for SNEL's future development focuses on enhancing its AI capabilities to provide even more value to users interested in stablecoins and RWAs. This roadmap outlines our planned improvements:

### Phase 1: Enhanced Analysis Capabilities

#### 1. Smart Analysis Command
- **New Command**: `/smart <coin>` 
- **Description**: Combines price data with AI analysis for comprehensive insights
- **Implementation**:
  - Integrate existing price data from `crypto_service` with AI analysis
  - Create contextual prompts that focus on stability metrics and risk factors
  - Format responses to highlight key stability indicators and potential concerns
- **Benefits**: Provides users with AI-enhanced insights beyond raw data, helping them make more informed decisions

#### 2. News Sentiment Analysis
- **New Command**: `/sentiment <coin>`
- **Description**: Uses AI to analyze sentiment in recent news about a coin
- **Implementation**:
  - Enhance the existing `news_service` to collect more comprehensive news data
  - Create AI prompts focused on sentiment extraction and categorization
  - Present a sentiment score with key positive/negative factors identified
- **Benefits**: Helps users understand market perception and identify potential risks not reflected in price data

### Phase 2: Economic & Global Data Integration

#### 1. Inflation Data Integration
- **New Services**: `WorldBankService` and `AlphaVantageService`
- **New Commands**: 
  - `/inflation <country>` - Global inflation data
  - `/stable-value <coin> <country>` - Stablecoin value relative to local inflation
- **Implementation**:
  - Develop new service classes for World Bank and Alpha Vantage APIs
  - Create data visualization capabilities for inflation trends
  - Implement caching to respect API rate limits
- **Benefits**: Provides global context for stablecoin usage, particularly valuable for users in high-inflation regions

#### 2. Portfolio Analysis Tools
- **New Commands**: 
  - `/portfolio` - Analyze user's stablecoin portfolio
  - `/diversify` - Get diversification recommendations
- **Implementation**:
  - Create temporary portfolio data storage during chat sessions
  - Develop AI prompts for portfolio risk assessment
  - Implement visualization of portfolio allocation
- **Benefits**: Helps users maintain balanced exposure across different stablecoin types and regions

### Phase 3: Advanced Integrations & Applications

#### 1. Web App Integration Enhancement
- **Description**: Deeper integration with Stable Station web app
- **Implementation**:
  - Create direct deep links to specific features on Stable Station
  - Develop shared backend services between bot and web app
  - Implement optional user authentication between platforms
- **Benefits**: Seamless experience for users moving between the bot and web app

#### 2. Predictive Analytics Features
- **New Commands**: 
  - `/trend <coin>` - Stability trend prediction
  - `/alert <condition>` - Set up custom stability alerts
- **Implementation**:
  - Train specialized AI models on stablecoin historical data
  - Develop notification system for predefined conditions
  - Create visualization for trend predictions
- **Benefits**: Anticipatory insights help users stay ahead of potential stability issues

This roadmap represents our commitment to making stablecoin and RWA information more accessible, insightful, and actionable through the power of AI, while maintaining our philosophy of cautious, steady wealth preservation.
