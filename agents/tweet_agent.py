"""Agent for fetching tweets via Apify actor runs."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests


class TweetFetchError(Exception):
    """Raised when tweets cannot be fetched from Apify."""


@dataclass
class Tweet:
    """Simple tweet representation."""

    id: str
    text: str
    url: str | None = None


class TweetAgent:
    """Fetch tweets with Apify actor `apidojo/tweet-scraper`."""

    BASE_URL = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/run-sync-get-dataset-items"

    def __init__(self, apify_token: str | None = None, timeout: int = 120) -> None:
        self.apify_token = apify_token or os.getenv("APIFY_TOKEN", "")
        self.timeout = timeout

        if not self.apify_token:
            raise TweetFetchError(
                "Missing Apify token. Set APIFY_TOKEN environment variable or pass apify_token explicitly."
            )

    def fetch_tweets(self, query: str, limit: int = 10) -> list[Tweet]:
        """
        Fetch tweets for a query string.

        Args:
            query: Search query (e.g., '$TSLA lang:en').
            limit: Maximum number of tweets to request.

        Returns:
            List of Tweet objects.

        Raises:
            TweetFetchError: If API call fails or response is malformed.
        """
        payload: dict[str, Any] = {
            "searchTerms": [query],
            "maxItems": limit,
            "sort": "Latest",
        }

        try:
            response = requests.post(
                self.BASE_URL,
                params={"token": self.apify_token},
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            items = response.json()

            tweets: list[Tweet] = []
            for item in items:
                # Apify fields can vary by actor version, so keep extraction defensive.
                text = (item.get("text") or item.get("fullText") or "").strip()
                if not text:
                    continue

                tweet_id = str(item.get("id") or item.get("tweetId") or "unknown")
                url = item.get("url")
                tweets.append(Tweet(id=tweet_id, text=text, url=url))

            return tweets
        except requests.RequestException as exc:
            raise TweetFetchError(f"Failed to fetch tweets from Apify: {exc}") from exc
        except ValueError as exc:
            raise TweetFetchError(f"Apify response is not valid JSON: {exc}") from exc
        except Exception as exc:  # pragma: no cover - fallback for unknown edge cases
            raise TweetFetchError(f"Unexpected error while processing tweets: {exc}") from exc
