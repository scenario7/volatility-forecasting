"""Plot the Volatility Risk Premium (VRP) over time."""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("spy_realized_vol.csv", index_col="Date", parse_dates=True)

fig, ax = plt.subplots(figsize=(14, 5))
ax.fill_between(df.index, df["VRP"], 0, where=df["VRP"] >= 0, color="steelblue", alpha=0.5, label="VRP > 0 (VIX overestimates)")
ax.fill_between(df.index, df["VRP"], 0, where=df["VRP"] < 0, color="coral", alpha=0.5, label="VRP < 0 (VIX underestimates)")
ax.axhline(0, color="black", linewidth=0.5)
ax.set_title("Volatility Risk Premium (VIX − 21-Day Forward Realized Vol)")
ax.set_ylabel("VRP")
ax.set_xlabel("Date")
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig("vrp.png", dpi=150)
plt.show()
print("Saved to vrp.png")
