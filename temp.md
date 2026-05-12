
**1. Pierwsze poznanie Couchbase i danych -- 1 pkt**

**Cel**

Poznaj podstawową strukturę danych w Couchbase i sprawdź, jakie kolekcje
są dostępne.

**Wykonaj**

1.  W panelu Couchbase za pomocą zakładek w menu bocznym np. 'Buckets',
    'Documents', 'Query' zbadaj strukturę:

```sql
bucket → scope → collection
```

bucket - odpowiednik bazy danych w SQL

scope - odpowiednik schematu w SQL

collection - odpowiednik tabeli w SQL

2. W Query Workbench policz liczbę dokumentów w kolekcjach:

- orders,

- orderdetails,

- customers,

- products,

- orders_nested.

| Kolekcja      | Liczba dokumentów |
|----------------|------------------|
| orders         | 830               |
| orderdetails   | 2155              |
| customers      | 91                |
| products       | 77                |
| orders_nested  | 830               |

```sql
  SELECT COUNT(1) AS orders_count
  FROM `north0`._default.orders
  WHERE OrderID IS NOT MISSING;
```

```sql
 SELECT COUNT(1) AS orderdetails_count
  FROM `north0`._default.orderdetails
  WHERE OrderID IS NOT MISSING;
```

```sql
  SELECT COUNT(1) AS customers_count
  FROM `north0`._default.customers
  WHERE CustomerID IS NOT MISSING;
```

```sql
  CREATE INDEX idx_products_productid
  ON `north0`._default.products(ProductID);
```

```sql
  SELECT COUNT(1) AS products_count
  FROM `north0`._default.products
  WHERE ProductID IS NOT MISSING;
```

```sql
  SELECT COUNT(1) AS orders_nested_count
  FROM `north0`._default.orders_nested
  WHERE OrderID IS NOT MISSING;
```
  
3. Podejrzyj kilka dokumentów z kolekcji orders.

```sql
  SELECT o
  FROM `north0`._default.orders AS o
  WHERE o.OrderID IS NOT MISSING
  LIMIT 3;
```

```json
 [
  {
    "o": {
      "CustomerID": "VINET",
      "EmployeeID": 5,
      "Freight": 32.38,
      "OrderDate": {
        "$date": "1996-07-04T00:00:00Z"
      },
      "OrderID": 10248,
      "RequiredDate": {
        "$date": "1996-08-01T00:00:00Z"
      },
      "ShipAddress": "59 rue de l'Abbaye",
      "ShipCity": "Reims",
      "ShipCountry": "France",
      "ShipName": "Vins et alcools Chevalier",
      "ShipPostalCode": "51100",
      "ShipRegion": null,
      "ShipVia": 3,
      "ShippedDate": {
        "$date": "1996-07-16T00:00:00Z"
      },
      "_id": {
        "$oid": "63a060b9bb3b972d6f4e1fc6"
      }
    }
  },
  {
    "o": {
      "CustomerID": "TOMSP",
      "EmployeeID": 6,
      "Freight": 11.61,
      "OrderDate": {
        "$date": "1996-07-05T00:00:00Z"
      },
      "OrderID": 10249,
      "RequiredDate": {
        "$date": "1996-08-16T00:00:00Z"
      },
      "ShipAddress": "Luisenstr. 48",
      "ShipCity": "Münster",
      "ShipCountry": "Germany",
      "ShipName": "Toms Spezialitäten",
      "ShipPostalCode": "44087",
      "ShipRegion": null,
      "ShipVia": 1,
      "ShippedDate": {
        "$date": "1996-07-10T00:00:00Z"
      },
      "_id": {
        "$oid": "63a060b9bb3b972d6f4e1fc7"
      }
    }
  },
  {
    "o": {
      "CustomerID": "HANAR",
      "EmployeeID": 4,
      "Freight": 65.83,
      "OrderDate": {
        "$date": "1996-07-08T00:00:00Z"
      },
      "OrderID": 10250,
      "RequiredDate": {
        "$date": "1996-08-05T00:00:00Z"
      },
      "ShipAddress": "Rua do Paço, 67",
      "ShipCity": "Rio de Janeiro",
      "ShipCountry": "Brazil",
      "ShipName": "Hanari Carnes",
      "ShipPostalCode": "05454-876",
      "ShipRegion": "RJ",
      "ShipVia": 2,
      "ShippedDate": {
        "$date": "1996-07-12T00:00:00Z"
      },
      "_id": {
        "$oid": "63a060b9bb3b972d6f4e1fc8"
      }
    }
  }
]
```

4. Podejrzyj jeden dokument z kolekcji orders_nested.

