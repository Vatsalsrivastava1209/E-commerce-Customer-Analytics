# Power Query Steps To Apply In Power BI

Use this as the manual checklist when updating the `.pbix` file.

1. Load `data/raw/online_retail.xlsx`.
2. Set data types:
   - `InvoiceNo`: text
   - `StockCode`: text
   - `Description`: text
   - `Quantity`: whole number
   - `InvoiceDate`: datetime
   - `UnitPrice`: decimal number
   - `CustomerID`: whole number
   - `Country`: text
3. Add flags:
   - `IsCancellation = Text.StartsWith([InvoiceNo], "C")`
   - `IsReturn = [Quantity] < 0`
   - `InvalidPrice = [UnitPrice] <= 0`
   - `MissingCustomer = [CustomerID] = null`
   - `IsPostage = Text.Upper([StockCode]) = "DOT" or Text.Contains(Text.Upper([Description]), "POSTAGE")`
4. Create a clean sales table by filtering:
   - `IsCancellation = false`
   - `IsReturn = false`
   - `InvalidPrice = false`
   - `MissingCustomer = false`
5. Add:
   - `NetRevenue = [Quantity] * [UnitPrice]`
   - `ProductRevenue = if [IsPostage] then 0 else [NetRevenue]`
   - `InvoiceMonth = Date.StartOfMonth(DateTime.Date([InvoiceDate]))`
6. Keep a raw table for data-quality and returns analysis.
7. Use clean sales for revenue, customer, AOV, product, RFM, and cohort visuals.
