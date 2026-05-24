SET search_path TO retail;

COPY categories FROM '/data/medium/categories.csv' WITH (FORMAT csv, HEADER true, NULL '');
COPY customers FROM '/data/medium/customers.csv' WITH (FORMAT csv, HEADER true, NULL '');
COPY products FROM '/data/medium/products.csv' WITH (FORMAT csv, HEADER true, NULL '');
COPY orders FROM '/data/medium/orders.csv' WITH (FORMAT csv, HEADER true, NULL '');
COPY order_items FROM '/data/medium/order_items.csv' WITH (FORMAT csv, HEADER true, NULL '');
COPY customers_dirty FROM '/data/medium/customers_dirty.csv' WITH (FORMAT csv, HEADER true, NULL '');
COPY orders_dirty FROM '/data/medium/orders_dirty.csv' WITH (FORMAT csv, HEADER true, NULL '');
COPY fact_sales FROM '/data/medium/fact_sales.csv' WITH (FORMAT csv, HEADER true, NULL '');

CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_orders_order_date ON orders(order_date);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_fact_sales_date_country_category ON fact_sales(order_date, country, category_name);
CREATE INDEX idx_fact_sales_customer_id ON fact_sales(customer_id);

ANALYZE;
