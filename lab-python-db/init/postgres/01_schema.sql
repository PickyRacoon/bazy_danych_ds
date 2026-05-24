CREATE SCHEMA IF NOT EXISTS retail;
SET search_path TO retail;

DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS customers_dirty CASCADE;
DROP TABLE IF EXISTS orders_dirty CASCADE;
DROP TABLE IF EXISTS fact_sales CASCADE;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    country TEXT,
    city TEXT,
    customer_type TEXT,
    registration_date DATE,
    phone TEXT
);

CREATE TABLE categories (
    category_id INTEGER PRIMARY KEY,
    category_name TEXT NOT NULL
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(category_id),
    base_price NUMERIC(12, 2),
    is_discontinued BOOLEAN
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    required_date DATE,
    shipped_date DATE,
    ship_country TEXT,
    ship_city TEXT,
    shipping_cost NUMERIC(12, 2)
);

CREATE TABLE order_items (
    order_id INTEGER NOT NULL REFERENCES orders(order_id),
    line_no INTEGER NOT NULL,
    product_id INTEGER NOT NULL REFERENCES products(product_id),
    unit_price NUMERIC(12, 2) NOT NULL,
    quantity INTEGER NOT NULL,
    discount NUMERIC(5, 2) NOT NULL,
    PRIMARY KEY (order_id, line_no)
);

-- Dirty tables are intentionally loose: their purpose is cleaning in pandas.
CREATE TABLE customers_dirty (
    customer_id INTEGER,
    company_name TEXT,
    country TEXT,
    city TEXT,
    customer_type TEXT,
    registration_date TEXT,
    phone TEXT
);

CREATE TABLE orders_dirty (
    order_id INTEGER,
    customer_id INTEGER,
    order_date TEXT,
    required_date TEXT,
    shipped_date TEXT,
    ship_country TEXT,
    ship_city TEXT,
    shipping_cost NUMERIC(12, 2)
);

-- A denormalized fact table for analytical queries in PostgreSQL as well.
CREATE TABLE fact_sales (
    order_id INTEGER,
    line_no INTEGER,
    customer_id INTEGER,
    company_name TEXT,
    order_date DATE,
    order_month TEXT,
    country TEXT,
    city TEXT,
    customer_type TEXT,
    product_id INTEGER,
    product_name TEXT,
    category_id INTEGER,
    category_name TEXT,
    quantity INTEGER,
    unit_price NUMERIC(12, 2),
    discount NUMERIC(5, 2),
    line_value NUMERIC(14, 2),
    shipping_cost NUMERIC(12, 2)
);
