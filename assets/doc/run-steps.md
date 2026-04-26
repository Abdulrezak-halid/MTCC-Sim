# Run Steps (Data, Simulation, API, UI)

This file contains only the steps to run everything.

## 1) Setup Python Environment

```bash
cd /home/abod/Workspace/Projects/multi-tier-call-center-simulation
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Generate Simulation Data (CLI)

```bash
source .venv/bin/activate
python simulation/run_simulation.py --scenario all --output simulation/results/latest_results.json
```

Optional single scenario:

```bash
python simulation/run_simulation.py --scenario peak_load --replications 20 --seed 42 --output simulation/results/peak.json
```

## 3) Start API

```bash
source .venv/bin/activate
uvicorn api.main:app --reload
```

API URL:

- http://127.0.0.1:8000

## 4) Start Dashboard UI

Open a new terminal:

```bash
cd /home/abod/Workspace/Projects/multi-tier-call-center-simulation/dashboard
npm install
npm run dev
```

Dashboard URL:

- http://127.0.0.1:5173

## 5) Validate End-to-End

- Open the dashboard.
- Ensure scenarios and run history load.
- Trigger a simulation from API if needed:

```bash
curl -X POST "http://127.0.0.1:8000/run-simulation" \
  -H "Content-Type: application/json" \
  -d '{"scenario":"all","seed":42,"replications":10}'
```

- Refresh dashboard data.

## 6) Run Tests (Optional)

```bash
cd /home/abod/Workspace/Projects/multi-tier-call-center-simulation
source .venv/bin/activate
python -m unittest discover -s tests
```
