#!/bin/bash

# Get script directory and navigate to project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." &> /dev/null && pwd )"

# Load environment variables from .env file
if [ -f "$PROJECT_ROOT/.env" ]; then
    export $(cat "$PROJECT_ROOT/.env" | grep -v '^#' | xargs)
    echo "Loaded environment variables from .env file"
else
    echo "Error: .env file not found"
    exit 1
fi

# Check if API keys are loaded
echo "Venice API key length: ${#VENICE_API_KEY}"
echo "Gemini API key length: ${#GEMINI_API_KEY}"

# Test Venice API - Models List
echo -e "\n\033[1;34m==== Testing Venice API - Models List ====\033[0m"
curl -s https://api.venice.ai/api/v1/models \
  -H "Authorization: Bearer $VENICE_API_KEY" | jq .data[0]

# Test Venice API - Chat Completion
echo -e "\n\033[1;34m==== Testing Venice API - Chat Completion ====\033[0m"
curl -s https://api.venice.ai/api/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VENICE_API_KEY" \
  -d '{
    "model": "llama-3.2-3b",
    "messages": [{"role": "user", "content": "Hello, can you tell me what day it is today?"}],
    "temperature": 0.7
  }' | jq

# Test Gemini API - Models List
echo -e "\n\033[1;34m==== Testing Gemini API - Models List ====\033[0m"
curl -s "https://generativelanguage.googleapis.com/v1/models?key=$GEMINI_API_KEY" | jq

# Test Gemini API - Chat Completion
echo -e "\n\033[1;34m==== Testing Gemini API - Chat Completion ====\033[0m"
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=$GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "parts": [
          {"text": "Hello, can you tell me what day it is today?"}
        ]
      }
    ]
  }' | jq