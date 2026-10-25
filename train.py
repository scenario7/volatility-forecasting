"""Run HAR walk-forward backtest and print RMSE/bias results."""

import numpy as np
from backtest import load_data, walk_forward

df = load_data()
predictions, yearly_rmse = walk_forward(df)

print("RMSE by Year (lower is better):")
print("=" * 60)
print(yearly_rmse.to_string(float_format="{:.4f}".format))
print("=" * 60)

print(f"\nMean RMSE:")
for col in ["HAR", "VIX", "Naive"]:
    print(f"  {col:12s} {yearly_rmse[col].mean():.4f}")

print(f"\nHAR wins vs VIX:   {(yearly_rmse['HAR'] < yearly_rmse['VIX']).sum()}/{len(yearly_rmse)} years")
print(f"HAR wins vs Naive: {(yearly_rmse['HAR'] < yearly_rmse['Naive']).sum()}/{len(yearly_rmse)} years")

print(f"\nOverall Bias (all {len(predictions)} test days):")
for col in ["HAR", "VIX", "Naive"]:
    bias = (predictions[col] - predictions["Actual"]).mean()
    rmse = np.sqrt(((predictions[col] - predictions["Actual"]) ** 2).mean())
    print(f"  {col:12s} RMSE={rmse:.4f}  Bias={bias:+.4f}")
