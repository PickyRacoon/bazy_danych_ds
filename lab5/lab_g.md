### 1. Pierwsze poznanie tabeli events 

- PostgreSQL

```sql
select column_name, data_type, is_nullable, column_default
from information_schema.columns
where table_name = 'events';
```

![zdj2](./_img/1_p_opis.png)


```sql
select * from events limit 10;
```

![zdj2](./_img/1_p_limit.png)


```sql
SELECT
    count(*) AS n,
    min(event_time) AS min_time,
    max(event_time) AS max_time
FROM events;
```

![zdj2](./_img/1_p_min.png)


```sql
SELECT
    count(*) AS all_rows,
    count(price) AS non_null_price,
    count(quantity) AS non_null_quantity,
    count(*) - count(price) AS null_price_rows,
    count(*) - count(quantity) AS null_quantity_rows
FROM events;
```

![zdj2](./_img/1_p_null.png)

- ClickHouse

Te same zapytania zostały użyte dla ClickHouse.

![zdj2](./_img/1_ch_opis.png)

![zdj2](./_img/1_ch_limit.png)

![zdj2](./_img/1_ch_min.png)

![zdj2](./_img/1_ch_null.png)

### 3. Aktywność w czasie

- PostgreSQL


- ClickHouse


### 5. KPI w przekrojach biznesowych

- PostgreSQL


- ClickHouse

### 7. Benchmark zapytań w PostgreSQL i ClickHouse

- A
  
  
  - B


- C

| Zapytanie | Koszt    | Czas (ms) | Odczytane strony  |
| :-------- | :------- | :-------- | :---------------- |
| 3        | 19.659   | 67      |       25837       |
| 4         | 21.2591  | 9       |          70     |
