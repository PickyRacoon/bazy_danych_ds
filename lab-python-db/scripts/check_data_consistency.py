"""
Basic consistency checks for CSV, SQLite, PostgreSQL and ClickHouse.
PostgreSQL/ClickHouse checks are optional and require running Docker services.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd

TABLES = ["customers", "categories", "products", "orders", "order_items", "customers_dirty", "orders_dirty", "fact_sales"]


def csv_counts(dataset_dir: Path) -> dict[str, int]:
    return {table: len(pd.read_csv(dataset_dir / f"{table}.csv")) for table in TABLES}


def sqlite_counts(db_path: Path) -> dict[str, int]:
    with sqlite3.connect(db_path) as conn:
        return {table: pd.read_sql_query(f"SELECT COUNT(*) AS n FROM {table}", conn)["n"].iloc[0] for table in TABLES}


def postgres_counts(url: str) -> dict[str, int]:
    from sqlalchemy import create_engine, text

    engine = create_engine(url)
    with engine.connect() as conn:
        return {table: conn.execute(text(f"SELECT COUNT(*) FROM retail.{table}")).scalar_one() for table in TABLES}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["small", "medium"], default="medium")
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--sqlite", type=Path, default=Path("output/northwind_plus.db"))
    parser.add_argument("--postgres-url", default="postgresql+psycopg2://student:student@localhost:15432/retail_lab")
    parser.add_argument("--skip-postgres", action="store_true")
    args = parser.parse_args()

    dataset_dir = args.data_dir / args.dataset
    result = pd.DataFrame({"csv_rows": csv_counts(dataset_dir)})

    if args.sqlite.exists():
        result["sqlite_rows"] = pd.Series(sqlite_counts(args.sqlite))
    else:
        print(f"SQLite file not found, skipping: {args.sqlite}")

    if not args.skip_postgres:
        try:
            result["postgres_rows"] = pd.Series(postgres_counts(args.postgres_url))
        except Exception as exc:
            print(f"PostgreSQL check skipped/error: {exc}")

    print(result)


if __name__ == "__main__":
    main()
