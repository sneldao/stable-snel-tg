# Using direnv for Automatic Environment Variable Management

## What is direnv?

`direnv` is an environment switcher for the shell. It automatically loads and unloads environment variables depending on the current directory. This is perfect for project-specific environment variables stored in `.env` files.

## Installation

### macOS
```bash
brew install direnv
```

### Ubuntu/Debian
```bash
sudo apt-get install direnv
```

### From source
```bash
git clone https://github.com/direnv/direnv.git
cd direnv
make install
```

## Shell Setup

Add the following line to your shell configuration file (`.bashrc`, `.zshrc`, etc.):

### For Bash
```bash
eval "$(direnv hook bash)"
```

### For Zsh
```bash
eval "$(direnv hook zsh)"
```

### For Fish
```bash
direnv hook fish | source
```

Restart your shell or source your configuration file:
```bash
source ~/.bashrc  # or ~/.zshrc
```

## Usage with Your Project

1. Navigate to your project directory:
   ```bash
   cd stable-snel-tg
   ```

2. Create a `.envrc` file that loads your `.env` variables:
   ```bash
   echo 'dotenv' > .envrc
   ```

3. Allow the `.envrc` file (this is a security feature):
   ```bash
   direnv allow
   ```

Now, whenever you enter the `stable-snel-tg` directory, direnv will automatically load all environment variables from your `.env` file. When you leave the directory, those variables will be unloaded.

## Testing Your API Keys

With direnv set up, you can test your API keys without any additional steps to load environment variables:

```bash
# Test Venice API
curl -s "https://api.venice.ai/api/v1/models" \
  -H "Authorization: Bearer $VENICE_API_KEY" | jq

# Test Gemini API
curl -s "https://generativelanguage.googleapis.com/v1/models?key=$GEMINI_API_KEY" | jq
```

## Advanced Usage

### Using Different .env Files

You can specify which `.env` file to load:
```bash
echo 'dotenv .env.development' > .envrc
direnv allow
```

### Combining with Shell Commands

You can include other shell commands in your `.envrc`:
```bash
echo 'dotenv
echo "Environment loaded for $(pwd)"
export EXTRA_VAR="something"' > .envrc
direnv allow
```

### Layered Environments

direnv supports directory hierarchy, allowing parent directory configurations to cascade down to subdirectories.

## Troubleshooting

If your environment variables aren't loading:

1. Check that direnv is properly installed: `which direnv`
2. Verify that the hook is in your shell config: `grep direnv ~/.zshrc`
3. Make sure your `.envrc` file is allowed: `direnv status`
4. Check your `.env` file format for any syntax errors

## References

- [direnv Official Documentation](https://direnv.net/)
- [direnv GitHub Repository](https://github.com/direnv/direnv)