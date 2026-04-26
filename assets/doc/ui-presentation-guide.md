# UI Presentation Guide (Quick Q&A)

Use this file to explain the dashboard smoothly during presentation.

## What is shown in the UI?

The dashboard is split into four main sections:

1. Current run card
- Shows which simulation run is active.
- Displays readable run time, scenario count, and seed.
- Also keeps a short run ID for traceability.

2. Scenario comparison chart
- Bar chart uses `avg_wait_seconds` from each scenario.
- Lower bar means less customer waiting time.
- Used for fast scenario-to-scenario performance comparison.

3. Historical runs
- Lists saved runs from API persistence.
- Lets us switch context and inspect old results.
- Each row shows run date/time, seed, and scenario count.

4. KPI snapshot + controls
- KPI cards summarize key metrics for selected scenario:
  - Average wait (seconds)
  - SLA compliance
  - Tier 1 utilization
  - Abandonment rate
- Active run selector changes which run is loaded.
- API status field shows connection or error message.

## Typical Professor Questions and Answers

### Q1) What does this UI solve?
It gives one place to compare scenarios, inspect historical runs, and read key KPIs without manually opening raw JSON files.

### Q2) Why is `avg_wait_seconds` important?
It directly reflects customer experience. If average wait goes up, service quality risk usually increases.

### Q3) What is `run-20260419T110016396184Z-40eac316`?
It is a unique run ID.
- `20260419T110016...Z` is the UTC timestamp of run creation.
- `40eac316` is a short unique suffix to avoid collisions.
In UI, it is now displayed in a readable way (date/time + seed + scenarios), with short ID kept for traceability.

### Q4) How does UI get data?
From FastAPI endpoints:
- `GET /compare-scenarios`
- `GET /runs`
- `GET /runs/{run_id}`

### Q5) How do we trust the data format?
Contracts and tests:
- `contracts/simulation-output.schema.json`
- `contracts/api.openapi.yaml`
- `tests/test_api_history.py`

## Talk Track (30 seconds)

This dashboard is the visualization layer of our call center simulation pipeline. We run scenario-based simulations, persist historical outputs, and expose them via FastAPI. The UI then compares average wait times, shows KPI snapshots, and allows switching between saved runs for analysis and reporting.