```sql
  SELECT o
  FROM `north0`._default.orders_nested AS o
  WHERE o.OrderID IS NOT MISSING
  LIMIT 3;
```

```json
[
  {
    "o": {
      "CustomerID": "VINET",
      "EmployeeID": 5,
      "OrderDate": {
        "$date": "1996-07-04T00:00:00Z"
      },
      "OrderID": 10248,
      "ShipCity": "Reims",
      "ShipCountry": "France",
      "ShipName": "Vins et alcools Chevalier",
      "items": [
        {
          "Discount": 0,
          "LineValue": 98,
          "ProductID": 42,
          "Quantity": 10,
          "UnitPrice": 9.8
        },
        {
          "Discount": 0,
          "LineValue": 168,
          "ProductID": 11,
          "Quantity": 12,
          "UnitPrice": 14
        },
        {
          "Discount": 0,
          "LineValue": 174,
          "ProductID": 72,
          "Quantity": 5,
          "UnitPrice": 34.8
        }
      ],
      "type": "order_nested"
    }
  },
  {
    "o": {
      "CustomerID": "TOMSP",
      "EmployeeID": 6,
      "OrderDate": {
        "$date": "1996-07-05T00:00:00Z"
      },
      "OrderID": 10249,
      "ShipCity": "Münster",
      "ShipCountry": "Germany",
      "ShipName": "Toms Spezialitäten",
      "items": [
        {
          "Discount": 0,
          "LineValue": 167.4,
          "ProductID": 14,
          "Quantity": 9,
          "UnitPrice": 18.6
        },
        {
          "Discount": 0,
          "LineValue": 1696,
          "ProductID": 51,
          "Quantity": 40,
          "UnitPrice": 42.4
        }
      ],
      "type": "order_nested"
    }
  },
  {
    "o": {
      "CustomerID": "HANAR",
      "EmployeeID": 4,
      "OrderDate": {
        "$date": "1996-07-08T00:00:00Z"
      },
      "OrderID": 10250,
      "ShipCity": "Rio de Janeiro",
      "ShipCountry": "Brazil",
      "ShipName": "Hanari Carnes",
      "items": [
        {
          "Discount": 0,
          "LineValue": 77,
          "ProductID": 41,
          "Quantity": 10,
          "UnitPrice": 7.7
        },
        {
          "Discount": 0.15000000596046448,
          "LineValue": 214.19999849796295,
          "ProductID": 65,
          "Quantity": 15,
          "UnitPrice": 16.8
        },
        {
          "Discount": 0.15000000596046448,
          "LineValue": 1261.3999911546707,
          "ProductID": 51,
          "Quantity": 35,
          "UnitPrice": 42.4
        }
      ],
      "type": "order_nested"
    }
  }
]
```



**Wskazówki**

Przykład zapytania liczącego dokumenty:


```sql
  SELECT COUNT(1) AS orders_count
  FROM `north0`._default.orders
  WHERE OrderID IS NOT MISSING;
```

Przykład podejrzenia dokumentu:

```sql
  SELECT o
  FROM `north0`._default.orders AS o
  WHERE o.OrderID IS NOT MISSING
  LIMIT 3;
```

**W komentarzu napisz**

- Co oznaczają pojęcia bucket, scope i collection?

- Ile dokumentów znajduje się w kolekcjach orders, orderdetails,
  customers, products i orders_nested?

- Czym różni się dokument z kolekcji orders od dokumentu z kolekcji
  orders_nested?

---

**3.** JOIN **na kolekcjach dokumentów -- 2 pkt**

**Cel**

Zobacz, że Couchbase pozwala wykonywać JOIN podobny do SQL, ale pracuje
na dokumentach JSON i kolekcjach, a nie na klasycznych tabelach
relacyjnych.

**Część A -- zamówienia z nazwą klienta**

Dla zamówień pokaż:

- OrderID,

- OrderDate,

- CustomerID,

- CompanyName.

Przed wykonaniem zapytania utwórz indeks potrzebny do łączenia z
kolekcją customers:

```sql
  CREATE INDEX idx_customers_customerid
  ON `north0`._default.customers(CustomerID);
```

Jeżeli indeks już istnieje, Couchbase zwróci komunikat o istniejącym
indeksie. W takiej sytuacji przejdź do kolejnego kroku.

Następnie przygotuj zapytanie łączące orders z customers.

```sql
  SELECT 
    o.OrderID,
    o.OrderDate,
    o.CustomerID,
    c.CompanyName
FROM `north0`._default.orders AS o
JOIN `north0`._default.customers AS c
ON o.CustomerID = c.CustomerID;
```

