# SNEL Telegram Bot Scripts

This directory contains utility scripts for managing the SNEL Telegram Bot.

## Setup Scripts

- **setup-server-env.example.sh**: Template for setting up environment variables on the server
- **setup-server-env.sh**: Script to set up environment variables on the server (create from example)
- **setup-local-env.sh**: Script to set up environment variables for local development
- **load_env.sh**: Utility to load environment variables in the current shell

## Deployment Scripts

- **check-env.sh**: Validates environment variables before deployment
- **check-server-env.sh**: Checks and helps update environment variables on the server
- **fix-venv.sh**: Fixes virtual environment issues

## Usage Instructions

### Server Environment Setup

1. Copy `setup-server-env.example.sh` to `setup-server-env.sh`
   ```bash
   cp setup-server-env.example.sh setup-server-env.sh
   ```

2. Edit `setup-server-env.sh` with your API keys and credentials

3. Run the script to set up environment on the server
   ```bash
   ./setup-server-env.sh
   ```

### Local Environment Setup

1. Set up local environment
   ```bash
   ./setup-local-env.sh
   ```

2. Load environment variables
   ```bash
   source load_env.sh
   ```

### Checking Environment Variables

- To check environment variables on the server:
  ```bash
  ./check-server-env.sh
  ```

- To check local environment variables:
  ```bash
  ./check-env.sh
  ```

## Notes

- Scripts with sensitive information (API keys, tokens) are gitignored
- Always use the `.example` versions as templates
- Make scripts executable if needed: `chmod +x script_name.sh`