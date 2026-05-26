"""Clean and analyze the UCI Online Retail dataset for the portfolio case study."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


RAW_PATH = Path("data/raw/online_retail.xlsx")
PROCESSED_DIR = Path("data/processed")
REPORTS_DIR = Path("reports")
FIGURES_DIR = REPORTS_DIR / "figures"
SNAPSHOT_DATE = pd.Timestamp("2011-12-10")


def ensure_dirs() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_raw(path: Path = RAW_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Missing raw dataset: {path}")
    data = pd.read_excel(path)
    data.columns = [str(column).strip() for column in data.columns]
    return data


def classify_rows(data: pd.DataFrame) -> pd.DataFrame:
    cleaned = data.copy()
    cleaned["InvoiceNo"] = cleaned["InvoiceNo"].astype(str)
    cleaned["StockCode"] = cleaned["StockCode"].astype(str).str.strip()
    cleaned["Description"] = cleaned["Description"].astype("string").str.strip()
    cleaned["InvoiceDate"] = pd.to_datetime(cleaned["InvoiceDate"], errors="coerce")
    cleaned["CustomerID"] = pd.to_numeric(cleaned["CustomerID"], errors="coerce")
    cleaned["Quantity"] = pd.to_numeric(cleaned["Quantity"], errors="coerce")
    cleaned["UnitPrice"] = pd.to_numeric(cleaned["UnitPrice"], errors="coerce")
    cleaned["GrossRevenue"] = cleaned["Quantity"] * cleaned["UnitPrice"]
    cleaned["InvoiceMonth"] = cleaned["InvoiceDate"].dt.to_period("M").astype(str)
    cleaned["IsCancellation"] = cleaned["InvoiceNo"].str.startswith("C")
    cleaned["IsReturn"] = cleaned["Quantity"] < 0
    cleaned["InvalidPrice"] = cleaned["UnitPrice"] <= 0
    cleaned["MissingCustomer"] = cleaned["CustomerID"].isna()
    cleaned["IsPostage"] = (
        cleaned["StockCode"].str.upper().eq("DOT")
        | cleaned["Description"].str.upper().str.contains("POSTAGE", na=False)
    )
    cleaned["IsValidSale"] = (
        ~cleaned["IsCancellation"]
        & ~cleaned["IsReturn"]
        & ~cleaned["InvalidPrice"]
        & ~cleaned["MissingCustomer"]
    )
    cleaned["ProductRevenue"] = np.where(
        cleaned["IsValidSale"] & ~cleaned["IsPostage"], cleaned["GrossRevenue"], 0.0
    )
    cleaned["NetRevenue"] = np.where(cleaned["IsValidSale"], cleaned["GrossRevenue"], 0.0)
    return cleaned


def rfm_segments(valid_sales: pd.DataFrame) -> pd.DataFrame:
    customer = (
        valid_sales.groupby("CustomerID")
        .agg(
            last_purchase=("InvoiceDate", "max"),
            frequency=("InvoiceNo", "nunique"),
            monetary=("NetRevenue", "sum"),
            country=("Country", lambda values: values.mode().iloc[0] if not values.mode().empty else values.iloc[0]),
        )
        .reset_index()
    )
    customer["recency_days"] = (SNAPSHOT_DATE - customer["last_purchase"]).dt.days
    customer["r_score"] = pd.qcut(customer["recency_days"], 5, labels=[5, 4, 3, 2, 1], duplicates="drop").astype(int)
    customer["f_score"] = pd.qcut(customer["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    customer["m_score"] = pd.qcut(customer["monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    customer["rfm_score"] = customer["r_score"] + customer["f_score"] + customer["m_score"]

    def label(row: pd.Series) -> str:
        if row["r_score"] >= 4 and row["f_score"] >= 4 and row["m_score"] >= 4:
            return "Champions"
        if row["r_score"] >= 3 and row["f_score"] >= 4:
            return "Loyal Customers"
        if row["r_score"] <= 2 and row["f_score"] >= 3 and row["m_score"] >= 3:
            return "At Risk"
        if row["r_score"] >= 4 and row["frequency"] <= 2:
            return "New Customers"
        if row["m_score"] >= 4:
            return "High Value"
        return "Needs Nurture"

    customer["segment"] = customer.apply(label, axis=1)
    return customer


def cohort_retention(valid_sales: pd.DataFrame) -> pd.DataFrame:
    sales = valid_sales.copy()
    sales["cohort_month"] = sales.groupby("CustomerID")["InvoiceDate"].transform("min").dt.to_period("M")
    sales["order_month"] = sales["InvoiceDate"].dt.to_period("M")
    sales["months_since_first"] = (
        (sales["order_month"].dt.year - sales["cohort_month"].dt.year) * 12
        + (sales["order_month"].dt.month - sales["cohort_month"].dt.month)
    )
    cohort = (
        sales.groupby(["cohort_month", "months_since_first"])["CustomerID"]
        .nunique()
        .reset_index(name="active_customers")
    )
    sizes = cohort[cohort["months_since_first"] == 0][["cohort_month", "active_customers"]].rename(
        columns={"active_customers": "cohort_size"}
    )
    cohort = cohort.merge(sizes, on="cohort_month")
    cohort["retention_rate"] = cohort["active_customers"] / cohort["cohort_size"]
    cohort["cohort_month"] = cohort["cohort_month"].astype(str)
    return cohort


def build_outputs(data: pd.DataFrame) -> dict:
    valid_sales = data[data["IsValidSale"]].copy()
    product_sales = valid_sales[~valid_sales["IsPostage"]].copy()
    returns = data[data["IsReturn"] | data["IsCancellation"]].copy()

    monthly = (
        valid_sales.groupby("InvoiceMonth")
        .agg(
            net_revenue=("NetRevenue", "sum"),
            product_revenue=("ProductRevenue", "sum"),
            orders=("InvoiceNo", "nunique"),
            customers=("CustomerID", "nunique"),
        )
        .reset_index()
    )
    monthly["aov"] = monthly["net_revenue"] / monthly["orders"]

    country = (
        valid_sales.groupby("Country")
        .agg(
            net_revenue=("NetRevenue", "sum"),
            product_revenue=("ProductRevenue", "sum"),
            orders=("InvoiceNo", "nunique"),
            customers=("CustomerID", "nunique"),
        )
        .reset_index()
    )
    country["aov"] = country["net_revenue"] / country["orders"]
    country["revenue_per_customer"] = country["net_revenue"] / country["customers"]

    products = (
        product_sales.groupby(["StockCode", "Description"])
        .agg(product_revenue=("ProductRevenue", "sum"), quantity=("Quantity", "sum"), orders=("InvoiceNo", "nunique"))
        .reset_index()
        .sort_values("product_revenue", ascending=False)
    )

    returns_summary = (
        returns.groupby("Country")
        .agg(return_rows=("InvoiceNo", "count"), return_value=("GrossRevenue", "sum"))
        .reset_index()
        .sort_values("return_rows", ascending=False)
    )

    rfm = rfm_segments(valid_sales)
    cohort = cohort_retention(valid_sales)

    return {
        "cleaned_transactions": data,
        "valid_sales": valid_sales,
        "monthly_revenue": monthly,
        "country_performance": country,
        "top_products": products,
        "returns_by_country": returns_summary,
        "rfm_segments": rfm,
        "cohort_retention": cohort,
    }


def make_figures(outputs: dict) -> None:
    sns.set_theme(style="whitegrid")

    monthly = outputs["monthly_revenue"]
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=monthly, x="InvoiceMonth", y="net_revenue", marker="o")
    plt.title("Monthly Net Revenue")
    plt.xlabel("")
    plt.ylabel("Net revenue")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "monthly_revenue.png", dpi=160)
    plt.close()

    country = outputs["country_performance"].sort_values("net_revenue", ascending=False).head(12)
    plt.figure(figsize=(10, 5))
    sns.barplot(data=country, x="net_revenue", y="Country")
    plt.title("Top Countries by Net Revenue")
    plt.xlabel("Net revenue")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "country_revenue.png", dpi=160)
    plt.close()

    rfm_counts = outputs["rfm_segments"]["segment"].value_counts().reset_index()
    rfm_counts.columns = ["segment", "customers"]
    plt.figure(figsize=(9, 5))
    sns.barplot(data=rfm_counts, x="customers", y="segment")
    plt.title("RFM Customer Segments")
    plt.xlabel("Customers")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "rfm_segments.png", dpi=160)
    plt.close()

    cohort = outputs["cohort_retention"]
    pivot = cohort.pivot(index="cohort_month", columns="months_since_first", values="retention_rate").fillna(0)
    plt.figure(figsize=(11, 6))
    sns.heatmap(pivot, cmap="Blues", vmin=0, vmax=1)
    plt.title("Monthly Cohort Retention")
    plt.xlabel("Months since first purchase")
    plt.ylabel("First purchase cohort")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "cohort_retention.png", dpi=160)
    plt.close()


def write_outputs(outputs: dict) -> dict:
    for name, frame in outputs.items():
        frame.to_csv(PROCESSED_DIR / f"{name}.csv", index=False)

    raw = outputs["cleaned_transactions"]
    valid = outputs["valid_sales"]
    country = outputs["country_performance"]
    monthly = outputs["monthly_revenue"]
    products = outputs["top_products"]
    rfm = outputs["rfm_segments"]
    returns = outputs["returns_by_country"]

    top_country = country.sort_values("net_revenue", ascending=False).iloc[0]
    high_aov = country[country["orders"] >= 20].sort_values("aov", ascending=False).iloc[0]
    top_product = products.iloc[0]
    champion_count = int((rfm["segment"] == "Champions").sum())
    at_risk_count = int((rfm["segment"] == "At Risk").sum())
    november = monthly[monthly["InvoiceMonth"] == "2011-11"].iloc[0]
    avg_monthly = monthly[monthly["InvoiceMonth"] != "2011-12"]["net_revenue"].mean()
    return_rows = int((raw["IsReturn"] | raw["IsCancellation"]).sum())

    summary = {
        "raw_rows": int(len(raw)),
        "valid_sales_rows": int(len(valid)),
        "missing_customer_rows": int(raw["MissingCustomer"].sum()),
        "cancelled_invoice_rows": int(raw["IsCancellation"].sum()),
        "negative_quantity_rows": int(raw["IsReturn"].sum()),
        "zero_or_negative_price_rows": int(raw["InvalidPrice"].sum()),
        "postage_rows": int(raw["IsPostage"].sum()),
        "net_revenue": float(valid["NetRevenue"].sum()),
        "product_revenue": float(valid["ProductRevenue"].sum()),
        "orders": int(valid["InvoiceNo"].nunique()),
        "customers": int(valid["CustomerID"].nunique()),
        "aov": float(valid["NetRevenue"].sum() / valid["InvoiceNo"].nunique()),
        "top_country": str(top_country["Country"]),
        "top_country_revenue": float(top_country["net_revenue"]),
        "high_aov_country": str(high_aov["Country"]),
        "high_aov": float(high_aov["aov"]),
        "top_product": str(top_product["Description"]),
        "top_product_revenue": float(top_product["product_revenue"]),
        "champion_customers": champion_count,
        "at_risk_customers": at_risk_count,
        "november_revenue": float(november["net_revenue"]),
        "november_vs_avg_month": float(november["net_revenue"] / avg_monthly - 1),
        "return_rows": return_rows,
        "top_return_country": str(returns.iloc[0]["Country"]) if not returns.empty else "n/a",
    }
    (REPORTS_DIR / "analysis_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    write_executive_summary(summary)
    return summary


def write_executive_summary(summary: dict) -> None:
    text = f"""# Executive Summary: E-Commerce Revenue and Customer Behavior

