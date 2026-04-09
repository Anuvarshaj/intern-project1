"""Stock sentiment analysis application.

Features:
1. Fetches stock price via yfinance.
2. Fetches tweets via Apify actor `apidojo/tweet-scraper`.
3. Extracts tweet text.
4. Performs sentiment analysis (Positive/Negative/Neutral).
5. Prints stock price, tweets, per-tweet sentiment, and aggregate summary.
6. Optional: creates a bar chart visualization.
"""

from __future__ import annotations

import argparse
import sys
from typing import Iterable

from agents.stock_agent import StockAgent, StockFetchError
from agents.tweet_agent import TweetAgent, TweetFetchError
from utils.sentiment import SentimentAnalyzer, SentimentResult
from utils.visualization import plot_summary


def _format_results(results: Iterable[SentimentResult]) -> str:
    """Create pretty printable lines for sentiment output."""
    lines: list[str] = []
    for idx, result in enumerate(results, start=1):
        # Keep tweet preview concise in terminal output.
        preview = result.text.replace("\n", " ").strip()
        if len(preview) > 180:
            preview = preview[:177] + "..."
        lines.append(f"{idx:02d}. [{result.label:<8}] score={result.score:>6.3f} | {preview}")
    return "\n".join(lines)


def run(symbol: str, query: str, tweet_limit: int, with_chart: bool) -> int:
    """Run end-to-end analysis workflow and return process exit code."""
    print("=" * 70)
    print(f"Stock Sentiment Analysis for {symbol.upper()}")
    print("=" * 70)

    # Step 1: stock price
    try:
        stock_data = StockAgent(symbol).fetch_price()
        print(f"\nStock Price: {stock_data.symbol} = {stock_data.price:.2f} {stock_data.currency}")
    except StockFetchError as exc:
        print(f"Error fetching stock price: {exc}", file=sys.stderr)
        return 1

    # Step 2: tweets
    try:
        tweet_agent = TweetAgent()
        tweets = tweet_agent.fetch_tweets(query=query, limit=tweet_limit)
    except TweetFetchError as exc:
        print(f"Error fetching tweets: {exc}", file=sys.stderr)
        return 1

    if not tweets:
        print("No tweets found for query. Try another query or increase limit.")
        return 0

    # Step 3+4: extract text + sentiment analysis
    analyzer = SentimentAnalyzer()
    results = [analyzer.analyze(tweet.text) for tweet in tweets]

    # Step 5: print tweets and sentiment
    print(f"\nTweets ({len(tweets)}):")
    for i, tweet in enumerate(tweets, start=1):
        url_suffix = f" | {tweet.url}" if tweet.url else ""
        print(f"{i:02d}. {tweet.text}{url_suffix}")

    print("\nSentiment per Tweet:")
    print(_format_results(results))

    summary = analyzer.summarize(results)
    print("\nOverall Sentiment Summary:")
    for label, count in summary.items():
        print(f"- {label}: {count}")

    # Optional visualization
    if with_chart:
        chart_path = plot_summary(summary)
        print(f"\nSaved sentiment chart to: {chart_path}")

    return 0


def build_parser() -> argparse.ArgumentParser:
    """Configure command-line arguments."""
    parser = argparse.ArgumentParser(description="Stock sentiment analysis using yfinance + Apify tweets")
    parser.add_argument("--symbol", default="TSLA", help="Stock ticker symbol (default: TSLA)")
    parser.add_argument(
        "--query",
        default="Tesla lang:en",
        help="Tweet search query passed to Apify actor (default: 'Tesla lang:en')",
    )
    parser.add_argument("--tweet-limit", type=int, default=10, help="Maximum tweets to fetch (default: 10)")
    parser.add_argument("--with-chart", action="store_true", help="Generate a bar chart of sentiment counts")
    return parser


if __name__ == "__main__":
    args = build_parser().parse_args()
    sys.exit(run(args.symbol, args.query, args.tweet_limit, args.with_chart))
