"""Multi-criteria dealer scoring and ranking."""
import pandas as pd

DEFAULT_WEIGHTS = {
    "financial_health": 0.30,
    "infrastructure": 0.25,
    "on_time_delivery_pct": 0.25,
    "track_record_years": 0.10,
    "responsiveness": 0.10,
}


def score_all(dealers, weights=None):
    """Weighted 0-1 normalised score per dealer.

    'responsiveness' is derived by inverting response_time_hrs
    (faster response -> higher score).
    """
    weights = weights or DEFAULT_WEIGHTS
    d = dealers.copy()
    d["responsiveness"] = d["response_time_hrs"].max() - d["response_time_hrs"]

    score = pd.Series(0.0, index=d.index)
    for col, w in weights.items():
        score += d[col] / d[col].max() * w
    d["score"] = score.round(3)
    return d


def rank_dealers(scored, top_n=10, capacity_floor=200):
    """Top-N dealer shortlist among those meeting the capacity floor."""
    eligible = scored[scored["monthly_capacity_units"] >= capacity_floor]
    ranked = eligible.sort_values("score", ascending=False).head(top_n)
    cols = ["score", "dealer_id", "region", "monthly_capacity_units",
            "financial_health", "infrastructure", "on_time_delivery_pct",
            "response_time_hrs"]
    return ranked[cols].reset_index(drop=True)
