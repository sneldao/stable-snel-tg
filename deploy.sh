#!/bin/bash

# Sync the project files to the server
rsync -avz --exclude 'venv' --exclude '.git' --exclude '__pycache__' --exclude '.env.prod' ./ snel-bot:/opt/snel-telegram/

# SSH into the server and start the bot
ssh snel-bot "cd /opt/snel-telegram && \
    docker-compose down && \
    docker-compose build --no-cache && \
    docker-compose up -d && \
    docker-compose logs -f" 