"""Keyword research module (mock)."""
from typing import List


def fetch_keywords(topic: str) -> List[str]:
    """Return a list of keywords based on a topic.

    This mock implementation uses simple heuristics.
    """
    base = topic.lower().replace(" ", "-")
    keywords = [f"{base}", f"best-{base}", f"{base}-guide", f"{base}-tips"]
    return keywords
