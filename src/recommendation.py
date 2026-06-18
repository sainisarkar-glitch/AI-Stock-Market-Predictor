def generate_signal(latest_close: float, predicted_price: float, sentiment_score: float) -> str:
    expected_change = (predicted_price - latest_close) / latest_close

    if expected_change > 0.015 and sentiment_score >= 0:
        return "BUY"
    elif expected_change < -0.015 and sentiment_score <= 0:
        return "SELL"
    else:
        return "HOLD"
