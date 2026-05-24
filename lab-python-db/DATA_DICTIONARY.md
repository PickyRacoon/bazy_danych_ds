# Słownik danych

## `customers`

| Kolumna | Typ logiczny | Opis |
|---|---|---|
| `customer_id` | integer | identyfikator klienta |
| `company_name` | text | nazwa klienta / firmy |
| `country` | text | kraj klienta |
| `city` | text | miasto klienta |
| `customer_type` | text | typ klienta: retail, wholesale, horeca, online, distributor |
| `registration_date` | date | data rejestracji klienta |
| `phone` | text | telefon |

## `categories`

| Kolumna | Typ logiczny | Opis |
|---|---|---|
| `category_id` | integer | identyfikator kategorii |
| `category_name` | text | nazwa kategorii |

## `products`

| Kolumna | Typ logiczny | Opis |
|---|---|---|
| `product_id` | integer | identyfikator produktu |
| `product_name` | text | nazwa produktu |
| `category_id` | integer | identyfikator kategorii |
| `base_price` | numeric | cena bazowa |
| `is_discontinued` | boolean/integer | czy produkt jest wycofany |

## `orders`

| Kolumna | Typ logiczny | Opis |
|---|---|---|
| `order_id` | integer | identyfikator zamówienia |
| `customer_id` | integer | identyfikator klienta |
| `order_date` | date | data zamówienia |
| `required_date` | date | oczekiwana data realizacji |
| `shipped_date` | date/null | data wysyłki; część rekordów ma brak |
| `ship_country` | text | kraj dostawy |
| `ship_city` | text | miasto dostawy |
| `shipping_cost` | numeric | koszt dostawy |

## `order_items`

Jeden wiersz oznacza jedną pozycję zamówienia. To główna tabela długa do ćwiczeń long → wide.

| Kolumna | Typ logiczny | Opis |
|---|---|---|
| `order_id` | integer | identyfikator zamówienia |
| `line_no` | integer | numer pozycji w zamówieniu |
| `product_id` | integer | identyfikator produktu |
| `unit_price` | numeric | cena jednostkowa w pozycji |
| `quantity` | integer | liczba sztuk |
| `discount` | numeric | rabat, np. 0.10 oznacza 10% |

Typowa wartość pozycji:

```text
line_value = unit_price * quantity * (1 - discount)
```

## `fact_sales`

Zdenormalizowana tabela faktów, jeden wiersz = jedna pozycja zamówienia z dołączonym klientem, produktem i kategorią.

| Kolumna | Opis |
|---|---|
| `order_id`, `line_no` | identyfikacja pozycji zamówienia |
| `customer_id`, `company_name`, `country`, `city`, `customer_type` | dane klienta |
| `order_date`, `order_month` | czas zamówienia |
| `product_id`, `product_name`, `category_id`, `category_name` | dane produktu |
| `quantity`, `unit_price`, `discount` | dane pozycji |
| `line_value` | gotowa wartość pozycji po rabacie |
| `shipping_cost` | koszt dostawy przypisany do zamówienia |

## `customers_dirty`

Celowo zabrudzona wersja tabeli klientów. Problemy:

- brakujące wartości w `country` i `phone`,
- niespójne nazwy krajów, np. `USA`, `US`, `United States`, `usa`,
- duplikaty firm po `company_name`,
- odstępy w nazwach,
- daty rejestracji w różnych formatach.

## `orders_dirty`

Celowo zabrudzona wersja tabeli zamówień. Problemy:

- daty w różnych formatach,
- braki w `shipped_date`,
- podejrzane daty, np. 1900 albo 2099,
- ujemne koszty dostawy,
- duplikaty zamówień.
