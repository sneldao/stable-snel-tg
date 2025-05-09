# Using dotenv-cli for Environment Variables

## Installation

Install the `dotenv-cli` package globally:

```bash
npm install -g dotenv-cli
```

## Basic Usage

The `dotenv-cli` tool allows you to run commands with environment variables loaded from your `.env` file:

```bash
# Run a command with env vars from .env
dotenv -- your-command-here

# Example: Running a curl command with loaded env vars
dotenv -- curl -s "https://api.venice.ai/api/v1/models" -H "Authorization: Bearer $VENICE_API_KEY" | jq
```

## Running Scripts

You can also use `dotenv-cli` to run scripts with environment variables loaded:

```bash
# Run a script with env vars from .env
dotenv -- ./your-script.sh

# Example: Running a Node.js script
dotenv -- node your-script.js
```

## Using Custom .env Files

If you have different environment files for different environments:

```bash
# Specify a custom .env file
dotenv -e .env.development -- your-command

# Load multiple .env files (later files take precedence)
dotenv -e .env -e .env.local -- your-command
```

## Shell Integration

For a more permanent solution, you can add a function to your shell configuration file (`.bashrc`, `.zshrc`, etc.):

```bash
# Add this to your shell config
function loadenv() {
  set -a
  [ -f .env ] && . .env
  set +a
}
```

Then use it in any directory with a `.env` file:

```bash
cd your-project
loadenv
echo $YOUR_ENV_VARIABLE
```

## For Your Project

To test your API keys in the project:

```bash
cd stable-snel-tg
dotenv -- curl -s "https://api.venice.ai/api/v1/models" -H "Authorization: Bearer $VENICE_API_KEY" | jq

# Or run your test script
dotenv -- ./test_api_keys.sh
```