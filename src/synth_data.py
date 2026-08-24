"""Fully synthetic distributor/dealer dataset generator (no real market data)."""
import numpy as np
import pandas as pd

REGIONS = ["North", "West", "South", "East"]


def generate_dealers(n=120, seed=42):
    """Synthetic dealer master: capacity, health scores, responsiveness."""
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "dealer_id": [f"D{i:03d}" for i in range(1, n + 1)],
        "region": rng.choice(REGIONS, n, p=[0.32, 0.30, 0.24, 0.14]),
        "monthly_capacity_units": rng.integers(80, 900, n),
        "financial_health": rng.normal(70, 15, n).clip(20, 100).round(1),
        "infrastructure": rng.normal(65, 18, n).clip(10, 100).round(1),
        "track_record_years": rng.integers(1, 15, n),
        "response_time_hrs": rng.gamma(2.5, 6, n).round(1),
    })
    otd = rng.normal(85, 10, n) - 0.05 * (df["response_time_hrs"] - 12)
    df["on_time_delivery_pct"] = np.clip(otd, 50, 99).round(1)
    return df


def generate_regional_demand():
    """Monthly demand (units) by region — synthetic market-entry scenario."""
    return pd.Series(
        {"North": 5200, "West": 4800, "South": 3900, "East": 2100},
        name="monthly_demand_units",
    )
