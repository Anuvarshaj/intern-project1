# Simplified Trading Bot CLI

A modular Python 3 command-line application that places simplified MARKET and LIMIT orders.

## Features

- MARKET and LIMIT order support
- BUY and SELL side support
- Input validation for symbol, side, type, quantity, and price
- Separate API client layer (`bot/client.py`)
- Fallback mock response if API call fails
- Logging to `bot.log` with timestamps and log levels
- Clear terminal output with order summary and response

## Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── logging_config.py
│   ├── orders.py
│   └── validators.py
├── cli.py
├── README.md
└── requirements.txt
```

## Setup

```bash
cd trading_bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Market Order

```bash
python3 cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Limit Order

```bash
python3 cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000
```

### Force mock mode (demo)

Use `--fail-rate 1.0` to intentionally simulate API failure:

```bash
python3 cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --fail-rate 1.0
```

## Notes

- For LIMIT orders, `--price` is required.
- All requests, responses, and errors are logged in `bot.log`.
- This app uses a simulated API layer for demonstration and can be extended to real exchange endpoints.
