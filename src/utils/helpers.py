# src/utils/helpers.py

import re
import logging

def clean_text(text: str) -> str:
    """Remove extra whitespace and line breaks from text."""
    # Example: Remove extra whitespace and special characters
    return re.sub(r'\s+', ' ', text).strip()

def safe_get(d, key, default=""):
    """Safely get a key from a dictionary, with default fallback."""
    try:
        return d[key] if key in d and d[key] is not None else default
    except Exception:
        return default

def format_currency(amount: float, currency: str = "USD") -> str:
    """Return a formatted string for currency values."""
    return f"{currency} {amount:,.2f}"

def setup_logging(log_file="app.log"):
    """Set up logging for the application."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s"
    )

def validate_url(url: str) -> bool:
    """Simple URL validator."""
    # Simple URL validation
    return bool(re.match(r'^https?://', url))
