"""Demo: response-time SLAs + capacity-buffer vs service-level trade-off."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from src.synth_data import generate_dealers, generate_regional_demand
from src.scoring import score_all
from src.response_time import simulate_sla, buffer_tradeoff

os.makedirs("outputs", exist_ok=True)

dealers = score_all(generate_dealers(120))
demand = generate_regional_demand()

# ---- 1. Network shape drives response SLAs ------------------------------------
full_pool = dealers["response_time_hrs"].to_numpy()
selected = dealers.nlargest(42, "score")["response_time_hrs"].to_numpy()
top_quartile = (dealers.nlargest(30, "score")["response_time_hrs"].to_numpy())

print("=== RESPONSE-TIME SLA (Monte Carlo, 24h SLA, 2,000 orders) ===")
rows = []
for label, pool in [("Full universe (120)", full_pool),
                    ("Scored selection (42)", selected),
                    ("Top-score only (30)", top_quartile)]:
    s = simulate_sla(pool)
    s["network"] = label
    rows.append(s)
sla = pd.DataFrame(rows).set_index("network")
print(sla.to_string())

# ---- 2. Capacity buffer vs resilience trade-off --------------------------------
trade = pd.DataFrame(buffer_tradeoff(dealers, demand))
print("\n=== CAPACITY BUFFER vs SERVICE LEVEL ===")
print(trade.to_string(index=False))

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].bar(trade["buffer"], trade["partners"], color="#264653")
axes[0].set_title("Partners needed vs buffer")
axes[0].set_xlabel("Capacity buffer")
axes[0].set_ylabel("Partners")
axes[1].plot(trade["buffer"], trade["p_within_sla_pct"],
             marker="o", lw=2, color="#e76f51")
axes[1].set_title("Orders answered < 24h vs buffer")
axes[1].set_xlabel("Capacity buffer")
axes[1].set_ylabel("% within SLA")
axes[1].set_ylim(80, 101)
plt.tight_layout()
plt.savefig("outputs/buffer_tradeoff.png", dpi=150)
plt.close()

print("\nSaved outputs/: buffer_tradeoff.png")
