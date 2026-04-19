import { useEffect } from "react";
import {
  BarChart,
  Bar,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { useDashboardStore } from "./store/useDashboardStore";
import type { HistoricalRunPayload } from "./types";

const kpiTone = ["#f97316", "#14b8a6", "#84cc16", "#e879f9"];

function formatPercent(value: number) {
  return `${(value * 100).toFixed(1)}%`;
}

function formatSeconds(value: number) {
  return `${value.toFixed(1)}s`;
}

export default function App() {
  const {
    comparison,
    runs,
    activeRun,
    loading,
    error,
    loadAll,
    selectRun,
    selectedRunId,
  } = useDashboardStore();

  useEffect(() => {
    void loadAll();
  }, [loadAll]);

  const selectedScenarioId =
    activeRun?.payload.scenarios[0]?.scenario.scenario_id;
  const selectedScenario = activeRun?.payload.scenarios.find(
    (scenario: HistoricalRunPayload["payload"]["scenarios"][number]) =>
      scenario.scenario.scenario_id === selectedScenarioId,
  );
  const kpis = selectedScenario?.aggregates.kpis ?? {};

  return (
    <div className="shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Call Center Control Room</p>
          <h1>Simulation comparison dashboard</h1>
          <p className="lede">
            A compact view of scenario performance, historical runs, and the
            current exported simulation payload.
          </p>
        </div>
        <div className="hero-card">
          <div className="hero-card-title">Current run</div>
          <div className="hero-card-value">
            {activeRun?.record.run_id ?? "No run selected"}
          </div>
          <div className="hero-card-subtitle">
            {activeRun
              ? `${activeRun.record.scenario_count} scenarios · seed ${activeRun.record.base_seed}`
              : "Load a run to inspect metrics"}
          </div>
        </div>
      </header>

      <main className="grid">
        <section className="panel panel-wide">
          <div className="panel-header">
            <h2>Scenario comparison</h2>
            <span>{comparison.length} scenarios</span>
          </div>
          <div className="chart-wrap">
            <ResponsiveContainer width="100%" height={320}>
              <BarChart
                data={comparison}
                margin={{ top: 16, right: 20, bottom: 8, left: 0 }}
              >
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="rgba(255,255,255,0.08)"
                />
                <XAxis
                  dataKey="scenario_name"
                  tick={{ fill: "#dbe4ff", fontSize: 12 }}
                />
                <YAxis tick={{ fill: "#dbe4ff", fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    background: "#10162d",
                    border: "1px solid rgba(255,255,255,0.12)",
                  }}
                />
                <Bar dataKey="avg_wait_seconds" radius={[10, 10, 0, 0]}>
                  {comparison.map((entry, index) => (
                    <Cell
                      key={entry.scenario_id}
                      fill={kpiTone[index % kpiTone.length]}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="panel">
          <div className="panel-header">
            <h2>Historical runs</h2>
            <span>{runs.length} saved</span>
          </div>
          <div className="run-list">
            {runs.map((run) => (
              <button
                key={run.run_id}
                type="button"
                className={
                  run.run_id === selectedRunId ? "run-item active" : "run-item"
                }
                onClick={() => void selectRun(run.run_id)}
              >
                <strong>{run.run_id}</strong>
                <span>{run.scenario_count} scenarios</span>
              </button>
            ))}
          </div>
        </section>

        <section className="panel panel-wide">
          <div className="panel-header">
            <h2>KPI snapshot</h2>
            <span>
              {selectedScenario
                ? selectedScenario.scenario.name
                : "No scenario selected"}
            </span>
          </div>
          <div className="kpi-grid">
            <article className="kpi-card">
              <span>Avg wait</span>
              <strong>
                {typeof kpis.avg_wait_seconds === "number"
                  ? formatSeconds(kpis.avg_wait_seconds)
                  : "—"}
              </strong>
            </article>
            <article className="kpi-card">
              <span>SLA compliance</span>
              <strong>
                {typeof kpis.sla_compliance_rate === "number"
                  ? formatPercent(kpis.sla_compliance_rate)
                  : "—"}
              </strong>
            </article>
            <article className="kpi-card">
              <span>Tier 1 utilization</span>
              <strong>
                {typeof kpis.utilization_tier1 === "number"
                  ? formatPercent(kpis.utilization_tier1)
                  : "—"}
              </strong>
            </article>
            <article className="kpi-card">
              <span>Abandonment</span>
              <strong>
                {typeof kpis.abandonment_rate === "number"
                  ? formatPercent(kpis.abandonment_rate)
                  : "—"}
              </strong>
            </article>
          </div>
        </section>

        <section className="panel">
          <div className="panel-header">
            <h2>Current run controls</h2>
            <span>{loading ? "Loading..." : "Ready"}</span>
          </div>
          <div className="control-stack">
            <label>
              <span>Active run</span>
              <select
                value={selectedRunId ?? ""}
                onChange={(event) => void selectRun(event.target.value)}
              >
                {runs.map((run) => (
                  <option key={run.run_id} value={run.run_id}>
                    {run.run_id}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <span>API status</span>
              <input value={error ?? "Connected to API contract"} readOnly />
            </label>
          </div>
        </section>
      </main>
    </div>
  );
}
