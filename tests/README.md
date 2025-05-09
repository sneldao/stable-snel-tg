# SNEL Bot Tests

This directory contains various test scripts for the SNEL Telegram bot.

## Test Files

- **test_ai.py**: Tests the AI integration features independently
- **test_ai_features.py**: A comprehensive test bot focused on SNEL's AI capabilities
- **test_api_keys.sh**: Shell script to test API keys (Venice and Gemini)
- **test_bot.py**: A simplified test bot for basic functionality
- **test_with_dotenv.js**: JavaScript test for environment variable loading

## Running Tests

From the project root directory:

```bash
# Test AI integration
python3 tests/test_ai.py

# Run the AI-focused test bot
python3 tests/test_ai_features.py

# Test API keys
bash tests/test_api_keys.sh

# Run the simplified test bot
python3 tests/test_bot.py
```

## Environment Setup

Make sure to set up your environment variables before running tests:

```bash
source scripts/load_env.sh
```

Or use the `.env` file directly with the dotenv package in Python scripts.