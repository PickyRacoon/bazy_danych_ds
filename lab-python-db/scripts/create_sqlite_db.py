"""
Create a local SQLite database from generated CSV files.

Example:
    python scripts/create_sqlite_db.py --dataset medium --output output/northwind_plus.db
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

TABLE_ORDER = [
    "categories",
    "customers",
    "products",
    "orders",
    "order_items",
    "customers_dirty",
    "orders_dirty",
    "fact_sales",
]

INDEX_STATEMENTS = [
    "CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id)",
    "CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date)",
    "CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id)",
    "CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id)",
    "CREATE INDEX IF NOT EXISTS idx_fact_sales_date_country_category ON fact_sales(order_date, country, category_name)",
    "CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_id ON fact_sales(customer_id)",
]


def load_table(conn: sqlite3.Connection, csv_path: Path, table_name: str) -> None:
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded {table_name:16s} rows={len(df):8d}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["small", "medium"], default="medium")
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--output", type=Path, default=Path("output/northwind_plus.db"))
    args = parser.parse_args()

    dataset_dir = args.data_dir / args.dataset
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        args.output.unlink()

    with sqlite3.connect(args.output) as conn:
        for table_name in TABLE_ORDER:
            csv_path = dataset_dir / f"{table_name}.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"Missing CSV: {csv_path}")
            load_table(conn, csv_path, table_name)

        for statement in INDEX_STATEMENTS:
            conn.execute(statement)
        conn.commit()

    print(f"\nSQLite database created: {args.output}")


if __name__ == "__main__":
    main()
