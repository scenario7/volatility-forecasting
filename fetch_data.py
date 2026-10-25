"""Fetch SPY and VIX closing prices from Yahoo Finance since 2005.

Outputs separate CSVs for each, with log daily returns computed.
VIX is normalized from percentage to decimal (divided by 100).
"""

import numpy as np
import yfinance as yf
import pandas as pd

START_DATE = "2005-01-01"
TICKERS = {"SPY": "SPY", "VIX": "^VIX"}


def fetch_and_save(name: str, ticker: str, normalize: bool = False) -> pd.DataFrame:
    df = yf.download(ticker, start=START_DATE, auto_adjust=True)
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]

    out = pd.DataFrame({"Close": close})
    out.index.name = "Date"

    if normalize:
        out["Close"] = out["Close"] / 100.0

    out["Log_Return"] = np.log(out["Close"] / out["Close"].shift(1))
    out = out.dropna()

    filename = f"{name.lower()}_daily.csv"
    out.to_csv(filename)
    print(f"{name}: saved {len(out)} rows to {filename}")
    print(out.head(), "\n")
    return out


if __name__ == "__main__":
    spy = fetch_and_save("SPY", TICKERS["SPY"])
    vix = fetch_and_save("VIX", TICKERS["VIX"], normalize=True)
