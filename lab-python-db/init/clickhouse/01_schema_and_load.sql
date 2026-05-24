CREATE DATABASE IF NOT EXISTS retail;

DROP TABLE IF EXISTS retail.fact_sales;

CREATE TABLE retail.fact_sales
(
    order_id UInt32,
    line_no UInt8,
    customer_id UInt32,
    company_name String,
    order_date Date,
    order_month String,
    country LowCardinality(String),
    city LowCardinality(String),
    customer_type LowCardinality(String),
    product_id UInt32,
    product_name String,
    category_id UInt16,
    category_name LowCardinality(String),
    quantity UInt16,
    unit_price Float64,
    discount Float64,
    line_value Float64,
    shipping_cost Float64
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(order_date)
ORDER BY (order_date, country, category_name, customer_id, product_id);

INSERT INTO retail.fact_sales
SELECT *
FROM file(
    'data/medium/fact_sales.csv',
    'CSVWithNames',
    'order_id UInt32, line_no UInt8, customer_id UInt32, company_name String, order_date Date, order_month String, country String, city String, customer_type String, product_id UInt32, product_name String, category_id UInt16, category_name String, quantity UInt16, unit_price Float64, discount Float64, line_value Float64, shipping_cost Float64'
);
