# Data Cleaning Methodology

The raw UCI Online Retail dataset contains transaction rows that must be handled before drawing business conclusions.

## Raw Data Issues

- `135,080` rows are missing `CustomerID`.
- `9,288` rows are cancelled invoice rows where `InvoiceNo` starts with `C`.
- `10,624` rows have negative quantities.
- `2,517` rows have zero or negative unit prices.
- `1,962` rows are postage/shipping related and should not be treated as physical product sales.

## Cleaning Rules

- Keep valid sales only when `CustomerID` is present, `Quantity > 0`, `UnitPrice > 0`, and `InvoiceNo` does not start with `C`.
- Calculate `NetRevenue = Quantity * UnitPrice` for valid sales.
- Separate postage/shipping rows from product revenue using `StockCode = DOT` or descriptions containing `POSTAGE`.
- Use product revenue, not total net revenue, when ranking physical products.
- Treat cancellations and negative quantities as return/revenue leakage indicators, not normal product demand.

## Why This Matters

Without these rules, the dashboard can overstate revenue, mis-rank products, distort customer value, and hide return leakage.
