# 🐌 SNEL - Stablecoin & RWA Information Bot

A Telegram bot focused on stablecoins and real-world assets (RWAs), providing reliable market data and educational resources. Built with a philosophy of slow, steady growth and risk awareness.

## 🔹 Philosophy

SNEL is designed for those who prioritize stability over speculation. While the crypto world chases 100x gains, we focus on:

- Reliable stablecoin information
- Real-world asset (RWA) tracking
- Market stability indicators
- Security best practices

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

### Utility Commands

- `/about` - About the bot
- `/help` - Show help message
- `/status` - Check bot status

## 🔹 Setup

1. Clone the repository
2. Create a `.env.prod` file with your Telegram bot token:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   LOG_LEVEL=INFO
   ```
3. Copy `setup-server-env.example.sh` to `setup-server-env.sh` and update it with your bot token
4. Run `./setup-server-env.sh` to set up the environment on the server
5. Run `./deploy.sh` to deploy the bot

## 🔹 Development

- `bot.py`: Main bot code
- `telegram/handlers/`: Command handlers
- `telegram/services/`: Business logic services
- `docker-compose.yml`: Docker configuration
- `Dockerfile`: Container definition
- `requirements.txt`: Python dependencies

## 🔹 Deployment

The bot is deployed using a two-step process:

1. Push changes to GitHub:

   ```bash
   git add .
   git commit -m "your message"
   git push
   ```

2. 2. Deploy on the server:
   ```bash
   ssh snel-bot "/opt/snel-telegram/pull-and-deploy.sh"
   ```

## 🔹 Security

- Environment variables are stored in `.env.prod` on the server
- Sensitive files are gitignored
- Docker container runs with minimal permissions
- Setup scripts containing sensitive information are excluded from git

## 🔹 Contact & Support

- Farcaster: @papa
- Lens: @papajams

## 🔹 License

MIT.

---

Remember: Slow and steady may not necessarily win the race, but crashing and burning is a sure way to lose it! 🌱
