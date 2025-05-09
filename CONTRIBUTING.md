# Contributing to SNEL Telegram Bot

Thank you for considering contributing to the SNEL Telegram Bot project! This document outlines the process for contributing and guidelines to follow.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a branch for your feature or bugfix
4. Make your changes
5. Test your changes
6. Push your branch to your fork
7. Submit a pull request

## Development Environment

### Prerequisites

- Python 3.9+
- pip
- virtualenv or venv

### Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

3. Install dependencies:
   ```
   pip install -r requirements-local.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in the required API keys and credentials

## Pull Request Process

1. Update the README.md with details of changes to the interface, if applicable
2. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent
3. The PR will be merged once you have the sign-off of at least one maintainer

## Coding Standards

- Follow PEP 8 style guide for Python code
- Use descriptive variable names and function names
- Include docstrings for all functions, classes, and modules
- Keep functions small and focused on a single task
- Add comments for complex logic

### Code Structure

- New handlers should be placed in the `telegram/handlers/` directory
- New services should be placed in the `telegram/services/` directory
- Utility functions should be placed in the `telegram/utils/` directory

## Testing

- Add unit tests for new functionality
- Ensure all tests pass before submitting a pull request
- Run tests using:
  ```
  python -m pytest
  ```

## Documentation

- Update documentation for new features or changes to existing functionality
- Include code examples where appropriate
- Keep language clear and accessible

## Utility Features

When extending the bot's utility features, please follow these guidelines:

### Caching

- Use the `@cached` decorator for functions that fetch external data
- Set appropriate TTL values based on how frequently the data changes
- Do not cache user-specific data without considering privacy implications

### Error Handling and Retries

- Use the `@retry` decorator for functions that interact with external APIs
- Set appropriate `max_retries` and `initial_delay` values
- Add specific error handling for known issues

### Rate Limiting

- Register a rate limiter for new API services
- Set appropriate tokens per second based on API documentation
- Apply rate limiting to all external API calls

## Thank You!

Your contributions are what make the open-source community such an amazing place to learn, inspire, and create. We appreciate your help in making the SNEL Telegram Bot better!