-- Monthly net revenue and order trend.

SELECT
    invoice_month,
    SUM(gross_revenue) AS net_revenue,
    SUM(CASE WHEN NOT is_postage THEN gross_revenue ELSE 0 END) AS product_revenue,
    COUNT(DISTINCT invoice_no) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    SUM(gross_revenue) / NULLIF(COUNT(DISTINCT invoice_no), 0) AS average_order_value
FROM clean_sales
GROUP BY 1
ORDER BY 1;
