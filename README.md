# E-Commerce Customer Behavior and Sales Insights 

---

### Summary

This project provides a comprehensive analysis of the Online Retail dataset, culminating in an interactive Power BI dashboard. The dashboard visualizes key sales patterns, product performance,
and customer purchasing behaviors to support strategic business decisions.

---

### Business Problem

The primary goal of this analysis was to understand sales patterns and identify high-value customer segments. This involved answering key business questions such as:
- Who are our most valuable customers?
- What are our top-performing products?
- How does seasonality impact our sales?
- Which geographic markets drive sales volume versus transaction value?

---

### Data Source

The data used for this analysis is the **[Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/Online+Retail)** from the UCI Machine Learning Repository. It contains transactional data for a UK-based online retail company covering the period from **December 1st, 2010 to December 9th, 2011**.

---

### Tools & Technologies

* **Data Analysis & Modeling:** DAX (Data Analysis Expressions)
* **Data Transformation & Cleaning:** Power Query
* **Data Visualization & Dashboarding:** Microsoft Power BI

---

### Key Insights & Findings

The analysis yielded several critical insights into the business's operations:

1.  **Market Dominance vs. Customer Value:**
    * The **United Kingdom** is the dominant market, accounting for the vast majority of total orders and sales volume.
    * However, other countries such as the **Netherlands** and **Australia** demonstrate a significantly higher **Average Order Value (AOV)**, indicating that these markets contain customers who purchase higher-value items per transaction.

2.  **Strong Sales Seasonality:**
    * The business experiences a powerful seasonal trend, with sales consistently peaking in **November**. This highlights the importance of the holiday shopping season and provides a crucial window for targeted marketing and inventory management.

3.  **Product & Revenue Anomaly:**
    * The analysis of product sales revealed that **"DOTCOM POSTAGE"** is the single largest contributor to sales revenue. This finding suggests that shipping fees are likely categorized as product sales and should be analyzed separately to get a true picture of physical product performance.

4.  **High-Level Business Metrics:**
    * The dashboard provides a snapshot of key performance indicators, summarizing total sales revenue, order count, and the total number of unique customers.

---

### Dashboard Overview

The Power BI report is composed of two main pages:

* **Sales Overview:** Provides a high-level summary of business performance, including sales over time, sales by country, and top-selling products.
* **Customer Purchasing Analysis:** A deep dive into the "Value vs. Volume" narrative, directly comparing countries by their Average Order Value against their order counts.

---

### How to Use This Report

The dashboard is fully interactive:
* Use slicers to filter data by specific criteria.
* Click on data points in any visual (e.g., a country or a month) to cross-filter the entire report page and see related insights.

---

