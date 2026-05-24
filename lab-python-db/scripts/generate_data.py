"""
Generate a synthetic Northwind-like retail transaction dataset for labs:
Python + databases, SQL vs pandas, long-to-wide transformations, cohorts,
pipeline building, and optional ClickHouse aggregation examples.

Outputs for each dataset size:
- customers.csv
- categories.csv
- products.csv
- orders.csv
- order_items.csv
- fact_sales.csv
- customers_dirty.csv
- orders_dirty.csv
"""

from __future__ import annotations

import argparse
from pathlib import Path
import random
import string
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

SEED = 20260509

COUNTRY_CITIES: Dict[str, List[str]] = {
    "Poland": ["Warsaw", "Krakow", "Gdansk", "Poznan", "Wroclaw", "Lodz"],
    "Germany": ["Berlin", "Munich", "Hamburg", "Cologne", "Frankfurt"],
    "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"],
    "USA": ["New York", "Chicago", "Boston", "Seattle", "Austin", "Denver"],
    "United Kingdom": ["London", "Manchester", "Bristol", "Liverpool", "Leeds"],
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao"],
    "Italy": ["Rome", "Milan", "Florence", "Turin", "Naples"],
    "Netherlands": ["Amsterdam", "Rotterdam", "Utrecht", "Eindhoven"],
    "Sweden": ["Stockholm", "Gothenburg", "Malmo", "Uppsala"],
    "Norway": ["Oslo", "Bergen", "Trondheim", "Stavanger"],
    "Czech Republic": ["Prague", "Brno", "Ostrava", "Pilsen"],
    "Austria": ["Vienna", "Graz", "Linz", "Salzburg"],
    "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa"],
}

CATEGORY_NAMES = [
    "Beverages",
    "Dairy",
    "Seafood",
    "Meat",
    "Bakery",
    "Confections",
    "Produce",
    "Grains",
    "Spices",
    "Frozen Foods",
    "Snacks",
    "Household",
    "Coffee & Tea",
    "Condiments",
    "Prepared Meals",
]

PRODUCT_ADJECTIVES = [
    "Premium", "Classic", "Organic", "Fresh", "Smoked", "Dried", "Sweet", "Salted",
    "Traditional", "Golden", "Natural", "Imported", "Local", "Family", "Craft",
]

PRODUCT_NOUNS = {
    "Beverages": ["Tea", "Coffee", "Juice", "Soda", "Mineral Water", "Lemonade"],
    "Dairy": ["Cheese", "Yogurt", "Milk", "Butter", "Cream"],
    "Seafood": ["Salmon", "Tuna", "Shrimp", "Cod", "Herring"],
    "Meat": ["Ham", "Sausage", "Bacon", "Chicken", "Beef"],
    "Bakery": ["Bread", "Bun", "Croissant", "Cake", "Muffin"],
    "Confections": ["Chocolate", "Cookie", "Candy", "Caramel", "Biscuit"],
    "Produce": ["Apple", "Tomato", "Potato", "Carrot", "Onion"],
    "Grains": ["Rice", "Pasta", "Oats", "Flour", "Cereal"],
    "Spices": ["Pepper", "Paprika", "Cinnamon", "Basil", "Oregano"],
    "Frozen Foods": ["Pizza", "Vegetables", "Dumplings", "Fries", "Dessert"],
    "Snacks": ["Chips", "Nuts", "Crackers", "Popcorn", "Pretzels"],
    "Household": ["Soap", "Towels", "Cleaner", "Napkins", "Bags"],
    "Coffee & Tea": ["Espresso", "Green Tea", "Black Tea", "Cocoa", "Herbal Tea"],
    "Condiments": ["Mustard", "Ketchup", "Sauce", "Vinegar", "Mayonnaise"],
    "Prepared Meals": ["Soup", "Lasagna", "Curry", "Stew", "Salad"],
}

COMPANY_PREFIXES = [
    "Alfa", "Beta", "Gamma", "Delta", "Nova", "Prime", "Green", "Blue", "Silver", "Amber",
    "Baltic", "Central", "Euro", "Fresh", "Urban", "Global", "Royal", "North", "East", "West",
]

