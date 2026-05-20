# Olist E-Commerce Analytics Dashboard

An end-to-end data analytics pipeline built on 100,000+ real Brazilian e-commerce orders transforming raw transactional data into actionable business insights through advanced SQL analytics and interactive dashboards.

**Live Demo:** [Click here](https://ecommerce-analytics-sglnrpqfykatyf5s7wcbym.streamlit.app/) *(may take 30-60 seconds to load on first visit - free tier hosting)*

---

## Business Problem

Olist is a Brazilian e-commerce marketplace connecting 3,095 sellers to customers across 27 states. With 99,441 orders processed between 2016-2018, understanding revenue drivers, customer retention, and delivery performance is critical to growth.

This project answers 5 key business questions:

1. Which product categories and states drive the most revenue?
2. What is the customer retention rate and what does fixing it mean in dollars?
3. How does delivery performance impact customer satisfaction?
4. Which sellers are top performers?
5. Where are the biggest geographic opportunities?

---

## Key Business Insights

| Finding | Business Impact |
|---|---|
| 99.7% of customers never return after first purchase | Converting 5% to returning customers = R.67M additional revenue |
| Late deliveries score 2.57 vs 4.29 for on-time - 40% drop | 4,160 avoidable negative reviews per year |
| November 2017 Black Friday spike: 53% revenue jump | Seasonal planning opportunity |
| Sao Paulo generates 3x more revenue than Rio de Janeiro | Geographic concentration risk |
| Health and Beauty is the #1 category at 9.45% revenue share | Category investment priority |

---

## SQL Complexity Demonstrated

**Window Functions:**

RANK() OVER (ORDER BY total_revenue DESC) for seller rankings

SUM(total_revenue) OVER() for percentage share calculations

NTILE(4) OVER (ORDER BY total_spent DESC) for customer quartile segmentation

**CTEs (Common Table Expressions):**

Chained CTEs for multi-step customer segmentation analysis

Named intermediate results for readable complex queries

**Multi-table JOINs:**

5-table JOINs across orders, order_items, products, translations, and reviews

LEFT JOINs to preserve all orders regardless of review status

DATEDIFF calculations for delivery time and on-time performance

---

## Technical Stack

| Layer | Technology | Purpose |
|---|---|---|
| Storage | DuckDB | Columnar analytics database |
| Processing | Python + pandas | Data ingestion and cleaning |
| Analytics | DuckDB SQL | Window functions, CTEs, JOINs |
| Visualization | Streamlit + Plotly | 5-page interactive dashboard |
| Deployment | Streamlit Cloud | Live public URL |
| Version Control | Git + GitHub | Source control |

---

## Dashboard Pages

| Page | What It Shows |
|---|---|
| Overview | Revenue trends, KPIs, monthly order volume |
| Product Categories | Top 20 categories, revenue share, pricing analysis |
| Customer Insights | Segmentation, retention calculator, lifetime value |
| State Performance | Geographic revenue, delivery speed, satisfaction by state |
| Delivery Analysis | On-time vs late impact, avoidable negative reviews calculator |

---

## Dataset

Brazilian E-Commerce Public Dataset by Olist available on Kaggle

99,441 orders | 112,650 items | 3,095 sellers | 9 relational tables | 2016-2018

---

## How to Run Locally

git clone https://github.com/nithinkilari09/ecommerce-analytics.git

cd ecommerce-analytics

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

python src/ingest.py

streamlit run app/streamlit_app.py

---

## Author

**Nithin Kilari**

M.S. Computer Science (Data Science) - Oklahoma City University, 2026

LinkedIn: https://www.linkedin.com/in/kilari-nithin-619481272/

GitHub: https://github.com/nithinkilari09
