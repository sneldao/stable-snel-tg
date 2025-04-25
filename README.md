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
