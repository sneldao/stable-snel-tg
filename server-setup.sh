#!/bin/bash
# Script to set up proper directory structure and permissions on the server

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up server environment...${NC}"

# SSH to the server and set up the environment
ssh snel-bot << 'EOF'
  set -e
  
  echo "Setting up deployment directory..."
  # Create fresh deployment directory with correct permissions
  sudo rm -rf /opt/snel-telegram
  sudo mkdir -p /opt/snel-telegram
  
  # Get current user
  CURRENT_USER=$(whoami)
  echo "Current user: $CURRENT_USER"
  
  # Change ownership to current user
  sudo chown -R $CURRENT_USER:$CURRENT_USER /opt/snel-telegram
  sudo chmod -R 755 /opt/snel-telegram
  
  # Create dummy files to test permissions
  cd /opt/snel-telegram
  echo "# Test Dockerfile" > Dockerfile
  echo "version: '3.8'" > docker-compose.yml
  echo "print('Hello')" > bot.py
  echo "python-telegram-bot==20.8" > requirements.txt
  echo "BOT_TOKEN=test" > .env
  
  # Set up docker permissions
  if getent group docker > /dev/null; then
    echo "Docker group exists, adding current user..."
    sudo usermod -aG docker $CURRENT_USER
  else
    echo "Docker group doesn't exist, creating..."
    sudo groupadd docker
    sudo usermod -aG docker $CURRENT_USER
  fi
  
  # Display permissions
  echo "Directory permissions:"
  ls -la /opt/snel-telegram
  
  # Display current user and groups
  echo "User and groups:"
  id
  
  # Test docker 
  echo "Testing Docker access:"
  if docker ps >/dev/null 2>&1; then
    echo "Docker works without sudo!"
  else
    echo "Docker requires sudo, setting up proper permissions..."
    sudo chown root:docker /var/run/docker.sock
    sudo chmod 666 /var/run/docker.sock
    # Try again
    if docker ps >/dev/null 2>&1; then
      echo "Docker now works without sudo!"
    else
      echo "Docker still requires sudo, will use sudo in workflow"
    fi
  fi
  
  # Test with a simple container
  echo "Testing Docker with a simple container..."
  docker run --rm hello-world || sudo docker run --rm hello-world
EOF

# Check if script succeeded
if [ $? -eq 0 ]; then
  echo -e "\n${GREEN}Server setup completed successfully!${NC}"
else
  echo -e "\n${RED}Server setup failed.${NC}"
  exit 1
fi 