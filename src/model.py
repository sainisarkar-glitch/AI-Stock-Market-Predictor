from typing import Dict
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from xgboost import XGBRegressor


def train_prediction_model(data: pd.DataFrame) -> Dict[str, float]:
    features = ["Open", "High", "Low", "Close", "Volume", "MA_20", "MA_50", "Daily_Return", "RSI"]

    X = data[features]
    y = data["Target"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    model = XGBRegressor(
        n_estimators=120,
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    )

    model.fit(X_train, y_train)

    test_predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, test_predictions)

    latest_features = X.tail(1)
    next_price_prediction = model.predict(latest_features)[0]

    return {
        "prediction": float(next_price_prediction),
        "mae": float(mae)
    }
