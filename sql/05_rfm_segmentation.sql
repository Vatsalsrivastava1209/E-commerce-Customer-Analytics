-- RFM segmentation skeleton. Exact scoring can be implemented with NTILE in databases that support it.

WITH customer_metrics AS (
    SELECT
        customer_id,
        MAX(invoice_date) AS last_purchase,
        COUNT(DISTINCT invoice_no) AS frequency,
        SUM(gross_revenue) AS monetary
    FROM clean_sales
    GROUP BY 1
),
scored AS (
    SELECT
        *,
        NTILE(5) OVER (ORDER BY last_purchase ASC) AS recency_score,
        NTILE(5) OVER (ORDER BY frequency ASC) AS frequency_score,
        NTILE(5) OVER (ORDER BY monetary ASC) AS monetary_score
    FROM customer_metrics
)
SELECT
    customer_id,
    last_purchase,
    frequency,
    monetary,
    recency_score,
    frequency_score,
    monetary_score,
    CASE
        WHEN recency_score >= 4 AND frequency_score >= 4 AND monetary_score >= 4 THEN 'Champions'
        WHEN recency_score >= 3 AND frequency_score >= 4 THEN 'Loyal Customers'
        WHEN recency_score <= 2 AND frequency_score >= 3 AND monetary_score >= 3 THEN 'At Risk'
        WHEN monetary_score >= 4 THEN 'High Value'
        ELSE 'Needs Nurture'
    END AS segment
FROM scored;
