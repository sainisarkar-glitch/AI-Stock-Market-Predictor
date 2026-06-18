from textblob import TextBlob


def simple_sentiment_score(text: str) -> float:
    if not text.strip():
        return 0.0

    blob = TextBlob(text)
    return float(blob.sentiment.polarity)
