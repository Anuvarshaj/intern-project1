# Stock Sentiment Analysis

A clean Python project that:

1. Fetches stock price using **yfinance** (e.g., Tesla / TSLA)
2. Fetches tweets using **Apify** actor `apidojo/tweet-scraper`
3. Extracts tweet text
4. Performs sentiment analysis (**Positive / Negative / Neutral**)
5. Prints:
   - Stock price
   - Tweets
   - Sentiment per tweet
   - Overall sentiment summary
6. Optionally renders a simple bar chart

## Project Structure

```text
.
├── agents/
│   ├── stock_agent.py
│   └── tweet_agent.py
├── utils/
│   ├── sentiment.py
│   └── visualization.py
├── main.py
└── requirements.txt
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Set your Apify API token:

```bash
export APIFY_TOKEN="your_apify_token_here"
```

## Run

```bash
python main.py --symbol TSLA --query "Tesla lang:en" --tweet-limit 10
```

Optional chart:

```bash
python main.py --symbol TSLA --query "Tesla lang:en" --tweet-limit 10 --with-chart
```

## Notes

- Errors are handled with clear messages and custom exceptions.
- Sentiment analysis uses VADER with standard thresholds:
  - `>= 0.05`: Positive
  - `<= -0.05`: Negative
  - otherwise: Neutral
