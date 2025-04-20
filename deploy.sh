#!/bin/bash

# Exit on error
set -e

# Configuration
SERVER="snel-bot"
REMOTE_DIR="/opt/snel-telegram"
DOCKER_COMPOSE_FILE="docker-compose.yml"

# Sync the project files
echo "Syncing files to server..."
rsync -avz --exclude 'venv' --exclude '__pycache__' --exclude '.git' ./ $SERVER:$REMOTE_DIR/

# SSH into the server and deploy
echo "Deploying on server..."
ssh $SERVER "cd $REMOTE_DIR && \
    docker-compose down && \
    docker-compose build --no-cache && \
    docker-compose up -d"

echo "Deployment complete!" 