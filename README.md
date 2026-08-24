# Dealer Network Capacity Planner

An open-source toolkit for **designing and stress-testing distribution networks** — dealer selection, coverage modeling, and capacity planning for market-entry operations.

## Why

During my consulting internship (consumer & industrial clients), I worked on dealer-selection frameworks and distribution network analysis for an international brand's India entry — including processing 1,000+ distributor inputs that helped cut partner response times by ~50%. This project turns that methodology into a reusable, public tool with fully synthetic data.

## What it does

| Module | What it solves | Status |
|---|---|---|
| **Dealer scoring engine** | Multi-criteria partner selection — financial health, infra, OTD, track record, responsiveness → weighted 0–1 score + ranking | ✅ |
| **Coverage model** | Regional demand vs network footprint; saturation status per region | ✅ |
| **Capacity planner** | Greedy market-entry selection: pick top-scoring partners per region until demand × buffer is covered | ✅ |
| **Response-time simulator** | Monte Carlo SLA modeling — scored selection lifts 24h service level from 81% to 90% | ✅ |
| **Scenario board** | Capacity-buffer vs partner-count vs service-level trade-off analysis | ✅ |

Run it: `pip install -r requirements.txt` then `python demo_network_plan.py` and `python demo_scenarios.py`.

## Tech

- Python 3, pandas, numpy, matplotlib (geopandas/folium maps planned)
- Synthetic dataset only (generated, no real client or market data)

## Roadmap

- [x] Repo scaffold + README
- [x] Synthetic distributor dataset generator
- [x] Scoring engine + weighted-criteria config
- [x] Top-N dealer shortlist
- [x] Full-network saturation analysis
- [x] Greedy market-entry network plan (125% capacity buffer)
- [ ] Geospatial coverage maps
- [x] Response-time simulation (Monte Carlo SLA)
- [x] Scenario analysis: capacity buffer vs service-level trade-off

---

*In progress — being built out this week.*
