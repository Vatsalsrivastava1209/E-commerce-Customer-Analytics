# Recommended DAX Measures

Use these measures in Power BI after applying the cleaning logic in Power Query.

```DAX
Net Revenue =
SUM('Online Retail Clean'[NetRevenue])

Product Revenue =
SUM('Online Retail Clean'[ProductRevenue])

Total Orders =
DISTINCTCOUNT('Online Retail Clean'[InvoiceNo])

Unique Customers =
DISTINCTCOUNT('Online Retail Clean'[CustomerID])

Average Order Value =
DIVIDE([Net Revenue], [Total Orders])

Revenue per Customer =
DIVIDE([Net Revenue], [Unique Customers])

Postage Revenue =
[Net Revenue] - [Product Revenue]

Return Rows =
COUNTROWS(FILTER('Online Retail Raw', 'Online Retail Raw'[Quantity] < 0))

Cancellation Rows =
COUNTROWS(FILTER('Online Retail Raw', LEFT('Online Retail Raw'[InvoiceNo], 1) = "C"))

Repeat Customers =
COUNTROWS(
    FILTER(
        SUMMARIZE(
            'Online Retail Clean',
            'Online Retail Clean'[CustomerID],
            "Order Count", DISTINCTCOUNT('Online Retail Clean'[InvoiceNo])
        ),
        [Order Count] > 1
    )
)

Repeat Customer Rate =
DIVIDE([Repeat Customers], [Unique Customers])
```