COMPANY_SUFFIXES = [
    "Foods", "Market", "Trading", "Supplies", "Gourmet", "Distribution", "Stores",
    "Wholesale", "Cafe", "Restaurant", "Deli", "Partners", "Group", "Kitchen",
]

CUSTOMER_TYPES = ["retail", "wholesale", "horeca", "online", "distributor"]


def random_phone(rng: np.random.Generator) -> str:
    country_code = rng.choice(["+48", "+49", "+33", "+1", "+44", "+34", "+39"])
    parts = ["".join(rng.choice(list(string.digits), size=3)) for _ in range(3)]
    return f"{country_code} {parts[0]} {parts[1]} {parts[2]}"


def weighted_dates(
    rng: np.random.Generator,
    n: int,
    start: str = "2023-01-01",
    end: str = "2025-12-31",
) -> pd.Series:
    days = pd.date_range(start, end, freq="D")
    weights = np.ones(len(days), dtype=float)

    # Seasonality: more orders toward Q4 and Mondays/Fridays.
    months = pd.Series(days.month)
    weights *= np.where(months.isin([10, 11, 12]), 1.45, 1.0)
    weights *= np.where(months.isin([6, 7]), 1.15, 1.0)
    weekdays = pd.Series(days.weekday)
    weights *= np.where(weekdays.isin([0, 4]), 1.15, 1.0)

    # A few promotion/spike days for anomaly-detection exercises.
    spike_days = pd.to_datetime(["2023-11-24", "2024-06-03", "2024-11-29", "2025-06-02", "2025-12-15"])
    for spike in spike_days:
        idx = np.where(days == spike)[0]
        if len(idx):
            weights[idx[0]] *= 5.0
            # Add small halo around promotion day.
            for shift in [-1, 1]:
                halo_idx = np.where(days == spike + pd.Timedelta(days=shift))[0]
                if len(halo_idx):
                    weights[halo_idx[0]] *= 2.0

    weights = weights / weights.sum()
    sampled = rng.choice(days, size=n, replace=True, p=weights)
    sampled = pd.to_datetime(sampled).sort_values()
    return pd.Series(sampled).reset_index(drop=True)


def generate_customers(rng: np.random.Generator, n_customers: int) -> pd.DataFrame:
    countries = list(COUNTRY_CITIES.keys())
    country_weights = np.array([0.14, 0.13, 0.10, 0.12, 0.10, 0.08, 0.07, 0.06, 0.04, 0.03, 0.05, 0.04, 0.04])
    country_weights = country_weights / country_weights.sum()

    rows = []
    used_names = set()
    registration_dates = weighted_dates(rng, n_customers, "2021-01-01", "2025-06-30")

    for i in range(1, n_customers + 1):
        country = str(rng.choice(countries, p=country_weights))
        city = str(rng.choice(COUNTRY_CITIES[country]))
        for _ in range(100):
            name = f"{rng.choice(COMPANY_PREFIXES)} {rng.choice(COMPANY_SUFFIXES)} {i:05d}"
            if name not in used_names:
                used_names.add(name)
                break
        customer_type = str(rng.choice(CUSTOMER_TYPES, p=[0.34, 0.24, 0.18, 0.16, 0.08]))
        rows.append(
            {
                "customer_id": i,
                "company_name": name,
                "country": country,
                "city": city,
                "customer_type": customer_type,
                "registration_date": registration_dates.iloc[i - 1].date().isoformat(),
                "phone": random_phone(rng),
            }
        )
    return pd.DataFrame(rows)


def generate_categories(n_categories: int) -> pd.DataFrame:
    names = CATEGORY_NAMES[:n_categories]
    return pd.DataFrame(
        {
            "category_id": list(range(1, n_categories + 1)),
            "category_name": names,
        }
    )


