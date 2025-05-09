#!/bin/bash

# Function to load environment variables from .env file
# Usage: Add this to your ~/.bashrc or ~/.zshrc file

load_env() {
    local env_file="${1:-.env}"
    
    if [[ ! -f "$env_file" ]]; then
        echo "Error: $env_file not found"
        return 1
    fi
    
    echo "Loading environment variables from $env_file"
    
    # Use set -a to automatically export all variables
    set -a
    source "$env_file"
    set +a
    
    echo "Environment variables loaded successfully"
}

# Instructions for installation
# 
# 1. Copy this function to your shell configuration file:
#    For bash: ~/.bashrc
#    For zsh:  ~/.zshrc
#
# 2. Reload your shell configuration:
#    $ source ~/.bashrc
#    or
#    $ source ~/.zshrc
#
# 3. Use the function in any directory:
#    $ load_env            # loads .env in current directory
#    $ load_env .env.dev   # loads custom env file

# Example usage for Venice and Gemini API testing
#
# $ cd stable-snel-tg
# $ load_env
# $ curl -s "https://api.venice.ai/api/v1/models" -H "Authorization: Bearer $VENICE_API_KEY" | jq
#
# To make variables persist in current session only:
# $ set -a; source .env; set +a