export type ComparisonRow = {
  scenario_id: string;
  scenario_name: string;
  avg_wait_seconds: number;
  abandonment_rate: number;
  sla_compliance_rate: number;
  utilization_tier1: number;
  utilization_tier2: number;
};

export type RunRecord = {
  run_id: string;
  generated_at: string;
  base_seed: number;
  scenario_count: number;
  scenario_ids: string[];
  output_path: string;
};

export type HistoricalRunPayload = {
  record: RunRecord;
  payload: {
    meta: {
      run_id?: string | null;
      generated_at: string;
      engine_version: string;
      base_seed: number;
      scenario_count: number;
    };
    comparison: ComparisonRow[];
    scenarios: Array<{
      scenario: { scenario_id: string; name: string };
      aggregates: {
        kpis: Record<string, number>;
        confidence_intervals_95: Record<
          string,
          { mean: number; lower: number; upper: number }
        >;
      };
    }>;
  };
};
