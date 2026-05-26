# Executive Summary: E-Commerce Revenue and Customer Behavior

## Business Question

Which markets, customers, and products should the business prioritize after cleaning the Online Retail transaction data?

## Key Results

- Cleaned `541,909` raw rows into `397,884` valid sales rows.
- Net revenue after cleaning: `8,911,408`.
- Orders: `18,532`; customers: `4,338`; AOV: `480.87`.
- Largest market by revenue: `United Kingdom` with `7,308,392` net revenue.
- Highest-AOV market with meaningful order volume: `Netherlands` at `3,036.66` AOV.
- November revenue was `66.1%` above the non-December monthly average.
- RFM segments include `953` Champions and `461` At Risk customers.

## Data Quality Notes

- Missing CustomerID rows: `135,080`.
- Cancelled invoice rows: `9,288`.
- Negative quantity rows: `10,624`.
- Zero or negative price rows: `2,517`.
- Postage rows separated from product revenue: `1,962`.

## Recommendations

1. Separate postage/shipping from product revenue in all product-performance reporting.
2. Use November seasonality to plan inventory and promotional campaigns earlier.
3. Prioritize high-AOV international markets for targeted campaigns, while treating the UK as the volume base.
4. Use RFM segments to create loyalty campaigns for Champions and win-back campaigns for At Risk customers.
5. Monitor cancellations/returns as a revenue leakage KPI instead of reporting only gross sales.

## Limitations

The dataset does not include marketing spend, acquisition channel, product cost, margin, web sessions, or inventory. Profitability and campaign ROI cannot be concluded from this dataset alone.
