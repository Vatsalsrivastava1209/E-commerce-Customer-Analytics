-- Monthly repeat-purchase cohort retention.

WITH customer_orders AS (
    SELECT DISTINCT
        customer_id,
        invoice_no,
        DATE_TRUNC('month', invoice_date) AS order_month
    FROM clean_sales
),
cohorted AS (
    SELECT
        customer_id,
        order_month,
        MIN(order_month) OVER (PARTITION BY customer_id) AS cohort_month
    FROM customer_orders
),
retention AS (
    SELECT
        cohort_month,
        order_month,
        DATE_DIFF('month', cohort_month, order_month) AS months_since_first,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM cohorted
    GROUP BY 1,2,3
)
SELECT
    cohort_month,
    months_since_first,
    active_customers,
    active_customers * 1.0 / NULLIF(MAX(CASE WHEN months_since_first = 0 THEN active_customers END)
        OVER (PARTITION BY cohort_month), 0) AS retention_rate
FROM retention
ORDER BY cohort_month, months_since_first;
