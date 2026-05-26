-- Clean sales view used for revenue, customer, and product analysis.

CREATE OR REPLACE VIEW clean_sales AS
SELECT
    CAST(InvoiceNo AS VARCHAR) AS invoice_no,
    CAST(StockCode AS VARCHAR) AS stock_code,
    Description AS description,
    Quantity AS quantity,
    InvoiceDate AS invoice_date,
    UnitPrice AS unit_price,
    CustomerID AS customer_id,
    Country AS country,
    Quantity * UnitPrice AS gross_revenue,
    DATE_TRUNC('month', InvoiceDate) AS invoice_month,
    CASE
        WHEN UPPER(CAST(StockCode AS VARCHAR)) = 'DOT'
          OR UPPER(Description) LIKE '%POSTAGE%'
        THEN TRUE ELSE FALSE
    END AS is_postage
FROM online_retail
WHERE CustomerID IS NOT NULL
  AND Quantity > 0
  AND UnitPrice > 0
  AND CAST(InvoiceNo AS VARCHAR) NOT LIKE 'C%';
