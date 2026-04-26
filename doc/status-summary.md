# Project Status Summary

This file summarizes the current state of the project, what each main file does, and what we are working on right now.

## Current Goal

Build a multi-tier call center simulation with three layers:

1. Simulation engine in Python + SimPy
2. FastAPI service for serving simulation output
3. React dashboard for visual analysis later

## What Is Implemented

### Milestone 1: Simulation Engine

The simulation layer is already working and produces JSON output for multiple scenarios.

- Stochastic call arrivals
- VIP priority handling
- Tier 1 and Tier 2 service flow
- Dynamic escalation logic
- Random abandonment using patience time
- Monte Carlo replications
- KPI aggregation and confidence intervals
- Time-series export for queue and utilization charts

### Milestone 2: API Layer

The FastAPI layer is implemented and serves the exported simulation payload.

- Run new simulation scenarios through the API
- Read the latest comparison payload from disk
- Fetch metrics for all scenarios or one scenario
- Health check endpoint
- Historical run persistence and run listing
- Historical run retrieval by run id

### Milestone 2.1: Contracts and Persistence

We now also have explicit contract artifacts and run history support.

- JSON schema for exported simulation output
- OpenAPI contract for the FastAPI service
- Persistent run history manifest for saved simulation outputs

### Milestone 3: Dashboard Scaffold

A first React dashboard scaffold is present.

- Builds successfully with Vite after installing dashboard dependencies

## Main Files and What They Do

### Root Files


### Contract Files

- Dashboard production build passes with Vite
- [simulation/entities.py](../simulation/entities.py) defines the call entity and customer type model.
- [simulation/resources.py](../simulation/resources.py) creates the SimPy resource layer for IVR, Tier 1, and Tier 2.
- [simulation/processes.py](../simulation/processes.py) contains the actual event flow for arrivals, queueing, abandonment, service, and escalation.
- [simulation/metrics.py](../simulation/metrics.py) collects KPIs, stores time-series samples, and aggregates replications.
- [simulation/scenarios.py](../simulation/scenarios.py) defines the scenario catalog such as normal load, peak load, and reduced staff.
- [simulation/run_simulation.py](../simulation/run_simulation.py) is the CLI runner that executes scenarios and writes JSON output.

### API Layer

- [api/main.py](../api/main.py) exposes FastAPI endpoints for running simulations, reading exported comparison and metrics payloads, and browsing historical runs.

### Dashboard Layer

- [dashboard/package.json](../dashboard/package.json) defines the React, Vite, Recharts, and Zustand frontend stack.
- [dashboard/src/App.tsx](../dashboard/src/App.tsx) contains the current dashboard layout and data visualization shell.
- [dashboard/src/lib/api.ts](../dashboard/src/lib/api.ts) connects the dashboard to the FastAPI service.
- [dashboard/src/store/useDashboardStore.ts](../dashboard/src/store/useDashboardStore.ts) manages remote state for runs and comparison data.

## Current Behavior

### Simulation Output

The simulation runner produces a JSON document with:

- Meta information
- Per-scenario replications
- Aggregated KPI values
- 95 percent confidence intervals
- Time-series data for charts
- Scenario comparison rows

### API Behavior

The API currently supports these endpoints:

- `POST /run-simulation`
- `GET /compare-scenarios`
- `GET /get-metrics`
- `GET /runs`
- `GET /runs/{run_id}`
- `GET /health`

## What We Are Doing Now

We are in the API and contract phase after the simulation engine is complete.

Right now the focus is:

1. Keeping the simulation output contract stable
2. Serving the same output through FastAPI
3. Preserving historical runs on disk
4. Preparing the data shape that a future React dashboard can consume directly

## Verified So Far

- Simulation runs successfully from the CLI
- API module imports successfully
- API endpoints return valid payloads from exported results
- Historical run listing and lookup are now available
- Static error checks are clean for the new files
- Automated tests pass for persistence and schema validation

## Notes About the Workspace

- The project already contains generated simulation output under the results folder.
- The code currently uses the repo-local virtual environment at [.venv](../.venv) for validation.

## Next Likely Steps

1. Expand the dashboard from scaffold into richer charts and filters.
2. Add endpoint-level HTTP tests for the API when httpx is available in the environment.
3. Connect the dashboard to live refresh actions for new simulation runs.
