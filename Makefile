# SNEL Telegram Bot Makefile

.PHONY: setup install run test lint clean docker-build docker-run help

# Default target
help:
	@echo "SNEL Telegram Bot Make Commands"
	@echo "==============================="
	@echo "setup         : Set up virtual environment and install dependencies"
	@echo "install       : Install dependencies"
	@echo "run           : Run the bot locally"
	@echo "test          : Run all tests"
	@echo "lint          : Run linting checks"
	@echo "clean         : Clean up cache, logs, and temporary files"
	@echo "docker-build  : Build Docker container"
	@echo "docker-run    : Run bot using Docker"
	@echo "help          : Show this help message"

# Setup virtual environment and install dependencies
setup:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements-local.txt

# Install dependencies
install:
	pip install -r requirements.txt

# Run the bot
run:
	python bot.py

# Run tests
test:
	python tests/test_all_handlers.py
	python tests/test_coingecko.py
	python tests/test_news_service.py
	python tests/test_ai_local.py

# Lint the code
lint:
	flake8 telegram
	isort telegram

# Clean up cache and temporary files
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.pyc" -delete
	find . -type d -name ".cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".metrics" -exec rm -rf {} +
	find . -type d -name "logs/*.log" -exec rm -f {} +

# Docker commands
docker-build:
	docker build -t snel-telegram-bot .

docker-run:
	docker-compose up -d