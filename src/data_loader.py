import yfinance as yf
import pandas as pd


def load_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    data = yf.download(ticker, period=period, auto_adjust=True, progress=False)

    if data.empty:
        raise ValueError("No stock data found. Please check the ticker symbol.")

    data = data.dropna()
    return data
