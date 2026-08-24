# Dealer Network Capacity Planner

An open-source toolkit for **designing and stress-testing distribution networks** — dealer selection, coverage modeling, and capacity planning for market-entry operations.

## Why

During my consulting internship (consumer & industrial clients), I worked on dealer-selection frameworks and distribution network analysis for an international brand's India entry — including processing 1,000+ distributor inputs that helped cut partner response times by ~50%. This project turns that methodology into a reusable, public tool with fully synthetic data.

## What it does (planned)

| Module | What it solves | Status |
|---|---|---|
| **Dealer scoring engine** | Multi-criteria partner selection — financial health, infra, coverage, track record → weighted ranking | ⏳ |
| **Coverage model** | Geographic demand mapping vs network footprint; white-space identification | ⏳ |
| **Capacity planner** | Distributor throughput vs regional demand; where the network saturates first | ⏳ |
| **Response-time simulator** | Service-level modeling — how network shape drives fulfillment/response SLAs | ⏳ |
| **Scenario board** | Entry strategies compared: depth-first vs breadth-first expansion | ⏳ |

## Tech

- Python 3, pandas, geopandas, numpy, matplotlib/folium
- Synthetic dataset only (generated, no real client or market data)

## Roadmap

- [ ] Repo scaffold + README
- [ ] Synthetic distributor dataset generator
- [ ] Scoring engine + weighted-criteria config
- [ ] Coverage maps (demand vs footprint)
- [ ] Capacity saturation analysis
- [ ] Response-time simulation notebook
- [ ] Scenario comparison + final writeup

---

*In progress — being built out this week.*
