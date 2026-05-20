# Olist E-Commerce Analytics Dashboard

An end-to-end data analytics pipeline built on 100,000+ real Brazilian e-commerce orders — transforming raw transactional data into actionable business insights through advanced SQL analytics and interactive dashboards.

**Live Demo:** [Click here](https://ecommerce-analytics-sglnrpqfykatyf5s7wcbym.streamlit.app/) *(may take 30 seconds to wake up on first visit — free tier hosting)* 

---

## Business Problem

Olist is a Brazilian e-commerce marketplace connecting small businesses to major retailers. With 99,441 orders across 3,095 sellers and 27 states, understanding revenue drivers, customer retention, and delivery performance is critical to growth.

This project answers 5 key business questions:
1. Which product categories and states drive the most revenue?
2. What is the customer retention rate — and what does fixing it mean in dollars?
3. How does delivery performance impact customer satisfaction?
4. Which sellers are top performers and which need intervention?
5. Where are the biggest geographic opportunities?

---

## Key Business Insights

| Finding | Impact |
|---|---|
| 99.7% of customers never return after first purchase | Fixing 5% retention = R$1.2M additional revenue |
| Late deliveries score 2.57 vs 4.29 for on-time — 40% drop | 4,160 avoidable negative reviews |
| November 2017 Black Friday spike: 53% revenue jump | Seasonal planning opportunity |
| SP generates 3x more revenue than #2 state RJ | Geographic concentration risk |
| Health & Beauty is #1 category at 9.45% revenue share | Category investment priority |

---

## SQL Complexity Demonstrated

This project uses production-level SQL including:

**Window Functions:**
```sql
RANK() OVER (ORDER BY total_revenue DESC)
SUM(total_revenue) OVER()  -- running totals
NTILE(4) OVER (ORDER BY total_spent DESC)  -- quartile segmentation
```

**CTEs (Common Table Expressions):**
```sql
WITH customer_orders AS (...),
     segmented AS (...)
SELECT * FROM segmented
```

**Multi-table JOINs:**
```sql
FROM orders o
JOIN order_items oi  ON o.order_id    = oi.order_id
JOIN products p      ON oi.product_id = p.product_id
JOIN translations t  ON p.product_category_name = t.product_category_name
LEFT JOIN reviews r  ON o.order_id    = r.order_id
```

---

## Technical Stack

| Layer | Technology |
|---|---|
| Data Storage | DuckDB — columnar analytics database |
| Data Processing | Python, pandas |
| SQL Analytics | DuckDB SQL — window functions, CTEs, multi-table JOINs |
| Visualization | Streamlit, Plotly |
| Version Control | Git, GitHub |

---

## Dashboard Pages

1. **Overview** — Revenue trends, KPIs, monthly order volume
2. **Product Categories** — Top 20 categories, revenue share, pricing analysis
3. **Customer Insights** — Segmentation, retention calculator, lifetime value
4. **State Performance** — Geographic revenue, delivery speed, satisfaction by state
5. **Delivery Analysis** — On-time vs late impact, avoidable negative reviews calculator

---

## Dataset

Brazilian E-Commerce Public Dataset by Olist — available on
[Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

99,441 orders | 112,650 items | 3,095 sellers | 99,441 customers | 2016–2018

---

## How to Run Locally

```bash
git clone https://github.com/nithinkilari09/ecommerce-analytics.git
cd ecommerce-analytics
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cd src && python ingest.py
cd .. && streamlit run app/streamlit_app.py
```

---

## Author

**Nithin Kilari**
M.S. Computer Science (Data Science) — Oklahoma City University, 2026
[LinkedIn](https://www.linkedin.com/in/kilari-nithin-619481272/) | [GitHub](https://github.com/nithinkilari09)