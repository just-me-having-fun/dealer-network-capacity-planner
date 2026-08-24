"""Network capacity saturation and partner selection."""
import numpy as np
import pandas as pd


def saturation(scored, regional_demand):
    """Coverage if the full regional network ships at max capacity."""
    cap = scored.groupby("region")["monthly_capacity_units"].sum()
    out = pd.DataFrame({"network_capacity": cap, "regional_demand": regional_demand}).fillna(0)
    out["coverage_pct"] = (out["network_capacity"] / out["regional_demand"] * 100).round(1)
    out["status"] = np.where(out["coverage_pct"] >= 150, "Surplus",
                     np.where(out["coverage_pct"] >= 90, "Adequate", "Shortfall"))
    return out


def select_network(scored, regional_demand, buffer_pct=1.25):
    """Greedy partner selection per region until demand * buffer is covered.

    Picks highest-scoring dealers first. Returns per-region build-out plan
    and the flat list of selected dealer IDs.
    """
    picks, summary = [], []
    for region, demand in regional_demand.items():
        pool = (scored[scored["region"] == region]
                .sort_values("score", ascending=False))
        target = demand * buffer_pct
        cum = 0
        region_picks = []
        for _, row in pool.iterrows():
            if cum >= target:
                break
            picks.append(row["dealer_id"])
            region_picks.append(row["dealer_id"])
            cum += row["monthly_capacity_units"]
        sel = scored[scored["dealer_id"].isin(region_picks)]
        summary.append({
            "region": region,
            "demand": int(demand),
            "target_with_buffer": int(target),
            "partners_selected": len(sel),
            "selected_capacity": int(sel["monthly_capacity_units"].sum()),
        })

    plan = pd.DataFrame(summary)
    plan["coverage_pct"] = (plan["selected_capacity"] / plan["demand"] * 100).round(1)
    return plan, picks
