import pandas as pd
from prophet import Prophet
import joblib

MODEL_PATH = "models/traffic_forecast.pkl"

def train_forecasting_model(csv_path):

    df = pd.read_csv(csv_path)

    forecast_df = pd.DataFrame()

    forecast_df["ds"] = pd.to_datetime(df["timestamp"])
    forecast_df["y"] = df["total"]

    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True
    )

    model.fit(forecast_df)

    future = model.make_future_dataframe(
        periods=6,
        freq="h"
    )

    forecast = model.predict(future)

    print("\nForecast Result:")
    print(forecast[["ds", "yhat"]].tail(6))

    joblib.dump(model, MODEL_PATH)

    print(f"\nForecast model saved: {MODEL_PATH}")

    return forecast

if __name__ == "__main__":

    train_forecasting_model(
        "data/processed/ml_input/part-00000*.csv"
    )