<img width="1536" height="1024" alt="Multi-tier call center simulation overview" src="https://github.com/user-attachments/assets/ae268d7c-18d9-425e-81f3-9fe6da3711ca" />

# Multi-Tier Call Center Simulation

A probabilistic discrete-event simulation of a multi-tier support center with:

- Python + SimPy simulation engine
- FastAPI service layer
- React + TypeScript dashboard

<p align="center" width="1536" height="1024">
  <img src="https://github.com/user-attachments/assets/dd09e3e4-26ce-4040-8581-73a38be1e06e" width="600"/>
</p>

## What This Project Includes

- Scenario-based call center simulation with Monte Carlo replications
- API endpoints to run simulations and fetch metrics/results
- Dashboard scaffold for scenario comparison and run history
- JSON Schema and OpenAPI contract artifacts

## Core Scenarios

- normal_load
- peak_load
- reduced_staff
- increased_vip_ratio
- improved_efficiency

## API Endpoints

- POST /run-simulation
- GET /compare-scenarios
- GET /get-metrics
- GET /runs
- GET /runs/{run_id}
- GET /health

## Documentation

- Project structure and file purpose: [doc/project-structure.md](doc/project-structure.md)
- Full run steps (data + simulation + API + UI): [doc/run-steps.md](doc/run-steps.md)
- Status snapshot: [doc/status-summary.md](doc/status-summary.md)

## Contracts

- [contracts/simulation-output.schema.json](contracts/simulation-output.schema.json)
- [contracts/api.openapi.yaml](contracts/api.openapi.yaml)

## Tests

Run API persistence and schema tests:

```bash
source .venv/bin/activate
python -m unittest discover -s tests
```
