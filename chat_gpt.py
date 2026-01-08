import pandas as pd
import numpy as np

def pareto_front(df, x_col="pe", y_col="y"):
    """
    Pareto front for: minimize x, maximize y.
    Returns a boolean mask of non-dominated rows.
    """
    x = df[x_col].to_numpy(dtype=float)
    y = df[y_col].to_numpy(dtype=float)

    n = len(df)
    is_front = np.ones(n, dtype=bool)

    for i in range(n):
        if not is_front[i]:
            continue
        # Any j that dominates i?
        dominates_i = (x <= x[i]) & (y >= y[i]) & ((x < x[i]) | (y > y[i]))
        dominates_i[i] = False
        if dominates_i.any():
            is_front[i] = False

    return is_front

# --- Load your S&P 500 data ---
df = pd.read_csv("sp500_pe_price_52wh.csv")

# Clean / compute y
df = df.dropna(subset=["ticker", "pe", "price", "high_52w"]).copy()
df["pe"] = pd.to_numeric(df["pe"], errors="coerce")
df["price"] = pd.to_numeric(df["price"], errors="coerce")
df["high_52w"] = pd.to_numeric(df["high_52w"], errors="coerce")
df = df.dropna(subset=["pe", "price", "high_52w"])
df = df[df["high_52w"] > 0]
df = df[df["pe"] > 0]  # optional: exclude negative/undefined PEs

df["y"] = 1.0 - (df["price"] / df["high_52w"])

# Pareto front
mask = pareto_front(df, x_col="pe", y_col="y")
front = df.loc[mask].copy()

# Choose 10 to list (one reasonable convention: lowest P/E first)
front_10 = front.sort_values(["pe", "y"], ascending=[True, False]).head(10)

print(front_10[["ticker", "pe", "price", "high_52w", "y"]].to_string(index=False))

