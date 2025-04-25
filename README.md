# Snel Telegram Bot

A comprehensive cryptocurrency information and analysis Telegram bot built with modern Python and Telegram API.

## Features

### Phase 1 - Core Features (Current Focus)

#### Price and Market Data Commands

- `/p <coin>` - Get current coin price
- `/s <coin>` - Detailed price, market cap and volume information
- `/c <coin> [days]` - Price chart with volume overlay
- `/cs <coin> [days]` - Candlestick chart for technical analysis
- `/top [limit]` - List top coins by market cap (default: 30)
- `/best <24h|7d>` - Best performing coins
- `/worst <24h|7d>` - Worst performing coins

#### Basic Information Commands

- `/i <coin>` - General coin information and statistics
- `/des <coin>` - Detailed coin description and overview
- `/dev <coin>` - Development activity and GitHub statistics
- `/t <coin>` - Team information and key personnel
- `/wp <coin>` - Find and link to coin's whitepaper

### Phase 2 - Advanced Features (Coming Soon)

#### News & Social Media

- `/n <coin>` - Latest news articles about the coin
- `/tw <coin>` - Recent tweets mentioning the coin
- `/soc <coin>` - Social media presence and engagement
- `/ev <coin>` - Upcoming events and conferences

#### Technical Analysis

- `/ch <coin> [period]` - Price change analysis over time
- `/roi <coin>` - Return on Investment calculations
- `/ath <coin>` - All-time high price and related metrics

### Phase 3 - Utility Features (Future)

#### Exchange & Trading

- `/m <coin>` - Find exchanges where the coin is traded
- `/ex <exchange>` - Detailed exchange information
- `/comp <coin1> <coin2>` - Compare two coins

#### Wallets

- `/wa <coin>` - Recommended wallets and storage options

## Implementation Plan

### Phase 1 Implementation (Current)

1. **Core Price Data**

   - [x] Basic price commands (/p, /top, /best, /worst)
   - [ ] Enhanced price data (/s command)
   - [ ] Advanced charting (/c, /cs commands)

2. **Basic Information**
   - [ ] Coin information service
   - [ ] Description and team data integration
   - [ ] Whitepaper finder service

### Phase 2 Implementation

1. **News & Social Integration**

   - [ ] News API integration
   - [ ] Twitter API integration
   - [ ] Social media aggregator

2. **Technical Analysis**
   - [ ] Price history analysis
   - [ ] ROI calculator
   - [ ] ATH tracking

### Phase 3 Implementation

1. **Exchange Integration**

   - [ ] Exchange listing service
   - [ ] Exchange comparison
   - [ ] Trading pair finder

2. **Wallet Integration**
   - [ ] Wallet recommendation system
   - [ ] Security features
   - [ ] Storage options

## Technical Architecture

### Services

- `CryptoService`: Core price and market data
- `InfoService`: Coin information and metadata
- `ChartService`: Technical analysis and charting
- `NewsService`: News and social media integration
- `ExchangeService`: Exchange and trading information
- `WalletService`: Wallet recommendations

### Data Sources

- CoinGecko API for price and market data
- GitHub API for development metrics
- News APIs for cryptocurrency news
- Twitter API for social media
- Exchange APIs for trading information

## Setup

1. Clone the repository
2. Create a `.env.prod` file with your Telegram bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   LOG_LEVEL=INFO
   ```
3. Copy `setup-server-env.example.sh` to `setup-server-env.sh` and update it with your bot token
4. Run `./setup-server-env.sh` to set up the environment on the server
5. Run `./deploy.sh` to deploy the bot

## Development

- `bot.py`: Main bot code
- `telegram/handlers/`: Command handlers
- `telegram/services/`: Business logic services
- `docker-compose.yml`: Docker configuration
- `Dockerfile`: Container definition
- `requirements.txt`: Python dependencies

## Deployment

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

The deployment script will:

- Pull the latest changes from GitHub
- Stop any running containers
- Rebuild and start the containers
- Show deployment status

## Security

- Environment variables are stored in `.env.prod` on the server
- Sensitive files are gitignored
- Docker container runs with minimal permissions
- Setup scripts containing sensitive information are excluded from git
