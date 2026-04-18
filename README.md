<img width="1536" height="1024" alt="Multi-tier call center simulation overview" src="https://github.com/user-attachments/assets/ae268d7c-18d9-425e-81f3-9fe6da3711ca" />

# Multi-Tier Call Center Simulation Diagram

A simulation of how customer requests flow through a multi-level support system, including classification, routing, escalation, and resolution.

---

## Entry Point

- **Customer Call (Inbound)**
  - Phone / Chat

- **IVR & Auto-Router**
  - Classifies requests by issue type
  - Routes calls to appropriate queue

---

## Tier 1 — Front-Line Agents

Handles basic and common issues.

- **Agent A**
  - General inquiries
  - Password resets

- **Agent B**
  - Order tracking
  - Basic troubleshooting

- **Agent C**
  - Billing questions
  - Account updates

✅ Possible Outcomes:

- Issue resolved
- Escalation to Tier 2

---

## Tier 2 — Specialists

Handles more complex and technical issues.

- **Tech Specialist**
  - Complex issues
  - Deep diagnostics

- **Billing Specialist**
  - Disputes & refunds
  - Fraud review

- **Product Expert**
  - Configuration & setup
  - Compatibility issues

✅ Possible Outcomes:

- Issue resolved
- Escalation to Tier 3 (critical cases)

---

## Tier 3 — Expert Engineers / Management

Handles critical, system-level, or policy-related issues.

- **Engineering Team**
  - Bug fixes
  - System outages

- **Management**
  - Policy decisions
  - Escalation handling

- **Vendor / Third-Party Support**
  - External system issues

✅ Possible Outcomes:

- Issue resolved
- Critical resolution

---

## Flow Summary

1. Customer initiates request
2. IVR classifies and routes
3. Tier 1 handles basic issues
4. Tier 2 handles complex issues
5. Tier 3 handles critical/system-level issues

---

## Resolution States

- ✅ Resolved at Tier
- 🔼 Escalated to next Tier
- 🚨 Critical escalation

<p align="center" width="1536" height="1024">
  <img src="https://github.com/user-attachments/assets/dd09e3e4-26ce-4040-8581-73a38be1e06e" width="600"/>
</p>
This repository contains a probabilistic discrete-event simulation for a multi-tier call center.

### Implemented Milestone 1

- Stochastic call arrivals (Poisson process)
- VIP and normal customer handling with priority queueing
- Tier 1 and Tier 2 service flow with dynamic escalation logic
- Call abandonment based on random patience
- Monte Carlo replications for scenario comparison
- JSON export with per-replication KPIs, aggregate KPIs, confidence intervals, and time series

### Quick Start

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run all predefined scenarios:

```bash
python simulation/run_simulation.py --scenario all --output simulation/results/latest_results.json
```

4. Run a single scenario with custom replication count:

```bash
python simulation/run_simulation.py --scenario peak_load --replications 20 --seed 42 --output simulation/results/peak.json
```

### Scenario IDs

- `normal_load`
- `peak_load`
- `reduced_staff`
- `increased_vip_ratio`
- `improved_staff_efficiency`

### Output

The generated JSON file includes:

- `scenarios`: full simulation output for each scenario
- `comparison`: compact KPI table for cross-scenario analysis
- `meta`: run metadata including seed and engine version

### Milestone 2 API (FastAPI)

Start API server:

```bash
uvicorn api.main:app --reload
```

Available endpoints:

- `POST /run-simulation`
  - Runs one or more scenarios and optionally exports result JSON.
- `GET /compare-scenarios`
  - Returns the exported comparison payload directly.
- `GET /get-metrics`
  - Returns aggregate KPI metrics for all scenarios or one specific scenario.
- `GET /health`
  - Health check endpoint.

Example requests:

```bash
curl -X POST "http://127.0.0.1:8000/run-simulation" \
  -H "Content-Type: application/json" \
  -d '{"scenario":"all","seed":42,"replications":10}'
```

```bash
curl "http://127.0.0.1:8000/compare-scenarios"
```

```bash
curl "http://127.0.0.1:8000/get-metrics?scenario_id=normal_load"
```
