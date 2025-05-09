#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ENV_FILE=".env.prod"
ENV_EXAMPLE_FILE=".env.example"

# Get script directory and navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

echo -e "${BLUE}Checking environment variables in ${PROJECT_ROOT}/${ENV_FILE}${NC}"

# Check if .env.prod exists
if [ ! -f "${PROJECT_ROOT}/${ENV_FILE}" ]; then
    echo -e "${YELLOW}Warning: ${ENV_FILE} does not exist${NC}"
    
    # Check if .env.example exists to use as template
    if [ -f "${PROJECT_ROOT}/${ENV_EXAMPLE_FILE}" ]; then
        echo -e "${YELLOW}Creating ${ENV_FILE} from ${ENV_EXAMPLE_FILE}...${NC}"
        cp "${PROJECT_ROOT}/${ENV_EXAMPLE_FILE}" "${PROJECT_ROOT}/${ENV_FILE}"
        echo -e "${GREEN}Created ${ENV_FILE}${NC}"
        echo -e "${YELLOW}Please update the values in ${ENV_FILE} with your actual credentials${NC}"
    else
        echo -e "${YELLOW}Creating empty ${ENV_FILE}...${NC}"
        touch "${PROJECT_ROOT}/${ENV_FILE}"
        echo -e "${GREEN}Created empty ${ENV_FILE}${NC}"
    fi
fi

# Required environment variables to check
REQUIRED_VARS=(
    "TELEGRAM_BOT_TOKEN"
    "VENICE_API_KEY"
    "GEMINI_API_KEY"
    "LOG_LEVEL"
)

# Recommended environment variables to check (warn if missing)
RECOMMENDED_VARS=(
    "COINGECKO_API_KEY"
    "CRYPTOPANIC_API_KEY"
    "ENABLE_CACHE_PERSISTENCE"
    "MAX_CACHE_ENTRIES"
    "COINGECKO_RATE_LIMIT"
    "CRYPTOPANIC_RATE_LIMIT"
    "VENICE_RATE_LIMIT"
    "CIRCUIT_BREAKER_THRESHOLD"
    "CIRCUIT_BREAKER_RECOVERY_TIME"
)

# Source the environment file to check variables
source "${PROJECT_ROOT}/${ENV_FILE}"

# Check for missing or empty required variables
MISSING_VARS=()
for VAR in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!VAR}" ]; then
        MISSING_VARS+=("$VAR")
    fi
done

# Check for missing or empty recommended variables
MISSING_RECOMMENDED=()
for VAR in "${RECOMMENDED_VARS[@]}"; do
    if [ -z "${!VAR}" ]; then
        MISSING_RECOMMENDED+=("$VAR")
    fi
done

# If there are missing required variables, report them
if [ ${#MISSING_VARS[@]} -gt 0 ]; then
    echo -e "${RED}ERROR: The following required environment variables are missing or empty in ${ENV_FILE}:${NC}"
    for VAR in "${MISSING_VARS[@]}"; do
        echo -e "  - ${RED}${VAR}${NC}"
    done
    echo -e "${YELLOW}Please add these variables to ${PROJECT_ROOT}/${ENV_FILE}${NC}"
    exit 1
else
    echo -e "${GREEN}All required environment variables are set!${NC}"
    
    # Print the first few characters of sensitive variables for verification
    echo -e "${BLUE}Environment variable check:${NC}"
    echo -e "  TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN:0:5}...${TELEGRAM_BOT_TOKEN: -5}"
    echo -e "  VENICE_API_KEY: ${VENICE_API_KEY:0:5}...${VENICE_API_KEY: -5}"
    echo -e "  GEMINI_API_KEY: ${GEMINI_API_KEY:0:5}...${GEMINI_API_KEY: -5}"
    echo -e "  LOG_LEVEL: ${LOG_LEVEL}"
    
    # Report on missing recommended variables
    if [ ${#MISSING_RECOMMENDED[@]} -gt 0 ]; then
        echo -e "${YELLOW}WARNING: The following recommended environment variables are missing or empty:${NC}"
        for VAR in "${MISSING_RECOMMENDED[@]}"; do
            echo -e "  - ${YELLOW}${VAR}${NC}"
        done
        echo -e "${BLUE}The bot will still run, but some features may be limited${NC}"
    else
        echo -e "${GREEN}All recommended environment variables are set!${NC}"
    fi
    
    # Print additional environment variables if they exist
    if [ ! -z "$COINGECKO_API_KEY" ]; then
        echo -e "  COINGECKO_API_KEY: ${COINGECKO_API_KEY:0:5}...${COINGECKO_API_KEY: -5}"
    fi
    if [ ! -z "$CRYPTOPANIC_API_KEY" ]; then
        echo -e "  CRYPTOPANIC_API_KEY: ${CRYPTOPANIC_API_KEY:0:5}...${CRYPTOPANIC_API_KEY: -5}"
    fi
    if [ ! -z "$ENABLE_CACHE_PERSISTENCE" ]; then
        echo -e "  ENABLE_CACHE_PERSISTENCE: ${ENABLE_CACHE_PERSISTENCE}"
    fi
    if [ ! -z "$MAX_CACHE_ENTRIES" ]; then
        echo -e "  MAX_CACHE_ENTRIES: ${MAX_CACHE_ENTRIES}"
    fi
    if [ ! -z "$COINGECKO_RATE_LIMIT" ]; then
        echo -e "  COINGECKO_RATE_LIMIT: ${COINGECKO_RATE_LIMIT}"
    fi
fi

echo -e "${GREEN}Environment check completed${NC}"
exit 0