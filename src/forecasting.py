import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def forecast_next_30_days(df):
    """
    Forecast next 30 days demand using Units_Sold column.
    Works for product-level and warehouse-level filtered data.
    """

    if df.empty:
        return None

    # Ensure date type
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # Aggregate daily sales (important when multiple rows per day exist)
    daily_sales = (
        df.groupby("Date", as_index=False)["Units_Sold"]
        .sum()
        .sort_values("Date")
    )

    # Not enough data
    if len(daily_sales) < 30:
        return None

    ts = daily_sales.set_index("Date")["Units_Sold"]

    try:
        model = ExponentialSmoothing(
            ts,
            trend="add",
            seasonal=None
        )
        fitted_model = model.fit()
        forecast = fitted_model.forecast(30)

        forecast_df = forecast.reset_index()
        forecast_df.columns = ["Date", "Forecasted_Units"]

        return forecast_df

    except Exception:
        # Safety fallback
        return None
