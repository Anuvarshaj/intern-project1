"""Agent for fetching stock market data."""

from __future__ import annotations

from dataclasses import dataclass

import yfinance as yf


class StockFetchError(Exception):
    """Raised when stock information cannot be fetched."""


@dataclass
class StockPrice:
    """Simple data container for stock information."""

    symbol: str
    price: float
    currency: str


class StockAgent:
    """Fetches stock information using yfinance."""

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol.upper().strip()

    def fetch_price(self) -> StockPrice:
        """
        Fetch latest stock price.

        Returns:
            StockPrice containing symbol, price, and currency.

        Raises:
            StockFetchError: If data is unavailable or malformed.
        """
        try:
            ticker = yf.Ticker(self.symbol)
            # `fast_info` is generally quicker and sufficient for a simple quote.
            fast_info = ticker.fast_info
            last_price = fast_info.get("last_price")
            currency = fast_info.get("currency") or "USD"

            if last_price is None:
                # Fallback to historical close if real-time value is unavailable.
                history = ticker.history(period="1d")
                if history.empty:
                    raise StockFetchError(f"No market data available for symbol '{self.symbol}'.")
                last_price = float(history["Close"].iloc[-1])

            return StockPrice(symbol=self.symbol, price=float(last_price), currency=currency)
        except StockFetchError:
            raise
        except Exception as exc:  # pragma: no cover - defensive catch with clear context
            raise StockFetchError(f"Failed to fetch stock price for '{self.symbol}': {exc}") from exc
