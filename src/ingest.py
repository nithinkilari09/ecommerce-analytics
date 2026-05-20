import pandas as pd
import duckdb
import os

def ingest_all(data_dir: str, db_path: str):
    conn = duckdb.connect(db_path)

    files = {
        'orders':       'olist_orders_dataset.csv',
        'order_items':  'olist_order_items_dataset.csv',
        'payments':     'olist_order_payments_dataset.csv',
        'reviews':      'olist_order_reviews_dataset.csv',
        'customers':    'olist_customers_dataset.csv',
        'products':     'olist_products_dataset.csv',
        'sellers':      'olist_sellers_dataset.csv',
        'geolocation':  'olist_geolocation_dataset.csv',
        'translations': 'product_category_name_translation.csv',
    }

    for table, filename in files.items():
        path = os.path.join(data_dir, filename)
        df = pd.read_csv(path)
        conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.execute(f"CREATE TABLE {table} AS SELECT * FROM df")
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"Loaded {table}: {count:,} rows")

    print("\nAll tables loaded. Verifying schema...")
    tables = conn.execute("SHOW TABLES").fetchall()
    print("Tables in DuckDB:", [t[0] for t in tables])
    conn.close()
    print(f"\nDuckDB saved to: {db_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data', 'raw')
    db_path  = os.path.join(base_dir, 'data', 'ecommerce.duckdb')
    ingest_all(data_dir, db_path)