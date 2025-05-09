# SNEL Telegram Bot Tests

This directory contains tests for the SNEL Telegram Bot.

## Test Files

- **test_ai.py**: Tests for the AI integration (Gemini)
- **test_ai_features.py**: Tests for specific AI features and capabilities
- **test_ai_local.py**: Local tests for AI functionality without external dependencies
- **test_all_handlers.py**: Integration tests for all bot command handlers
- **test_api_keys.sh**: Shell script to verify API keys are properly configured
- **test_bot.py**: Basic bot functionality tests
- **test_coingecko.py**: Tests for CoinGecko API integration
- **test_news_service.py**: Tests for the news service functionality
- **test_with_dotenv.js**: JavaScript tests for environment variable loading

## Running Tests

### Running All Tests

```bash
# From the project root
pytest tests/
```

### Running Specific Tests

```bash
# From the project root
pytest tests/test_ai.py
python tests/test_ai_local.py
python tests/test_all_handlers.py
```

### Running Shell Tests

```bash
# From the project root
bash tests/test_api_keys.sh
```

## Adding New Tests

When adding new tests, please follow these guidelines:

1. Name test files with the prefix `test_`
2. Use descriptive names for test functions (`test_get_price_returns_valid_data`)
3. Include docstrings explaining what each test verifies
4. Mock external API dependencies when appropriate
5. Clean up any test data or state after tests complete

## Test Categories

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test how components work together
- **Functional Tests**: Test end-to-end functionality
- **API Tests**: Test external API integrations

## Running Tests with Docker

```bash
# From the project root
docker-compose run --rm app pytest tests/
```