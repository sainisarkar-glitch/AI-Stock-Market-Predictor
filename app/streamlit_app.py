import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import streamlit as st
import plotly.graph_objects as go

from src.data_loader import load_stock_data
from src.features import add_technical_indicators
from src.model import train_prediction_model
from src.recommendation import generate_signal
from src.sentiment import simple_sentiment_score


st.set_page_config(page_title="AI Stock Market Predictor", layout="wide")

st.title("AI Stock Market Predictor")
st.write("Machine learning stock prediction dashboard with technical indicators, sentiment score, and buy/sell/hold recommendation.")

ticker = st.sidebar.text_input("Enter stock ticker", value="AAPL")
period = st.sidebar.selectbox("Select period", ["6mo", "1y", "2y", "5y"], index=1)

news_text = st.sidebar.text_area(
    "Paste market news or company news for sentiment",
    value="The company reported strong revenue growth and positive future guidance."
)

if st.sidebar.button("Run Prediction"):
    data = load_stock_data(ticker, period)
    data = add_technical_indicators(data)

    model_result = train_prediction_model(data)
    latest_close = float(data["Close"].iloc[-1])
    predicted_price = float(model_result["prediction"])
    sentiment = simple_sentiment_score(news_text)
    signal = generate_signal(latest_close, predicted_price, sentiment)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest Close", f"${latest_close:.2f}")
    col2.metric("Predicted Next Price", f"${predicted_price:.2f}")
    col3.metric("Sentiment Score", f"{sentiment:.2f}")
    col4.metric("Signal", signal)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data["Close"], name="Close Price"))
    fig.add_trace(go.Scatter(x=data.index, y=data["MA_20"], name="20-Day MA"))
    fig.add_trace(go.Scatter(x=data.index, y=data["MA_50"], name="50-Day MA"))
    fig.update_layout(title=f"{ticker} Price Trend", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Model Performance")
    st.write(f"Mean Absolute Error: {model_result['mae']:.2f}")

    st.subheader("Recent Data")
    st.dataframe(data.tail(20))
else:
    st.info("Enter a ticker and click Run Prediction.")
