"""
A minimal example showing how students can write cleaned/derived data back to SQLite.
It is intentionally simple; labs can ask students to extend it.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

source_db = Path("output/northwind_plus.db")
target_db = Path("output/northwind_clean.db")

with sqlite3.connect(source_db) as conn:
    fact_sales = pd.read_sql_query("SELECT * FROM fact_sales", conn)

customer_kpis = (
    fact_sales
    .groupby(["customer_id", "company_name", "country"], as_index=False)
    .agg(
        orders_count=("order_id", "nunique"),
        order_items_count=("line_no", "count"),
        monetary=("line_value", "sum"),
        avg_line_value=("line_value", "mean"),
        last_order_date=("order_date", "max"),
    )
)

with sqlite3.connect(target_db) as conn:
    customer_kpis.to_sql("customer_kpis", conn, if_exists="replace", index=False)

print(f"Saved example cleaned/analytical table to {target_db}")
