# SNEL Bot Utility Scripts

This directory contains utility scripts for managing the SNEL Telegram bot environment and development workflow.

## Available Scripts

- **load_env.sh**: Loads environment variables from .env file into your shell session
- **fix-venv.sh**: Repairs Python virtual environment issues
- **shell_integration.sh**: Provides shell functions for common bot operations

## Usage Instructions

### Loading Environment Variables

The `load_env.sh` script loads all environment variables from your .env file:

```bash
# From project root
source scripts/load_env.sh

# Or the shorter syntax
. scripts/load_env.sh
```

### Fixing Virtual Environment

If you encounter issues with your Python virtual environment:

```bash
# From project root
bash scripts/fix-venv.sh
```

### Shell Integration

To add helpful shell functions to your environment:

```bash
# Source the shell integration file
source scripts/shell_integration.sh

# Then you can use the functions
load_env
```

## Best Practices

- Always load environment variables before running the bot or tests
- If you encounter dependency issues, try the fix-venv script
- For regular development, consider using the direnv approach documented in docs/direnv_instructions.md