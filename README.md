# Snel Telegram Bot

A simple Telegram echo bot that demonstrates deployment to a server using Docker.

## Features

- Echo messages back to users
- Status command to check bot health
- Docker-based deployment
- Secure environment variable handling

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
- `docker-compose.yml`: Docker configuration
- `Dockerfile`: Container definition
- `requirements.txt`: Python dependencies

## Deployment

The bot is deployed using Docker Compose. The deployment process is automated through GitHub Actions.

## Security

- Environment variables are stored in `.env.prod` on the server
- Sensitive files are gitignored
- Docker container runs with minimal permissions
- Setup scripts containing sensitive information are excluded from git
