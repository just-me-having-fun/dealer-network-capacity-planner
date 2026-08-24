"""Response-time service-level simulation for a dealer network."""
import numpy as np


def simulate_sla(partner_response_times, orders=2000, sla_hours=24, seed=1):
    """Monte Carlo: each order lands on a random partner in the configured
    network (capacity-weighted pools shift this toward better partners).

    partner_response_times: list/array of each partner's mean response hrs.
    Returns SLA stats for the network as configured.
    """
    rng = np.random.default_rng(seed)
    means = np.asarray(partner_response_times, dtype=float)
    picks = rng.integers(0, len(means), size=orders)
    draws = rng.gamma(2.5, means[picks] / 2.5)
    return {
        "median_hrs": round(float(np.median(draws)), 1),
        "p_within_sla_pct": round(float((draws <= sla_hours).mean() * 100), 1),
        "p90_hrs": round(float(np.percentile(draws, 90)), 1),
    }


def buffer_tradeoff(scored, regional_demand, buffers=(1.10, 1.25, 1.40),
                    from_src_capacity=None):
    """Partner count vs service level as the capacity buffer grows.

    Uses select_network at each buffer, then simulates SLA per config.
    """
    from .capacity import select_network

    rows = []
    for b in buffers:
        plan, picks = select_network(scored, regional_demand, buffer_pct=b)
        sel = scored[scored["dealer_id"].isin(picks)]
        stats = simulate_sla(sel["response_time_hrs"].to_numpy())
        rows.append({
            "buffer": f"{int(round((b - 1) * 100))}%",
            "partners": int(len(picks)),
            "capacity_units_mo": int(sel["monthly_capacity_units"].sum()),
            **stats,
        })
    return rows
