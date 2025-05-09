#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Server connection details
SERVER_NAME="snel-bot"
SERVER_PATH="/opt/snel-telegram"

echo -e "${BLUE}Checking environment variables on server ${SERVER_NAME}${NC}"

# Verify connection to server
if ! ssh ${SERVER_NAME} "echo Connection successful"; then
    echo -e "${RED}Failed to connect to server ${SERVER_NAME}${NC}"
    exit 1
fi

# Run the check-env.sh script on the server
echo -e "\n${YELLOW}Running environment check on server...${NC}"
if ! ssh ${SERVER_NAME} "cd ${SERVER_PATH} && bash scripts/check-env.sh"; then
    echo -e "${RED}Environment check failed on server.${NC}"
    
    # Get the list of required and recommended variables from .env.example
    echo -e "\n${YELLOW}Getting required variables from local .env.example...${NC}"
    
    # Read the local environment example file
    LOCAL_VARS=$(cat .env.example)
    
    # Get the server's current environment file
    echo -e "\n${YELLOW}Getting current server environment...${NC}"
    REMOTE_ENV=$(ssh ${SERVER_NAME} "cat ${SERVER_PATH}/.env.prod" 2>/dev/null)
    
    # Create a temporary local file with the server's environment
    TMP_FILE=".env.server.tmp"
    echo "${REMOTE_ENV}" > ${TMP_FILE}
    
    # Get missing variables by comparing
    echo -e "\n${BLUE}Analysis of server environment variables:${NC}"
    
    # Extract variable names from .env.example
    while IFS= read -r line; do
        # Skip comments and empty lines
        if [[ ! $line =~ ^# && ! -z $line ]]; then
            # Extract variable name before =
            VAR_NAME=$(echo "$line" | cut -d'=' -f1)
            
            # Check if variable exists in the server environment
            if ! grep -q "^${VAR_NAME}=" ${TMP_FILE}; then
                echo -e "  ${RED}Missing: ${VAR_NAME}${NC}"
                echo -e "  ${YELLOW}Default value: ${line#*=}${NC}"
                
                # Ask user if they want to set this variable
                read -p "  Do you want to set ${VAR_NAME} on the server? (y/n): " RESPONSE
                if [[ "$RESPONSE" == "y" || "$RESPONSE" == "Y" ]]; then
                    read -p "  Enter value for ${VAR_NAME}: " VAR_VALUE
                    
                    # Add the variable to the server's environment file
                    ssh ${SERVER_NAME} "echo '${VAR_NAME}=${VAR_VALUE}' >> ${SERVER_PATH}/.env.prod"
                    echo -e "  ${GREEN}Added ${VAR_NAME} to server environment.${NC}"
                fi
            else
                # Variable exists, get its current value for display
                SERVER_VALUE=$(grep "^${VAR_NAME}=" ${TMP_FILE} | cut -d'=' -f2-)
                MASKED_VALUE="${SERVER_VALUE:0:3}...${SERVER_VALUE: -3}"
                echo -e "  ${GREEN}✓ ${VAR_NAME}: ${MASKED_VALUE}${NC}"
            fi
        fi
    done < .env.example
    
    # Clean up
    rm ${TMP_FILE}
    
    # Run the check again to verify
    echo -e "\n${YELLOW}Verifying environment after updates...${NC}"
    if ssh ${SERVER_NAME} "cd ${SERVER_PATH} && bash scripts/check-env.sh"; then
        echo -e "${GREEN}Environment check now passes!${NC}"
    else
        echo -e "${RED}Environment check still fails. Please connect to the server and fix manually.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}Server environment check passed!${NC}"
fi

echo -e "\n${GREEN}Server environment verification complete.${NC}"
exit 0