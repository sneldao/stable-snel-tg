#!/bin/bash

# Create the environment file on the server
ssh snel-bot "cat > /opt/snel-telegram/.env.prod << 'EOL'
TELEGRAM_BOT_TOKEN=your_bot_token_here
LOG_LEVEL=INFO
EOL"

echo "Environment file has been set up on the server." 