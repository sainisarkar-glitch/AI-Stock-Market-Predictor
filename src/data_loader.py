import pandas as pd
from pathlib import Path
import yfinance as yf


def load_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    data_path = Path("data") / f"{ticker.upper().replace('.CSV', '')}.csv"

    if data_path.exists():
        data = pd.read_csv(data_path)
        data["Date"] = pd.to_datetime(data["Date"])
        data = data.set_index("Date")
        return data.dropna()

    data = yf.download(ticker.upper(), period=period, auto_adjust=True, progress=False)

    if data.empty:
        raise ValueError("No stock data found. Use ticker like TSLA or add data/TSLA.csv")

    return data.dropna()
