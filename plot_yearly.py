"""Plot HAR vs VIX vs Actual forward RV for each test year."""

import matplotlib.pyplot as plt
from backtest import load_data, walk_forward, FIRST_TEST_YEAR

df = load_data()
predictions, yearly_rmse = walk_forward(df)

last_year = df.index[-1].year - 1
test_years = range(FIRST_TEST_YEAR, last_year + 1)
n_years = len(list(test_years))

fig, axes = plt.subplots(n_years, 1, figsize=(14, 3.5 * n_years), sharex=False)

for i, year in enumerate(test_years):
    ax = axes[i]
    yr = predictions[predictions.index.year == year]
    rmse_har = yearly_rmse.loc[year, "HAR"]
    rmse_vix = yearly_rmse.loc[year, "VIX"]

    ax.plot(yr.index, yr["Actual"], label="Actual", color="black", linewidth=1.5)
    ax.plot(yr.index, yr["HAR"], label=f"HAR (RMSE={rmse_har:.4f})", color="steelblue", linewidth=1, alpha=0.8)
    ax.plot(yr.index, yr["VIX"], label=f"VIX (RMSE={rmse_vix:.4f})", color="coral", linewidth=1, alpha=0.8)
    ax.set_title(f"{year}", fontsize=12, fontweight="bold")
    ax.set_ylabel("Vol")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

fig.suptitle(f"HAR vs VIX vs Actual Forward Realized Vol ({FIRST_TEST_YEAR}\u2013{last_year})", fontsize=14, fontweight="bold", y=1.0)
fig.tight_layout()
fig.savefig("har_yearly_predictions.png", dpi=150, bbox_inches="tight")
plt.show()
print("Saved to har_yearly_predictions.png")
