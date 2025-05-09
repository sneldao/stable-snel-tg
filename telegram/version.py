"""
# SNEL Telegram Bot version information

__version__ = '1.1.0'
__author__ = 'Papa Jams'
__email__ = 'papajams@example.com'
__license__ = 'MIT'
__copyright__ = '2023-2024'
__status__ = 'Beta'

# Version history
VERSION_HISTORY = {
    '1.0.0': 'Initial release with basic crypto information features',
    '1.1.0': 'Added caching system, error handling with retries, rate limiting, and metrics'
}

def get_version_info():
    """Return formatted version information string."""
    return f"SNEL Telegram Bot v{__version__} ({__status__})"

def get_version_history():
    """Return version history as a formatted string."""
    history = ["Version History:"]
    for version, description in VERSION_HISTORY.items():
        history.append(f"- v{version}: {description}")
    return "\n".join(history)
"""