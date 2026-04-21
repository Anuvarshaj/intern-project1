"""API interaction layer for trading bot.

This module intentionally simulates API behavior while demonstrating how to
handle network/API failures and fall back to mock responses.
"""

from __future__ import annotations

import logging
import random
import time
from dataclasses import dataclass
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class APIClientError(RuntimeError):
    """Raised when the API client cannot execute the request."""


@dataclass
class OrderRequest:
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float] = None


class TradingAPIClient:
    """Simple client abstraction for placing orders.

    In a real implementation, this class would make HTTP requests to an
    exchange API. Here we keep it lightweight and deterministic enough for a
    coding exercise.
    """

    def __init__(self, fail_rate: float = 0.2, random_seed: Optional[int] = None) -> None:
        self.fail_rate = fail_rate
        self._rng = random.Random(random_seed)

    def place_order(self, order: OrderRequest) -> Dict[str, object]:
        """Attempt to place order via API.

        Raises:
            APIClientError: if a simulated network/API failure occurs.
        """
        payload = {
            "symbol": order.symbol,
            "side": order.side,
            "type": order.order_type,
            "quantity": order.quantity,
            "price": order.price,
        }
        logger.info("Sending API request: %s", payload)

        # Simulate latency and occasional transient failures.
        time.sleep(0.05)
        if self._rng.random() < self.fail_rate:
            error_message = "simulated network/API failure"
            logger.error("API request failed: %s", error_message)
            raise APIClientError(error_message)

        avg_price = order.price if order.order_type == "LIMIT" else round(self._rng.uniform(10000, 70000), 2)
        response = {
            "orderId": self._rng.randint(100000, 999999),
            "symbol": order.symbol,
            "side": order.side,
            "type": order.order_type,
            "status": "FILLED" if order.order_type == "MARKET" else "NEW",
            "executedQty": order.quantity if order.order_type == "MARKET" else 0.0,
            "avgPrice": avg_price if order.order_type == "MARKET" else 0.0,
        }
        logger.info("API response received: %s", response)
        return response


def simulated_order_response(order: OrderRequest) -> Dict[str, object]:
    """Fallback response used when real API request fails."""
    logger.warning("Using mock trading mode fallback")

    fallback_avg_price = order.price if order.order_type == "LIMIT" else 50000.0
    response = {
        "orderId": int(time.time() * 1000),
        "symbol": order.symbol,
        "side": order.side,
        "type": order.order_type,
        "status": "SIMULATED",
        "executedQty": order.quantity if order.order_type == "MARKET" else 0.0,
        "avgPrice": fallback_avg_price if order.order_type == "MARKET" else (order.price or 0.0),
    }
    logger.info("Mock response generated: %s", response)
    return response
