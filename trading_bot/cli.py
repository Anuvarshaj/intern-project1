"""CLI entry point for the simplified trading bot."""

from __future__ import annotations

import argparse
import logging
import sys

from bot.client import TradingAPIClient
from bot.logging_config import setup_logging
from bot.orders import (
    build_order_request,
    format_order_response,
    format_order_summary,
    place_order_with_fallback,
)
from bot.validators import ValidationError

logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simplified Trading Bot CLI")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g., BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Limit price (required for LIMIT orders)")
    parser.add_argument(
        "--fail-rate",
        type=float,
        default=0.2,
        help="Simulated API failure rate from 0.0 to 1.0 (default: 0.2)",
    )
    return parser.parse_args()


def validate_fail_rate(fail_rate: float) -> float:
    if not 0.0 <= fail_rate <= 1.0:
        raise ValidationError("fail-rate must be between 0.0 and 1.0")
    return fail_rate


def main() -> int:
    setup_logging()

    try:
        args = parse_args()
        fail_rate = validate_fail_rate(args.fail_rate)

        order = build_order_request(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )

        client = TradingAPIClient(fail_rate=fail_rate)
        result = place_order_with_fallback(client, order)

        print(format_order_summary(order))
        print()
        print(format_order_response(result.response))

        if result.mock_used:
            print("\n[Mock Mode] API unavailable. Simulated response returned.")

        logger.info("CLI run complete. mock_used=%s", result.mock_used)
        return 0

    except ValidationError as exc:
        logger.error("Validation error: %s", exc)
        print(f"Input Error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 - top-level guard for graceful CLI failure
        logger.exception("Unexpected runtime error: %s", exc)
        print(f"Runtime Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
