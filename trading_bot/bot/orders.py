"""Business logic for order creation and placement."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Optional

from bot.client import APIClientError, OrderRequest, TradingAPIClient, simulated_order_response
from bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)

logger = logging.getLogger(__name__)


@dataclass
class PlaceOrderResult:
    response: Dict[str, object]
    mock_used: bool


def build_order_request(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float],
) -> OrderRequest:
    """Validate and normalize user input into a structured order request."""
    validated_symbol = validate_symbol(symbol)
    validated_side = validate_side(side)
    validated_type = validate_order_type(order_type)
    validated_quantity = validate_quantity(quantity)
    validated_price = validate_price(price, validated_type)

    return OrderRequest(
        symbol=validated_symbol,
        side=validated_side,
        order_type=validated_type,
        quantity=validated_quantity,
        price=validated_price,
    )


def place_order_with_fallback(client: TradingAPIClient, order: OrderRequest) -> PlaceOrderResult:
    """Place an order and use a mock response if API placement fails."""
    try:
        api_response = client.place_order(order)
        return PlaceOrderResult(response=api_response, mock_used=False)
    except APIClientError as exc:
        logger.exception("API failure encountered, switching to mock mode: %s", exc)
        mock_response = simulated_order_response(order)
        return PlaceOrderResult(response=mock_response, mock_used=True)


def format_order_summary(order: OrderRequest) -> str:
    price_part = f"{order.price}" if order.price is not None else "N/A"
    return (
        "Order Summary\n"
        f"- Symbol: {order.symbol}\n"
        f"- Side: {order.side}\n"
        f"- Type: {order.order_type}\n"
        f"- Quantity: {order.quantity}\n"
        f"- Price: {price_part}"
    )


def format_order_response(response: Dict[str, object]) -> str:
    return (
        "Order Response\n"
        f"- orderId: {response.get('orderId')}\n"
        f"- status: {response.get('status')}\n"
        f"- executedQty: {response.get('executedQty')}\n"
        f"- avgPrice: {response.get('avgPrice')}"
    )
