-- Data quality checks for the UCI Online Retail dataset.
-- Assumes a table named online_retail with the raw Excel columns.

SELECT
    COUNT(*) AS raw_rows,
    SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END) AS missing_customer_rows,
    SUM(CASE WHEN CAST(InvoiceNo AS VARCHAR) LIKE 'C%' THEN 1 ELSE 0 END) AS cancelled_invoice_rows,
    SUM(CASE WHEN Quantity < 0 THEN 1 ELSE 0 END) AS negative_quantity_rows,
    SUM(CASE WHEN UnitPrice <= 0 THEN 1 ELSE 0 END) AS zero_or_negative_price_rows,
    SUM(CASE WHEN UPPER(CAST(StockCode AS VARCHAR)) = 'DOT'
           OR UPPER(Description) LIKE '%POSTAGE%' THEN 1 ELSE 0 END) AS postage_rows
FROM online_retail;
