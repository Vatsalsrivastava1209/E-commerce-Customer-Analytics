from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def test_summary_outputs_exist() -> None:
    summary_path = Path("reports/analysis_summary.json")
    assert summary_path.exists()
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["raw_rows"] == 541909
    assert summary["valid_sales_rows"] > 390000
    assert summary["net_revenue"] > 8_000_000
    assert summary["customers"] > 4000


def test_processed_files_have_expected_columns() -> None:
    country = pd.read_csv("data/processed/country_performance.csv")
    assert {"Country", "net_revenue", "orders", "customers", "aov"}.issubset(country.columns)

    rfm = pd.read_csv("data/processed/rfm_segments.csv")
    assert {"CustomerID", "recency_days", "frequency", "monetary", "segment"}.issubset(rfm.columns)

    cohort = pd.read_csv("data/processed/cohort_retention.csv")
    assert {"cohort_month", "months_since_first", "retention_rate"}.issubset(cohort.columns)


def test_figures_exist() -> None:
    for path in [
        Path("reports/figures/monthly_revenue.png"),
        Path("reports/figures/country_revenue.png"),
        Path("reports/figures/rfm_segments.png"),
        Path("reports/figures/cohort_retention.png"),
    ]:
        assert path.exists()
        assert path.stat().st_size > 0


def test_sql_files_are_substantive() -> None:
    sql_files = sorted(Path("sql").glob("*.sql"))
    assert len(sql_files) >= 7
    for path in sql_files:
        text = path.read_text(encoding="utf-8")
        assert "SELECT" in text.upper() or "CREATE" in text.upper()
        assert len(text.strip()) > 200
