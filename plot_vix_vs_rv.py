"""Plot VIX vs forward realized volatility to visualize the volatility risk premium."""

import pandas as pd
import matplotlib.pyplot as plt

rv = pd.read_csv("spy_realized_vol.csv", index_col="Date", parse_dates=True)
vix = pd.read_csv("vix_daily.csv", index_col="Date", parse_dates=True)

merged = rv[["RV_21_Fwd"]].join(vix[["Close"]].rename(columns={"Close": "VIX"}), how="inner")

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(merged.index, merged["VIX"], label="VIX (implied)", alpha=0.7, linewidth=0.8)
ax.plot(merged.index, merged["RV_21_Fwd"], label="21-day Fwd Realized Vol", alpha=0.7, linewidth=0.8)
ax.set_title("VIX vs 21-Day Forward Realized Volatility")
ax.set_ylabel("Annualized Volatility")
ax.set_xlabel("Date")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig("vix_vs_rv_fwd.png", dpi=150)
plt.show()
print("Saved to vix_vs_rv_fwd.png")