![zdj2](./_img/3_a.png)

**Część B -- zamówienia i pozycje zamówień**

Dla pozycji zamówień pokaż:

- OrderID,

- CustomerID,

- ProductID,

- UnitPrice,

- Quantity,

- Discount.

Wykorzystaj kolekcje:

- orders,

- orderdetails.

**Uwaga:** indeksy idx_orders_orderid oraz idx_orderdetails_orderid
zostały utworzone automatycznie podczas inicjalizacji środowiska. Nie
trzeba ich zakładać ręcznie. Jeżeli mimo to spróbujesz je utworzyć,
Couchbase poinformuje, że indeks już istnieje -- to nie jest błąd.

```sql
  SELECT
    o.OrderID,
    o.CustomerID,
    od.ProductID,
    od.UnitPrice,
    od.Quantity,
    od.Discount
FROM `north0`._default.orders AS o
JOIN `north0`._default.orderdetails AS od
ON o.OrderID = od.OrderID;
```

**Część C -- wartość zamówienia**

Policz wartość zamówienia według wzoru:


```sql
  wartość pozycji = UnitPrice * Quantity * (1 - Discount)
```

Brak rabatu traktuj jako 0.

**Wskazówka:** w dokumentach JSON pole Discount może nie istnieć albo
mieć wartość null. W Couchbase do obsługi takich sytuacji służy funkcja
IFMISSINGORNULL(od.Discount, 0), która zwraca 0, jeżeli pole nie
istnieje lub jest puste.

Dla każdego zamówienia oblicz:

- OrderID,

- CustomerID,

- order_value,

- liczbę pozycji zamówienia.

Pokaż 10 zamówień o najwyższej wartości.


```sql
  SELECT
    o.OrderID,
    o.CustomerID,
    SUM(
        od.UnitPrice * od.Quantity *
        (1 - IFMISSINGORNULL(od.Discount, 0))
    ) AS order_value,
    COUNT(1) AS items_count
FROM `north0`._default.orders AS o
JOIN `north0`._default.orderdetails AS od
ON o.OrderID = od.OrderID
GROUP BY o.OrderID, o.CustomerID
ORDER BY order_value DESC
LIMIT 10;
```

![zdj2](./_img/3_c.png)

**W komentarzu napisz**

- Czy JOIN w Couchbase przypomina składnię znaną z SQL?

- Czym różni się takie łączenie od relacji w klasycznej bazie relacyjnej
  (np. czy baza wymusza klucze obce i spójność relacji tak jak w typowym
  modelu relacyjnym)?

- Dlaczego indeks po stronie dołączanej kolekcji jest ważny?

- Czy największe zamówienia mają zawsze największą liczbę pozycji?

  ---

**5. Agregacja biznesowa -- 1 pkt**

**Cel**

Wykonaj prostą analizę biznesową na danych dokumentowych.

**Wybierz [jeden]{.underline} wariant**

Do zaliczenia zadania wybierz jeden wariant. Jeżeli skończysz wcześniej,
wykonaj drugi wariant jako ćwiczenie dodatkowe.

**Wariant A -- top 10 produktów po wartości sprzedaży**

Dla produktów policz:

- ProductID,

- ProductName,

- łączną liczbę sprzedanych sztuk,

- łączną wartość sprzedaży.

Wykorzystaj kolekcje:

- orderdetails,

- products.

Przed zapytaniem może być potrzebny indeks:


```sql
 CREATE INDEX idx_products_productid
  ON `north0`._default.products(ProductID);
  CREATE INDEX idx_orderdetails_productid
  ON `north0`._default.orderdetails(ProductID);
```

Jeżeli indeks już istnieje, Couchbase zwróci komunikat o istniejącym
indeksie --- to nie jest błąd.


```sql
 SELECT
    p.ProductID,
    p.ProductName,
    SUM(od.Quantity) AS total_quantity_sold,
    SUM(
        od.UnitPrice * od.Quantity *
        (1 - IFMISSINGORNULL(od.Discount, 0))
    ) AS total_sales_value
FROM `north0`._default.products AS p
JOIN `north0`._default.orderdetails AS od
ON p.ProductID = od.ProductID
GROUP BY p.ProductID, p.ProductName
ORDER BY total_sales_value DESC;
```

![zdj2](./_img/5_a.png)

**W komentarzu napisz**

- Który produkt albo klient ma najwyższą wartość sprzedaży?

- Czy wynik jest łatwy do biznesowej interpretacji?

- Czy zapytanie bardziej przypomina klasyczny SQL/BI, czy pracę z
  dokumentami JSON?

