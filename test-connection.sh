#!/bin/bash
# Script to test connection to Hetzner server and Docker functionality

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Testing connection to Hetzner server...${NC}"

# Get SSH host alias from local config
SSH_HOST="snel-bot"

# Test SSH connection 
if ssh -o ConnectTimeout=5 $SSH_HOST "echo Connection successful"; then
    echo -e "${GREEN}✓ SSH connection successful${NC}"
else
    echo -e "${RED}✗ SSH connection failed${NC}"
    echo "Check your SSH config and keys"
    exit 1
fi

# Test Docker on remote server
echo -e "\n${YELLOW}Testing Docker on remote server...${NC}"
if ssh $SSH_HOST "docker --version && docker compose version"; then
    echo -e "${GREEN}✓ Docker is installed and working${NC}"
else
    echo -e "${RED}✗ Docker check failed${NC}"
    exit 1
fi

# Check if the bot container is running
echo -e "\n${YELLOW}Checking if bot container is running...${NC}"
if ssh $SSH_HOST "docker ps | grep snel-telegram-bot"; then
    echo -e "${GREEN}✓ Bot container is running${NC}"
else
    echo -e "${RED}✗ Bot container is not running${NC}"
    
    # Check if it exists but is stopped
    if ssh $SSH_HOST "docker ps -a | grep snel-telegram-bot"; then
        echo -e "${YELLOW}Container exists but is not running. Checking logs:${NC}"
        ssh $SSH_HOST "docker logs snel-telegram-bot --tail 50"
    fi
fi

# Check Docker volumes and disk space
echo -e "\n${YELLOW}Checking Docker disk usage...${NC}"
ssh $SSH_HOST "docker system df && df -h | grep /var"

echo -e "\n${YELLOW}Testing deployment directory permissions...${NC}"
ssh $SSH_HOST "ls -la /opt/snel-telegram"

echo -e "\n${GREEN}Test completed.${NC}" 