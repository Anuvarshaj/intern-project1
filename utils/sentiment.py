"""Utilities for sentiment analysis."""

from __future__ import annotations

from dataclasses import dataclass

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


@dataclass
class SentimentResult:
    """Sentiment output for a single text."""

    text: str
    label: str
    score: float


class SentimentAnalyzer:
    """Performs sentiment classification using VADER polarity score."""

    def __init__(self) -> None:
        self._analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> SentimentResult:
        """Analyze one text and return a label with compound score."""
        compound = self._analyzer.polarity_scores(text)["compound"]

        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        return SentimentResult(text=text, label=label, score=compound)

    @staticmethod
    def summarize(results: list[SentimentResult]) -> dict[str, int]:
        """Create aggregate sentiment counts."""
        summary = {"Positive": 0, "Negative": 0, "Neutral": 0}
        for result in results:
            summary[result.label] += 1
        return summary
