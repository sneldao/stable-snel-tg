#!/bin/bash

# Create the environment file on the server
ssh snel-bot "cat > /opt/snel-telegram/.env.prod << 'EOL'
# Required variables
TELEGRAM_BOT_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
VENICE_API_KEY=your_venice_api_key_here
LOG_LEVEL=INFO

# API Keys for External Services
COINGECKO_API_KEY=your_coingecko_api_key_here
CRYPTOPANIC_API_KEY=your_cryptopanic_api_key_here

# Cache Configuration
ENABLE_CACHE_PERSISTENCE=true
MAX_CACHE_ENTRIES=1000

# Rate Limiting (requests per second)
COINGECKO_RATE_LIMIT=0.5
CRYPTOPANIC_RATE_LIMIT=0.01
VENICE_RATE_LIMIT=0.012

# Advanced Settings
CIRCUIT_BREAKER_THRESHOLD=5
CIRCUIT_BREAKER_RECOVERY_TIME=60
EOL"

echo "Environment file has been set up on the server."