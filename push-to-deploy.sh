#!/bin/bash
# Script to push changes to GitHub to trigger deployment

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Checking Git status...${NC}"
git status

echo -e "\n${YELLOW}Do you want to commit and push all changes to trigger deployment? (y/n)${NC}"
read answer

if [ "$answer" != "y" ]; then
    echo -e "${RED}Aborting...${NC}"
    exit 1
fi

# Add all changes
echo -e "\n${YELLOW}Adding all changes...${NC}"
git add .

# Prompt for commit message
echo -e "\n${YELLOW}Enter commit message:${NC}"
read commit_message

# Commit changes
echo -e "\n${YELLOW}Committing changes...${NC}"
git commit -m "$commit_message"

# Push to GitHub
echo -e "\n${YELLOW}Pushing to GitHub...${NC}"
if git push origin master; then
    echo -e "\n${GREEN}Changes pushed successfully!${NC}"
    echo -e "${GREEN}GitHub Actions workflow should be triggered automatically.${NC}"
    echo -e "${YELLOW}You can check the workflow status at:${NC}"
    echo -e "https://github.com/sneldao/stable-snel-tg/actions"
else
    echo -e "\n${RED}Failed to push changes.${NC}"
    echo -e "${YELLOW}Please check your Git configuration and try again.${NC}"
    exit 1
fi 