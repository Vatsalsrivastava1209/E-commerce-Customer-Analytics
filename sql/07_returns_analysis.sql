-- Cancellation and return leakage by country.

SELECT
    Country AS country,
    COUNT(*) AS return_rows,
    SUM(Quantity * UnitPrice) AS return_value
FROM online_retail
WHERE Quantity < 0
   OR CAST(InvoiceNo AS VARCHAR) LIKE 'C%'
GROUP BY 1
ORDER BY return_rows DESC;