def generate_products(
    rng: np.random.Generator,
    categories: pd.DataFrame,
    n_products: int,
) -> pd.DataFrame:
    rows = []
    category_names = dict(zip(categories["category_id"], categories["category_name"]))
    category_ids = categories["category_id"].to_numpy()

    for product_id in range(1, n_products + 1):
        category_id = int(rng.choice(category_ids))
        category_name = category_names[category_id]
        noun = str(rng.choice(PRODUCT_NOUNS.get(category_name, ["Product"])))
        adjective = str(rng.choice(PRODUCT_ADJECTIVES))
        product_name = f"{adjective} {noun} {product_id:03d}"

        # Category-dependent price ranges.
        base_low, base_high = {
            "Beverages": (3, 40),
            "Dairy": (4, 35),
            "Seafood": (12, 120),
            "Meat": (10, 95),
            "Bakery": (2, 30),
            "Confections": (3, 45),
            "Produce": (1, 25),
            "Grains": (2, 35),
            "Spices": (2, 50),
            "Frozen Foods": (5, 60),
            "Snacks": (2, 30),
            "Household": (3, 80),
            "Coffee & Tea": (5, 70),
            "Condiments": (2, 40),
            "Prepared Meals": (6, 75),
        }.get(category_name, (3, 50))
        price = round(float(rng.uniform(base_low, base_high)), 2)
        rows.append(
            {
                "product_id": product_id,
                "product_name": product_name,
                "category_id": category_id,
                "base_price": price,
                "is_discontinued": int(rng.random() < 0.06),
            }
        )
    return pd.DataFrame(rows)


def generate_orders(
    rng: np.random.Generator,
    customers: pd.DataFrame,
    n_orders: int,
) -> pd.DataFrame:
    # Pareto-like customer weights: a smaller group orders more frequently.
    customer_ids = customers["customer_id"].to_numpy()
    customer_scores = rng.gamma(shape=1.4, scale=1.0, size=len(customer_ids))
    type_multiplier = customers["customer_type"].map(
        {"retail": 0.8, "wholesale": 1.6, "horeca": 1.4, "online": 1.1, "distributor": 2.0}
    ).to_numpy()
    weights = customer_scores * type_multiplier
    weights = weights / weights.sum()

    order_customer_ids = rng.choice(customer_ids, size=n_orders, replace=True, p=weights)
    order_dates = weighted_dates(rng, n_orders)

    cust_lookup = customers.set_index("customer_id")[["country", "city"]].to_dict("index")
    rows = []
    for i, (customer_id, order_date) in enumerate(zip(order_customer_ids, order_dates), start=100001):
        customer_id = int(customer_id)
        required_date = order_date + pd.Timedelta(days=int(rng.integers(3, 14)))
        if rng.random() < 0.08:
            shipped_date = pd.NaT
        else:
            shipped_date = order_date + pd.Timedelta(days=int(rng.integers(1, 12)))
        ship_country = cust_lookup[customer_id]["country"]
        ship_city = cust_lookup[customer_id]["city"]
        shipping_cost = round(float(rng.gamma(shape=2.2, scale=7.0) + 3), 2)
        rows.append(
            {
                "order_id": i,
                "customer_id": customer_id,
                "order_date": order_date.date().isoformat(),
                "required_date": required_date.date().isoformat(),
                "shipped_date": "" if pd.isna(shipped_date) else shipped_date.date().isoformat(),
                "ship_country": ship_country,
                "ship_city": ship_city,
                "shipping_cost": shipping_cost,
            }
        )
    return pd.DataFrame(rows)


