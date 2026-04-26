# Project Structure and File Purpose

This document explains what each main folder does and what each project file is used for.

## Root

- `README.md`: concise project overview and links to detailed docs.
- `requirements.txt`: Python dependencies for simulation and API.
- `.gitignore`: ignored files and folders (venv, build outputs, generated results).

## .github

- `.github/instructions.md`: repository-specific coding/agent instructions.

## .vscode

- `.vscode/settings.json`: workspace editor settings.

## api

- `api/main.py`: FastAPI app, endpoints, run persistence, and CORS configuration.

## contracts

- `contracts/simulation-output.schema.json`: JSON Schema for exported simulation results.
- `contracts/api.openapi.yaml`: OpenAPI contract for API endpoints and payloads.

## simulation

- `simulation/environment.py`: simulation configuration and random stream helpers.
- `simulation/entities.py`: call/customer domain entities.
- `simulation/resources.py`: SimPy resource definitions (IVR, Tier 1, Tier 2).
- `simulation/processes.py`: call flow logic (arrival, queueing, service, escalation, abandonment).
- `simulation/metrics.py`: KPI collection, aggregation, and confidence intervals.
- `simulation/scenarios.py`: predefined scenario catalog and settings.
- `simulation/run_simulation.py`: CLI entry point to run scenarios and export JSON results.
- `simulation/results/`: primary output directory for generated simulation JSON.
- `simulation/simulation/`: nested package/output folder currently present in the repository.
- `simulation/simulation/results/latest_results.json`: latest generated simulation output snapshot currently available.

## dashboard

- `dashboard/package.json`: frontend scripts and dependencies.
- `dashboard/package-lock.json`: locked npm dependency tree.
- `dashboard/tsconfig.json`: TypeScript compiler configuration.
- `dashboard/vite.config.ts`: Vite dev/build configuration.
- `dashboard/index.html`: frontend app HTML shell.
- `dashboard/src/main.tsx`: React application bootstrap.
- `dashboard/src/App.tsx`: main dashboard UI composition.
- `dashboard/src/styles.css`: dashboard styling.
- `dashboard/src/types.ts`: shared TypeScript data models.
- `dashboard/src/vite-env.d.ts`: Vite TypeScript environment types.
- `dashboard/src/lib/api.ts`: API client functions used by the dashboard.
- `dashboard/src/store/useDashboardStore.ts`: Zustand store for dashboard state.

## tests

- `tests/test_api_history.py`: tests for run history endpoints and schema shape validation.

## doc

- `doc/status-summary.md`: current implementation status and milestone summary.
- `doc/ABDALRAZAK_KHALED_22430070907_VIZE_RAPORU.pdf`: project report document.
- `doc/project-structure.md`: this file.
- `doc/run-steps.md`: minimal run instructions for data, simulation, API, and UI.