## Business Question

Which markets, customers, and products should the business prioritize after cleaning the Online Retail transaction data?

## Key Results

- Cleaned `{summary['raw_rows']:,}` raw rows into `{summary['valid_sales_rows']:,}` valid sales rows.
- Net revenue after cleaning: `{summary['net_revenue']:,.0f}`.
- Orders: `{summary['orders']:,}`; customers: `{summary['customers']:,}`; AOV: `{summary['aov']:,.2f}`.
- Largest market by revenue: `{summary['top_country']}` with `{summary['top_country_revenue']:,.0f}` net revenue.
- Highest-AOV market with meaningful order volume: `{summary['high_aov_country']}` at `{summary['high_aov']:,.2f}` AOV.
- November revenue was `{summary['november_vs_avg_month']:.1%}` above the non-December monthly average.
- RFM segments include `{summary['champion_customers']:,}` Champions and `{summary['at_risk_customers']:,}` At Risk customers.

## Data Quality Notes

- Missing CustomerID rows: `{summary['missing_customer_rows']:,}`.
- Cancelled invoice rows: `{summary['cancelled_invoice_rows']:,}`.
- Negative quantity rows: `{summary['negative_quantity_rows']:,}`.
- Zero or negative price rows: `{summary['zero_or_negative_price_rows']:,}`.
- Postage rows separated from product revenue: `{summary['postage_rows']:,}`.

## Recommendations

1. Separate postage/shipping from product revenue in all product-performance reporting.
2. Use November seasonality to plan inventory and promotional campaigns earlier.
3. Prioritize high-AOV international markets for targeted campaigns, while treating the UK as the volume base.
4. Use RFM segments to create loyalty campaigns for Champions and win-back campaigns for At Risk customers.
5. Monitor cancellations/returns as a revenue leakage KPI instead of reporting only gross sales.

## Limitations

The dataset does not include marketing spend, acquisition channel, product cost, margin, web sessions, or inventory. Profitability and campaign ROI cannot be concluded from this dataset alone.
"""
    (REPORTS_DIR / "executive_summary.md").write_text(text, encoding="utf-8")


def main() -> int:
    ensure_dirs()
    raw = load_raw()
    cleaned = classify_rows(raw)
    outputs = build_outputs(cleaned)
    make_figures(outputs)
    summary = write_outputs(outputs)
    print(
        "Analysis complete: "
        f"{summary['orders']:,} orders, {summary['customers']:,} customers, "
        f"{summary['net_revenue']:,.0f} net revenue."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