def generate_order_items(
    rng: np.random.Generator,
    orders: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    product_ids = products["product_id"].to_numpy()
    # Popularity weights by product.
    product_popularity = rng.lognormal(mean=0.0, sigma=0.8, size=len(product_ids))
    product_popularity = product_popularity / product_popularity.sum()
    price_lookup = products.set_index("product_id")["base_price"].to_dict()

    rows = []
    for order_id in orders["order_id"]:
        n_items = int(np.clip(rng.poisson(lam=2.4) + 1, 1, 8))
        chosen_products = rng.choice(product_ids, size=n_items, replace=False, p=product_popularity)
        for line_no, product_id in enumerate(chosen_products, start=1):
            base_price = float(price_lookup[int(product_id)])
            unit_price = round(max(0.5, base_price * float(rng.normal(1.0, 0.08))), 2)
            quantity = int(np.clip(rng.negative_binomial(n=3, p=0.48) + 1, 1, 50))
            discount = float(rng.choice([0, 0.03, 0.05, 0.10, 0.15, 0.20], p=[0.57, 0.08, 0.15, 0.12, 0.06, 0.02]))
            rows.append(
                {
                    "order_id": int(order_id),
                    "line_no": line_no,
                    "product_id": int(product_id),
                    "unit_price": unit_price,
                    "quantity": quantity,
                    "discount": discount,
                }
            )
    return pd.DataFrame(rows)


def make_fact_sales(
    customers: pd.DataFrame,
    categories: pd.DataFrame,
    products: pd.DataFrame,
    orders: pd.DataFrame,
    order_items: pd.DataFrame,
) -> pd.DataFrame:
    fact = (
        order_items.merge(orders, on="order_id", how="left")
        .merge(customers[["customer_id", "company_name", "country", "city", "customer_type"]], on="customer_id", how="left")
        .merge(products, on="product_id", how="left")
        .merge(categories, on="category_id", how="left")
    )
    fact["line_value"] = (fact["unit_price"] * fact["quantity"] * (1 - fact["discount"])).round(2)
    fact["order_month"] = pd.to_datetime(fact["order_date"]).dt.to_period("M").astype(str)
    columns = [
        "order_id",
        "line_no",
        "customer_id",
        "company_name",
        "order_date",
        "order_month",
        "country",
        "city",
        "customer_type",
        "product_id",
        "product_name",
        "category_id",
        "category_name",
        "quantity",
        "unit_price",
        "discount",
        "line_value",
        "shipping_cost",
    ]
    return fact[columns]


def dirty_country(rng: np.random.Generator, country: str) -> str:
    if pd.isna(country):
        return country
    mapping = {
        "USA": ["USA", "US", "United States", "usa", "U.S.A."],
        "United Kingdom": ["United Kingdom", "UK", "Great Britain", "uk"],
        "Poland": ["Poland", "poland", "PL", "Polska"],
        "Germany": ["Germany", "DE", "Deutschland", "germany"],
        "France": ["France", "FR", "france"],
    }
    if country in mapping and rng.random() < 0.65:
        return str(rng.choice(mapping[country]))
    if rng.random() < 0.12:
        return str(country).lower()
    return country


def random_date_format(rng: np.random.Generator, date_value: str) -> str:
    if date_value == "" or pd.isna(date_value):
        return ""
    dt = pd.to_datetime(date_value)
    fmt = str(rng.choice(["iso", "slash_dmy", "month_name", "dot_dmy", "us_mdy"], p=[0.45, 0.18, 0.12, 0.12, 0.13]))
    if fmt == "iso":
        return dt.strftime("%Y-%m-%d")
    if fmt == "slash_dmy":
        return dt.strftime("%d/%m/%Y")
    if fmt == "month_name":
        return dt.strftime("%b %d, %Y")
    if fmt == "dot_dmy":
        return dt.strftime("%d.%m.%Y")
    return dt.strftime("%m/%d/%Y")


def make_customers_dirty(rng: np.random.Generator, customers: pd.DataFrame) -> pd.DataFrame:
    dirty = customers.copy()
    dirty["country"] = [dirty_country(rng, c) for c in dirty["country"]]
    dirty["registration_date"] = [random_date_format(rng, d) for d in dirty["registration_date"]]

    # Missing values.
    country_missing = rng.choice(dirty.index, size=max(1, int(0.04 * len(dirty))), replace=False)
    phone_missing = rng.choice(dirty.index, size=max(1, int(0.08 * len(dirty))), replace=False)
    dirty.loc[country_missing, "country"] = ""
    dirty.loc[phone_missing, "phone"] = ""

    # Add duplicate companies with new IDs and slightly altered fields.
    n_duplicates = max(5, int(0.03 * len(dirty)))
    duplicate_rows = dirty.sample(n=n_duplicates, random_state=int(rng.integers(0, 1_000_000))).copy()
    duplicate_rows["customer_id"] = range(int(dirty["customer_id"].max()) + 1, int(dirty["customer_id"].max()) + 1 + n_duplicates)
    duplicate_rows.loc[duplicate_rows.index[: max(1, n_duplicates // 3)], "phone"] = ""
    duplicate_rows["company_name"] = duplicate_rows["company_name"].str.replace("  ", " ", regex=False)
    dirty = pd.concat([dirty, duplicate_rows], ignore_index=True)

    # A few leading/trailing spaces for string-cleaning practice.
    sample_idx = rng.choice(dirty.index, size=max(1, int(0.05 * len(dirty))), replace=False)
    dirty.loc[sample_idx, "company_name"] = " " + dirty.loc[sample_idx, "company_name"].astype(str) + " "
    return dirty


def make_orders_dirty(rng: np.random.Generator, orders: pd.DataFrame) -> pd.DataFrame:
    dirty = orders.copy()
    for col in ["order_date", "required_date", "shipped_date"]:
        dirty[col] = [random_date_format(rng, d) for d in dirty[col]]

    # Missing shipped dates.
    ship_missing = rng.choice(dirty.index, size=max(1, int(0.07 * len(dirty))), replace=False)
    dirty.loc[ship_missing, "shipped_date"] = ""

    # A few impossible or suspicious dates.
    suspicious = rng.choice(dirty.index, size=max(1, int(0.005 * len(dirty))), replace=False)
    dirty.loc[suspicious[: len(suspicious) // 2], "order_date"] = "2099-01-01"
    dirty.loc[suspicious[len(suspicious) // 2 :], "order_date"] = "1900-01-01"

    # A few invalid shipping costs.
    cost_bad = rng.choice(dirty.index, size=max(1, int(0.01 * len(dirty))), replace=False)
    dirty.loc[cost_bad, "shipping_cost"] = -dirty.loc[cost_bad, "shipping_cost"].abs()

    # Duplicate some orders to practice duplicate checks.
    n_duplicates = max(5, int(0.01 * len(dirty)))
    duplicates = dirty.sample(n=n_duplicates, random_state=int(rng.integers(0, 1_000_000))).copy()
    dirty = pd.concat([dirty, duplicates], ignore_index=True)
    return dirty


def generate_dataset(output_dir: Path, size_name: str, spec: Dict[str, int]) -> None:
    rng = np.random.default_rng(SEED + spec["customers"] + spec["orders"])
    random.seed(SEED)
    output_dir.mkdir(parents=True, exist_ok=True)

    categories = generate_categories(spec["categories"])
    customers = generate_customers(rng, spec["customers"])
    products = generate_products(rng, categories, spec["products"])
    orders = generate_orders(rng, customers, spec["orders"])
    order_items = generate_order_items(rng, orders, products)
    fact_sales = make_fact_sales(customers, categories, products, orders, order_items)
    customers_dirty = make_customers_dirty(rng, customers)
    orders_dirty = make_orders_dirty(rng, orders.sample(n=min(len(orders), 10000), random_state=SEED).sort_values("order_id"))

    # Deterministic ordering.
    customers = customers.sort_values("customer_id")
    products = products.sort_values("product_id")
    orders = orders.sort_values("order_id")
    order_items = order_items.sort_values(["order_id", "line_no"])
    fact_sales = fact_sales.sort_values(["order_date", "order_id", "line_no"])

    tables = {
        "categories": categories,
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
        "fact_sales": fact_sales,
        "customers_dirty": customers_dirty,
        "orders_dirty": orders_dirty,
    }
    for name, df in tables.items():
        df.to_csv(output_dir / f"{name}.csv", index=False)

    summary = pd.DataFrame(
        [
            {"table_name": name, "rows": len(df), "columns": len(df.columns)}
            for name, df in tables.items()
        ]
    )
    summary.to_csv(output_dir / "_summary.csv", index=False)
    print(f"Generated {size_name} dataset in {output_dir}")
    print(summary.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data"))
    args = parser.parse_args()

    specs = {
        "small": {"customers": 500, "products": 120, "categories": 12, "orders": 10_000},
        "medium": {"customers": 3_000, "products": 250, "categories": 15, "orders": 30_000},
    }
    for size_name, spec in specs.items():
        generate_dataset(args.output / size_name, size_name, spec)


if __name__ == "__main__":
    main()
