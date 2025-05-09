# Changelog

All notable changes to the SNEL Telegram Bot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced caching system with disk persistence
- Circuit breaker pattern for improved error handling
- Rate limiting for external API requests
- Comprehensive metrics and monitoring dashboard
- TokenBucketLimiter for precise API rate control
- Automated metrics collection and reporting
- Cache statistics and performance tracking

### Changed
- Improved retry mechanism with exponential backoff
- Enhanced crypto service now uses circuit breaker and rate limiting
- Startup process now initializes all background tasks properly
- Better handling of rate limits and temporary errors

### Fixed
- Potential memory issues with unbounded cache growth
- Cascading failures when external services are unavailable
- Thundering herd problem with multiple concurrent requests

## [1.0.0] - 2023-12-15

### Added
- Initial release of SNEL Telegram Bot
- Basic command handlers for cryptocurrency information
- Integration with CoinGecko API
- Price and market data commands
- Technical analysis features
- News and community information
- AI-powered analysis via Gemini API
- Stablecoin specific features via Venice API
- Docker deployment support

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)