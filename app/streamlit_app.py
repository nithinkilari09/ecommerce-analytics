# -*- coding: utf-8 -*-
import os
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Olist E-Commerce Analytics",
    page_icon="🛒",
    layout="wide"
)

# Connect to DuckDB
@st.cache_resource
def get_conn():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'data', 'ecommerce.duckdb')
    return duckdb.connect(db_path, read_only=True)

conn = get_conn()

# ── Sidebar Navigation ──
st.sidebar.title("Olist Analytics")
st.sidebar.markdown("Brazilian E-Commerce | 2016-2018")
page = st.sidebar.radio("Navigate", [
    "Overview",
    "Product Categories",
    "Customer Insights",
    "State Performance",
    "Delivery Analysis"
])

# ═══════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═══════════════════════════════════════
if page == "Overview":
    st.title("Olist E-Commerce — Business Overview")
    st.markdown("**99,441 orders | 96,478 delivered | 2016–2018 | Brazil**")
    st.markdown("---")

    # KPI cards
    kpis = conn.execute("""
        SELECT
            COUNT(DISTINCT o.order_id)              AS total_orders,
            COUNT(DISTINCT c.customer_unique_id)    AS unique_customers,
            ROUND(SUM(oi.price), 0)                 AS total_revenue,
            ROUND(AVG(oi.price), 2)                 AS avg_order_value,
            COUNT(DISTINCT oi.seller_id)            AS total_sellers,
            ROUND(AVG(r.review_score), 2)           AS avg_satisfaction
        FROM orders o
        JOIN order_items oi ON o.order_id   = oi.order_id
        JOIN customers c    ON o.customer_id = c.customer_id
        LEFT JOIN reviews r ON o.order_id   = r.order_id
        WHERE o.order_status = 'delivered'
    """).df()

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Orders", f"{int(kpis['total_orders'][0]):,}")
    c2.metric("Unique Customers", f"{int(kpis['unique_customers'][0]):,}")
    c3.metric("Total Revenue", f"R${int(kpis['total_revenue'][0]):,}")
    c4.metric("Avg Order Value", f"R${kpis['avg_order_value'][0]:.2f}")
    c5.metric("Active Sellers", f"{int(kpis['total_sellers'][0]):,}")
    c6.metric("Avg Satisfaction", f"{kpis['avg_satisfaction'][0]:.2f}/5")

    st.markdown("---")

    # Monthly revenue trend
    revenue = conn.execute("""
        SELECT
            DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS month,
            COUNT(DISTINCT o.order_id)          AS total_orders,
            ROUND(SUM(oi.price), 2)             AS total_revenue,
            ROUND(AVG(oi.price), 2)             AS avg_order_value
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE o.order_status = 'delivered'
          AND o.order_purchase_timestamp >= '2017-01-01'
        GROUP BY DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP))
        ORDER BY month
    """).df()
    revenue['month'] = pd.to_datetime(revenue['month'])

    col1, col2 = st.columns(2)
    with col1:
        fig = px.area(revenue, x='month', y='total_revenue',
                      title='Monthly Revenue Trend (BRL)',
                      color_discrete_sequence=['#3498db'])
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(revenue, x='month', y='total_orders',
                     title='Monthly Order Volume',
                     color_discrete_sequence=['#2ecc71'])
        st.plotly_chart(fig, use_container_width=True)

    # Key insights
    st.markdown("---")
    st.subheader("Key Business Insights")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("November 2017 saw a 53% revenue spike — Black Friday effect. Orders jumped from 4,478 to 7,289 in one month.")
    with col2:
        st.warning("99.7% of customers never return after their first purchase — critical retention problem.")
    with col3:
        st.error("Late deliveries receive 2.57 avg review vs 4.29 for on-time — a 40% satisfaction drop costing customer loyalty.")

