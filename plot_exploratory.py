"""Exploratory plots: VIX vs Forward RV, and Volatility Risk Premium."""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("spy_realized_vol.csv", index_col="Date", parse_dates=True)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# VIX vs Forward Realized Vol
ax1.plot(df.index, df["VIX"], label="VIX (implied)", alpha=0.7, linewidth=0.8)
ax1.plot(df.index, df["RV_21_Fwd"], label="21-day Fwd Realized Vol", alpha=0.7, linewidth=0.8)
ax1.set_title("VIX vs 21-Day Forward Realized Volatility")
ax1.set_ylabel("Annualized Volatility")
ax1.legend()
ax1.grid(True, alpha=0.3)

# VRP
ax2.fill_between(df.index, df["VRP"], 0, where=df["VRP"] >= 0, color="steelblue", alpha=0.5, label="VRP > 0 (VIX overestimates)")
ax2.fill_between(df.index, df["VRP"], 0, where=df["VRP"] < 0, color="coral", alpha=0.5, label="VRP < 0 (VIX underestimates)")
ax2.axhline(0, color="black", linewidth=0.5)
ax2.set_title("Volatility Risk Premium (VIX \u2212 21-Day Forward Realized Vol)")
ax2.set_ylabel("VRP")
ax2.set_xlabel("Date")
ax2.legend()
ax2.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig("exploratory.png", dpi=150)
plt.show()
print("Saved to exploratory.png")
