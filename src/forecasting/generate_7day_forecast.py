from pathlib import Path

import numpy as np
import pandas as pd
import xgboost as xgb

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "forecasting_features.parquet"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "xgboost_demand_forecast_log.json"
)

OUTPUT_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "forecasting"
    / "forecast_7_days.csv"
)


FEATURES = [
    "lag_1",
    "lag_7",
    "lag_14",
    "lag_28",
    "rolling_mean_7",
    "rolling_mean_14",
    "rolling_mean_28",
    "rolling_std_7",
    "rolling_max_7",
    "month",
    "day_of_week",
    "is_weekend",
]


print("Loading forecasting data...")

df = pd.read_parquet(DATA_PATH)

df["date"] = pd.to_datetime(df["date"])

print(f"Rows: {len(df):,}")
print(f"Products: {df['product_id'].nunique():,}")


print("\nLoading trained model...")

model = xgb.XGBRegressor()
model.load_model(MODEL_PATH)

print("Model loaded successfully.")


# Last available date in the dataset
last_date = df["date"].max()

print(f"\nLast historical date: {last_date.date()}")


# Future dates
future_dates = pd.date_range(
    start=last_date + pd.Timedelta(days=1),
    periods=7,
    freq="D",
)


products = (
    df[
        [
            "product_id",
            "product_name",
        ]
    ]
    .drop_duplicates("product_id")
)


# Create product × future-date combinations
future = products.assign(key=1).merge(
    pd.DataFrame(
        {
            "date": future_dates,
            "key": 1,
        }
    ),
    on="key",
).drop(columns="key")


# Calendar features
future["year"] = future["date"].dt.year
future["month"] = future["date"].dt.month
future["day"] = future["date"].dt.day
future["day_of_week"] = future["date"].dt.dayofweek
future["week_of_year"] = (
    future["date"]
    .dt.isocalendar()
    .week
    .astype(int)
)
future["quarter"] = future["date"].dt.quarter
future["is_weekend"] = future["day_of_week"].isin([5, 6])


# Historical demand lookup
history = df[
    [
        "product_id",
        "date",
        "demand",
    ]
].copy()

history = history.sort_values(
    ["product_id", "date"]
)


results = []


for product_id in future["product_id"].unique():

    product_history = history[
        history["product_id"] == product_id
    ].copy()

    product_future = future[
        future["product_id"] == product_id
    ].copy()

    # Historical demand values
    demand_values = product_history["demand"].tolist()

    if len(demand_values) < 28:
        continue

    for _, row in product_future.iterrows():

        # Lag features
        lag_1 = demand_values[-1]
        lag_7 = demand_values[-7]
        lag_14 = demand_values[-14]
        lag_28 = demand_values[-28]

        # Rolling features
        rolling_mean_7 = np.mean(
            demand_values[-7:]
        )

        rolling_mean_14 = np.mean(
            demand_values[-14:]
        )

        rolling_mean_28 = np.mean(
            demand_values[-28:]
        )

        rolling_std_7 = np.std(
            demand_values[-7:]
        )

        rolling_max_7 = np.max(
            demand_values[-7:]
        )


        # Create model input
        feature_row = pd.DataFrame(
            [
                {
                    "lag_1": lag_1,
                    "lag_7": lag_7,
                    "lag_14": lag_14,
                    "lag_28": lag_28,
                    "rolling_mean_7": rolling_mean_7,
                    "rolling_mean_14": rolling_mean_14,
                    "rolling_mean_28": rolling_mean_28,
                    "rolling_std_7": rolling_std_7,
                    "rolling_max_7": rolling_max_7,
                    "month": row["month"],
                    "day_of_week": row["day_of_week"],
                    "is_weekend": row["is_weekend"],
                }
            ]
        )


        # Predict log-transformed demand
        prediction_log = model.predict(
            feature_row[FEATURES]
        )[0]


        # Convert back from log scale
        prediction = max(
            0,
            np.expm1(prediction_log),
        )


        results.append(
            {
                "date": row["date"],
                "product_id": product_id,
                "product_name": row["product_name"],
                "predicted_demand": round(
                    float(prediction),
                    2,
                ),
            }
        )


        # Recursive forecasting:
        # use predicted demand as the next day's history
        demand_values.append(prediction)


# Create forecast DataFrame
forecast = pd.DataFrame(results)


# Sort forecast results
forecast = forecast.sort_values(
    ["date", "predicted_demand"],
    ascending=[True, False],
)


# Create output directory
OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True,
)


# Save forecast
forecast.to_csv(
    OUTPUT_PATH,
    index=False,
)


print("\n========================================")
print("7-DAY DEMAND FORECAST")
print("========================================")


print(
    f"Forecast start: {future_dates.min().date()}"
)

print(
    f"Forecast end:   {future_dates.max().date()}"
)

print(
    f"Products forecasted: "
    f"{forecast['product_id'].nunique()}"
)

print(
    f"Forecast rows: "
    f"{len(forecast)}"
)


print("\nTotal predicted demand:")

print(
    round(
        forecast["predicted_demand"].sum(),
        2,
    )
)


print("\nTop predicted products:")

print(
    forecast
    .groupby(
        ["product_id", "product_name"],
        as_index=False,
    )
    .agg(
        predicted_demand=(
            "predicted_demand",
            "sum",
        )
    )
    .sort_values(
        by="predicted_demand",
        ascending=False,
    )
    .head(10)
    .to_string(index=False)
)


print("\nForecast saved to:")
print(OUTPUT_PATH)


print("\n7-day forecasting completed successfully.")