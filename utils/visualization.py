"""Visualization helper for sentiment summary."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def plot_summary(summary: dict[str, int], output_path: str = "sentiment_summary.png") -> str:
    """Generate a basic bar chart for sentiment counts."""
    labels = list(summary.keys())
    values = [summary[label] for label in labels]

    plt.figure(figsize=(7, 4))
    bars = plt.bar(labels, values, color=["#4caf50", "#f44336", "#9e9e9e"])
    plt.title("Tweet Sentiment Summary")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")

    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(value), ha="center", va="bottom")

    plt.tight_layout()
    path = Path(output_path)
    plt.savefig(path)
    plt.close()
    return str(path)