# ═══════════════════════════════════════
# PAGE 2 — PRODUCT CATEGORIES
# ═══════════════════════════════════════
elif page == "Product Categories":
    st.title("Product Category Analysis")
    st.markdown("---")

    categories = conn.execute("""
        WITH category_revenue AS (
            SELECT
                t.product_category_name_english     AS category,
                COUNT(DISTINCT o.order_id)          AS total_orders,
                ROUND(SUM(oi.price), 2)             AS total_revenue,
                ROUND(AVG(oi.price), 2)             AS avg_price,
                COUNT(DISTINCT oi.seller_id)        AS num_sellers,
                ROUND(AVG(r.review_score), 2)       AS avg_review
            FROM orders o
            JOIN order_items oi  ON o.order_id    = oi.order_id
            JOIN products p      ON oi.product_id = p.product_id
            JOIN translations t  ON p.product_category_name = t.product_category_name
            LEFT JOIN reviews r  ON o.order_id    = r.order_id
            WHERE o.order_status = 'delivered'
            GROUP BY t.product_category_name_english
        )
        SELECT *,
            ROUND(total_revenue * 100.0 / SUM(total_revenue) OVER(), 2) AS revenue_share_pct,
            RANK() OVER (ORDER BY total_revenue DESC) AS revenue_rank
        FROM category_revenue
        ORDER BY total_revenue DESC
        LIMIT 20
    """).df()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(categories, x='total_revenue', y='category',
                     orientation='h', title='Top 20 Categories by Revenue',
                     color='total_revenue', color_continuous_scale='Blues')
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(categories, x='total_orders', y='avg_price',
                         size='revenue_share_pct', color='category',
                         title='Orders vs Avg Price (bubble = revenue share)',
                         hover_data=['total_revenue', 'num_sellers'])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(categories.head(8), values='revenue_share_pct',
                     names='category', title='Revenue Share — Top 8 Categories')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(categories.head(10), x='category', y='avg_review',
                     title='Avg Review Score by Category',
                     color='avg_review', color_continuous_scale='RdYlGn',
                     range_color=[3.5, 5])
        fig.update_layout(xaxis_tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Category Data Table")
    st.dataframe(categories, use_container_width=True)

# ═══════════════════════════════════════
# PAGE 3 — CUSTOMER INSIGHTS
# ═══════════════════════════════════════
elif page == "Customer Insights":
    st.title("Customer Insights")
    st.markdown("---")

    segments = conn.execute("""
        WITH customer_orders AS (
            SELECT
                c.customer_unique_id,
                c.customer_state,
                COUNT(DISTINCT o.order_id)      AS total_orders,
                ROUND(SUM(oi.price), 2)         AS total_spent,
                ROUND(AVG(r.review_score), 2)   AS avg_review
            FROM orders o
            JOIN order_items oi ON o.order_id   = oi.order_id
            JOIN customers c    ON o.customer_id = c.customer_id
            LEFT JOIN reviews r ON o.order_id   = r.order_id
            WHERE o.order_status = 'delivered'
            GROUP BY c.customer_unique_id, c.customer_state
        ),
        segmented AS (
            SELECT *,
                CASE
                    WHEN total_orders >= 3 THEN 'Loyal'
                    WHEN total_orders = 2  THEN 'Returning'
                    ELSE                       'One-time'
                END AS segment
            FROM customer_orders
        )
        SELECT
            segment,
            COUNT(*)                        AS num_customers,
            ROUND(AVG(total_spent), 2)      AS avg_lifetime_value,
            ROUND(AVG(total_orders), 2)     AS avg_orders,
            ROUND(AVG(avg_review), 2)       AS avg_satisfaction,
            ROUND(SUM(total_spent), 2)      AS segment_revenue
        FROM segmented
        GROUP BY segment
        ORDER BY num_customers DESC
    """).df()

    # KPIs
    c1, c2, c3 = st.columns(3)
    for i, row in segments.iterrows():
        col = [c1, c2, c3][i]
        col.metric(
            f"{row['segment']} Customers",
            f"{int(row['num_customers']):,}",
            f"R${row['avg_lifetime_value']:.0f} avg value"
        )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(segments, values='num_customers', names='segment',
                     title='Customer Distribution by Segment',
                     color_discrete_map={
                         'One-time': '#e74c3c',
                         'Returning': '#f39c12',
                         'Loyal': '#2ecc71'
                     })
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(segments, x='segment', y='segment_revenue',
                     title='Total Revenue by Customer Segment',
                     color='segment',
                     color_discrete_map={
                         'One-time': '#e74c3c',
                         'Returning': '#f39c12',
                         'Loyal': '#2ecc71'
                     })
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Retention Opportunity Calculator")
    st.markdown("If we convert X% of one-time customers to returning customers:")
    pct = st.slider("Conversion rate (%)", 1, 20, 5)
    one_time = int(segments[segments['segment'] == 'One-time']['num_customers'].values[0])
    avg_return_value = float(segments[segments['segment'] == 'Returning']['avg_lifetime_value'].values[0])
    converted = int(one_time * pct / 100)
    additional_revenue = converted * avg_return_value
    col1, col2 = st.columns(2)
    col1.metric("Customers Converted", f"{converted:,}")
    col2.metric("Additional Revenue", f"R${additional_revenue:,.0f}")

# ═══════════════════════════════════════
# PAGE 4 — STATE PERFORMANCE
# ═══════════════════════════════════════
elif page == "State Performance":
    st.title("State Performance Analysis")
    st.markdown("---")

    states = conn.execute("""
        SELECT
            c.customer_state                    AS state,
            COUNT(DISTINCT o.order_id)          AS total_orders,
            ROUND(SUM(oi.price), 2)             AS total_revenue,
            ROUND(AVG(oi.price), 2)             AS avg_order_value,
            ROUND(AVG(r.review_score), 2)       AS avg_review_score,
            ROUND(AVG(
                DATEDIFF('day',
                    CAST(o.order_purchase_timestamp AS TIMESTAMP),
                    CAST(o.order_delivered_customer_date AS TIMESTAMP))
            ), 1)                               AS avg_delivery_days,
            ROUND(AVG(oi.freight_value), 2)     AS avg_freight_cost
        FROM orders o
        JOIN order_items oi  ON o.order_id   = oi.order_id
        JOIN customers c     ON o.customer_id = c.customer_id
        LEFT JOIN reviews r  ON o.order_id   = r.order_id
        WHERE o.order_status = 'delivered'
          AND o.order_delivered_customer_date IS NOT NULL
        GROUP BY c.customer_state
        ORDER BY total_revenue DESC
    """).df()

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(states.head(15), x='state', y='total_revenue',
                     title='Top 15 States by Revenue',
                     color='total_revenue', color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.scatter(states, x='avg_delivery_days', y='avg_review_score',
                         size='total_orders', color='state',
                         title='Delivery Days vs Satisfaction (bubble = order volume)',
                         hover_data=['total_revenue', 'avg_freight_cost'])
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(states.sort_values('avg_delivery_days').head(10),
                     x='state', y='avg_delivery_days',
                     title='Top 10 Fastest Delivery States',
                     color='avg_delivery_days',
                     color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.bar(states.sort_values('avg_review_score', ascending=False).head(10),
                     x='state', y='avg_review_score',
                     title='Top 10 States by Customer Satisfaction',
                     color='avg_review_score',
                     color_continuous_scale='RdYlGn',
                     range_color=[3.5, 5])
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("State Data Table")
    st.dataframe(states, use_container_width=True)

# ═══════════════════════════════════════
# PAGE 5 — DELIVERY ANALYSIS
# ═══════════════════════════════════════
elif page == "Delivery Analysis":
    st.title("Delivery Performance Analysis")
    st.markdown("---")

    delivery = conn.execute("""
        WITH delivery_data AS (
            SELECT
                o.order_id,
                DATEDIFF('day',
                    CAST(o.order_purchase_timestamp AS TIMESTAMP),
                    CAST(o.order_delivered_customer_date AS TIMESTAMP)
                ) AS actual_days,
                CASE
                    WHEN CAST(o.order_delivered_customer_date AS TIMESTAMP)
                         <= CAST(o.order_estimated_delivery_date AS TIMESTAMP)
                    THEN 'On Time'
                    ELSE 'Late'
                END AS status,
                r.review_score
            FROM orders o
            LEFT JOIN reviews r ON o.order_id = r.order_id
            WHERE o.order_status = 'delivered'
              AND o.order_delivered_customer_date IS NOT NULL
              AND o.order_estimated_delivery_date IS NOT NULL
        )
        SELECT
            status,
            COUNT(*)                                    AS total_orders,
            ROUND(AVG(actual_days), 1)                  AS avg_delivery_days,
            ROUND(AVG(review_score), 3)                 AS avg_review,
            ROUND(COUNT(CASE WHEN review_score >= 4 THEN 1 END) * 100.0 / COUNT(*), 1) AS positive_pct,
            ROUND(COUNT(CASE WHEN review_score <= 2 THEN 1 END) * 100.0 / COUNT(*), 1) AS negative_pct
        FROM delivery_data
        GROUP BY status
    """).df()

    # KPIs
    for _, row in delivery.iterrows():
        color = "normal" if row['status'] == 'On Time' else "inverse"
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(f"{row['status']} Orders", f"{int(row['total_orders']):,}")
        c2.metric("Avg Delivery Days", f"{row['avg_delivery_days']} days")
        c3.metric("Avg Review Score", f"{row['avg_review']}/5")
        c4.metric("Positive Reviews", f"{row['positive_pct']}%")
        st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(delivery, x='status', y='avg_review',
                     title='Avg Review Score: On Time vs Late',
                     color='status',
                     color_discrete_map={'On Time': '#2ecc71', 'Late': '#e74c3c'})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Positive Reviews',
                             x=delivery['status'], y=delivery['positive_pct'],
                             marker_color='#2ecc71'))
        fig.add_trace(go.Bar(name='Negative Reviews',
                             x=delivery['status'], y=delivery['negative_pct'],
                             marker_color='#e74c3c'))
        fig.update_layout(title='Review Distribution: On Time vs Late',
                          barmode='group')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Business Impact of Late Deliveries")
    late_orders = int(delivery[delivery['status'] == 'Late']['total_orders'].values[0])
    neg_pct_late = float(delivery[delivery['status'] == 'Late']['negative_pct'].values[0])
    neg_pct_ontime = float(delivery[delivery['status'] == 'On Time']['negative_pct'].values[0])
    avoidable_negative = int(late_orders * (neg_pct_late - neg_pct_ontime) / 100)

    c1, c2, c3 = st.columns(3)
    c1.metric("Late Orders", f"{late_orders:,}")
    c2.metric("Avoidable Negative Reviews", f"{avoidable_negative:,}")
    c3.metric("Satisfaction Drop", f"{delivery[delivery['status']=='Late']['avg_review'].values[0]:.2f} vs {delivery[delivery['status']=='On Time']['avg_review'].values[0]:.2f}")

    st.error(f"If all late orders were on time, approximately {avoidable_negative:,} negative reviews could be eliminated — directly improving seller ratings and customer retention.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Built with DuckDB + Streamlit")
st.sidebar.markdown("Data: Olist Brazilian E-Commerce")
st.sidebar.markdown("Nithin Kilari | 2026")