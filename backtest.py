"""Walk-forward HAR backtest engine.

Trains HAR on an expanding window, predicting one year at a time.
Returns predictions and per-year RMSE/bias metrics.
"""

import statsmodels.api as sm
import pandas as pd
import numpy as np

GAP = 21
FEATURES = ["RV_1", "RV_5", "RV_21"]
FIRST_TEST_YEAR = 2013


def load_data() -> pd.DataFrame:
    return pd.read_csv("spy_realized_vol.csv", index_col="Date", parse_dates=True)


def walk_forward(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run expanding-window HAR backtest.

    Returns:
        predictions: DataFrame with Actual, HAR, VIX columns for all test days.
        yearly_rmse: DataFrame with per-year RMSE for HAR, VIX, Naive.
    """
    last_year = df.index[-1].year - 1
    test_years = range(FIRST_TEST_YEAR, last_year + 1)

    all_preds = []
    yearly_metrics = []

    for year in test_years:
        train = df[df.index < pd.Timestamp(f"{year}-01-01")].iloc[:-GAP]
        test = df[df.index.year == year]

        model = sm.OLS(
            train["RV_21_Fwd"],
            sm.add_constant(train[FEATURES]),
        ).fit()

        har_pred = model.predict(sm.add_constant(test[FEATURES]))
        actuals = test["RV_21_Fwd"]

        preds = pd.DataFrame({
            "Actual": actuals,
            "HAR": har_pred,
            "VIX": test["VIX"],
            "Naive": test["RV_21"],
        })
        all_preds.append(preds)

        yearly_metrics.append({
            "Year": year,
            "HAR": np.sqrt(((har_pred - actuals) ** 2).mean()),
            "VIX": np.sqrt(((test["VIX"] - actuals) ** 2).mean()),
            "Naive": np.sqrt(((test["RV_21"] - actuals) ** 2).mean()),
            "Train Size": len(train),
        })

    predictions = pd.concat(all_preds)
    yearly_rmse = pd.DataFrame(yearly_metrics).set_index("Year")
    return predictions, yearly_rmse
