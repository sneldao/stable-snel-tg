#!/bin/bash

# Script to load environment variables from .env file

# Get script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

# Check if .env file exists in project root
if [ -f "$PROJECT_ROOT/.env" ]; then
    echo "Loading environment variables from .env file..."
    
    # Read each line from the .env file
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Skip comments and empty lines
        if [[ ! "$line" =~ ^# && -n "$line" ]]; then
            # Export the variable
            export "$line"
            
            # Extract variable name for display (without the value)
            var_name=$(echo "$line" | cut -d= -f1)
            echo "Loaded: $var_name"
        fi
    done < "$PROJECT_ROOT/.env"
    
    echo "Environment variables loaded successfully!"
else
    echo "Error: .env file not found in the project root."
    exit 1
fi

# Provide usage instructions
echo ""
echo "To use these variables in your current shell session, source this script:"
echo "$ source ./scripts/load_env.sh"
echo ""
echo "Or use the shorter syntax:"
echo "$ . ./scripts/load_env.sh"