# Data Dictionary

| Field | Description |
| --- | --- |
| `InvoiceNo` | Invoice identifier. Values starting with `C` are cancellations. |
| `StockCode` | Product or service code. `DOT` is postage. |
| `Description` | Product/service description. |
| `Quantity` | Units purchased. Negative values usually indicate returns/cancellations. |
| `InvoiceDate` | Transaction timestamp. |
| `UnitPrice` | Unit sale price. Zero/negative values are excluded from valid sales. |
| `CustomerID` | Customer identifier. Missing IDs are excluded from customer-level analysis. |
| `Country` | Customer country. |

## Derived Fields

| Field | Description |
| --- | --- |
| `NetRevenue` | `Quantity * UnitPrice` for valid sales. |
| `ProductRevenue` | Net revenue excluding postage/shipping rows. |
| `InvoiceMonth` | Month of purchase. |
| `IsCancellation` | Whether `InvoiceNo` starts with `C`. |
| `IsReturn` | Whether quantity is negative. |
| `IsPostage` | Whether the row represents postage/shipping. |
| `IsValidSale` | Row passes the documented revenue/customer analysis filters. |
