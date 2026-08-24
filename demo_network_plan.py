"""Demo: score a synthetic dealer universe, then plan a market-entry network."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.synth_data import generate_dealers, generate_regional_demand
from src.scoring import score_all, rank_dealers
from src.capacity import saturation, select_network

os.makedirs("outputs", exist_ok=True)

dealers = generate_dealers(120)
demand = generate_regional_demand()
scored = score_all(dealers)

# ---- 1. Dealer shortlist -----------------------------------------------------
top = rank_dealers(scored, top_n=10)
print("=== TOP 10 DEALER SHORTLIST ===")
print(top.to_string(index=False))
top.to_csv("outputs/top_dealers.csv", index=False)

# ---- 2. Whole-network saturation ----------------------------------------------
sat = saturation(scored, demand)
print("\n=== FULL-NETWORK SATURATION (all dealers at max) ===")
print(sat.to_string())

# ---- 3. Greedy market-entry network -------------------------------------------
plan, picks = select_network(scored, demand)
print("\n=== MARKET-ENTRY PLAN (greedy by score, 125% capacity buffer) ===")
print(plan.to_string(index=False))
print(f"\nTotal partners needed: {len(picks)} of {len(dealers)}")

# ---- Chart ----------------------------------------------------------------------
sel = plan.set_index("region").loc[sat.index]
fig, ax = plt.subplots(figsize=(8, 4.5))
x = range(len(sat))
w = 0.38
ax.bar([i - w / 2 for i in x], sat["regional_demand"], w,
       label="Regional demand", color="#e76f51")
ax.bar([i + w / 2 for i in x], sel["selected_capacity"], w,
       label="Selected network capacity (+25% buffer)", color="#2a9d8f")
for i, cov in enumerate(sel["coverage_pct"]):
    ax.text(i + w / 2, sel["selected_capacity"].iloc[i] + 60,
            f"{cov:.0f}%", ha="center", fontsize=9)
ax.set_xticks(list(x))
ax.set_xticklabels(sat.index)
ax.set_title("Market-entry network: selected capacity vs demand")
ax.set_ylabel("Units/month")
ax.legend()
plt.tight_layout()
plt.savefig("outputs/network_coverage.png", dpi=150)
plt.close()

print("\nSaved outputs/: top_dealers.csv, network_coverage.png")
