#!/bin/bash

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== SNEL Telegram Bot - Virtual Environment Fix ===${NC}\n"

# Detect Python command (python or python3)
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: Neither python nor python3 commands found. Please install Python 3.${NC}"
    exit 1
fi

echo -e "${GREEN}Using Python command: ${PYTHON_CMD}${NC}"

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d " " -f 2)
echo -e "${GREEN}Python version: ${PYTHON_VERSION}${NC}"

# Remove existing virtual environment
if [ -d "venv" ]; then
    echo -e "${YELLOW}Removing existing virtual environment...${NC}"
    rm -rf venv
fi

# Create new virtual environment
echo -e "${YELLOW}Creating new virtual environment...${NC}"
$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}Error creating virtual environment. Trying with --without-pip flag...${NC}"
    $PYTHON_CMD -m venv venv --without-pip
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to create virtual environment. Please check your Python installation.${NC}"
        exit 1
    fi
    
    # Install pip manually if needed
    echo -e "${YELLOW}Installing pip in the virtual environment...${NC}"
    source venv/bin/activate
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    ./venv/bin/python get-pip.py
    rm get-pip.py
    deactivate
fi

echo -e "${GREEN}Virtual environment created successfully!${NC}"

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install requirements
echo -e "\n${YELLOW}Installing requirements...${NC}"
./venv/bin/pip install -r requirements.txt

echo -e "\n${GREEN}=== Fix Complete! ===${NC}\n"
echo -e "To start testing, run the following commands:\n"
echo -e "${YELLOW}1. Activate the virtual environment (if not already activated):${NC}"
echo -e "   source venv/bin/activate\n"
echo -e "${YELLOW}2. Test AI integration:${NC}"
echo -e "   ./venv/bin/python test_ai.py\n"
echo -e "${YELLOW}3. Run the bot locally:${NC}"
echo -e "   ./venv/bin/python bot.py\n"
echo -e "${YELLOW}4. When finished, deactivate the virtual environment:${NC}"
echo -e "   deactivate"