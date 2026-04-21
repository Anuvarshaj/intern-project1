"""Validation helpers for CLI and order inputs."""

from __future__ import annotations

from typing import Optional

VALID_SIDES = {"BUY", "SELL"}
VALID_TYPES = {"MARKET", "LIMIT"}


class ValidationError(ValueError):
    """Raised when an input value is invalid."""


def validate_symbol(symbol: str) -> str:
    if not symbol or not symbol.strip():
        raise ValidationError("symbol is required")

    symbol = symbol.strip().upper()
    if not symbol.isalnum():
        raise ValidationError("symbol must be alphanumeric (e.g., BTCUSDT)")
    return symbol


def validate_side(side: str) -> str:
    if side is None:
        raise ValidationError("side is required")

    normalized = side.strip().upper()
    if normalized not in VALID_SIDES:
        raise ValidationError(f"side must be one of: {', '.join(sorted(VALID_SIDES))}")
    return normalized


def validate_order_type(order_type: str) -> str:
    if order_type is None:
        raise ValidationError("type is required")

    normalized = order_type.strip().upper()
    if normalized not in VALID_TYPES:
        raise ValidationError(f"type must be one of: {', '.join(sorted(VALID_TYPES))}")
    return normalized


def validate_quantity(quantity: float) -> float:
    try:
        value = float(quantity)
    except (TypeError, ValueError) as exc:
        raise ValidationError("quantity must be a number") from exc

    if value <= 0:
        raise ValidationError("quantity must be greater than 0")
    return value


def validate_price(price: Optional[float], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("price is required for LIMIT orders")
        try:
            numeric_price = float(price)
        except (TypeError, ValueError) as exc:
            raise ValidationError("price must be a number") from exc

        if numeric_price <= 0:
            raise ValidationError("price must be greater than 0")
        return numeric_price

    # MARKET order: ignore provided price but keep robust behavior.
    if price is None:
        return None

    try:
        numeric_price = float(price)
    except (TypeError, ValueError) as exc:
        raise ValidationError("price must be a number") from exc

    if numeric_price <= 0:
        raise ValidationError("price must be greater than 0")
    return numeric_price
