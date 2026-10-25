"""Compute 21-day rolling realized volatility from SPY log returns, annualized."""

import numpy as np
import pandas as pd

WINDOW = 21
TRADING_DAYS = 252
INPUT_FILE = "spy_daily.csv"
OUTPUT_FILE = "spy_realized_vol.csv"


def compute_realized_vol() -> pd.DataFrame:
    df = pd.read_csv(INPUT_FILE, index_col="Date", parse_dates=True)
    vix = pd.read_csv("vix_daily.csv", index_col="Date", parse_dates=True)

    df["RV_1"] = df["Log_Return"].abs() * np.sqrt(TRADING_DAYS)
    df["RV_5"] = df["Log_Return"].rolling(window=5).std() * np.sqrt(TRADING_DAYS)
    df["RV_21"] = df["Log_Return"].rolling(window=WINDOW).std() * np.sqrt(TRADING_DAYS)
    df["RV_21_Fwd"] = df["RV_21"].shift(-WINDOW)
    df["VIX"] = vix["Close"]
    df["VRP"] = df["VIX"] - df["RV_21_Fwd"]
    df = df.dropna()
    return df


if __name__ == "__main__":
    data = compute_realized_vol()
    data.to_csv(OUTPUT_FILE)
    print(f"Saved {len(data)} rows to {OUTPUT_FILE}")
    print(data.head())
    print("...")
    print(data.tail())
