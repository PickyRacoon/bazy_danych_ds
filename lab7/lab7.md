# Laboratorium - dokumentowe bazy danych: Couchbase

**Temat:** Couchbase, dokumenty JSON, indeksy, JOIN, UNNEST i analiza danych Northwind

**Baza:** Couchbase Community uruchomiony w Dockerze

**Bucket:** north0

**Scope:** \_default

**Główne kolekcje:** orders, orderdetails, customers, products, orders_nested

**Imię i nazwisko:** Patrycja Markiewicz, Karolina Węgrzyn

**Grupa:** 1

---

## Cel ćwiczenia

Po wykonaniu laboratorium student powinien umieć:

1. uruchomić i zweryfikować środowisko Couchbase,
2. poruszać się po panelu Couchbase i korzystać z Query Workbench,
3. rozumieć strukturę bucket → scope → collection,
4. wykonać podstawowe zapytania SQL++ / N1QL na dokumentach JSON,
5. wyjaśnić, dlaczego Couchbase wymaga indeksów do wykonywania zapytań,
6. odróżnić primary index od indeksu celowego,
7. wykonać JOIN między kolekcjami dokumentów,
8. porównać model niezagnieżdżony z modelem zagnieżdżonym,
9. użyć UNNEST do rozbijania tablicy zagnieżdżonej w dokumencie,
10. wykorzystać EXPLAIN do podstawowej interpretacji planu zapytania.

## Ważne informacje

W tym laboratorium pracujemy na danych Northwind załadowanych do Couchbase.

Dane są dostępne w dwóch wariantach modelowania:

### Model niezagnieżdżony

Dane są podzielone na osobne kolekcje:

- orders -- zamówienia,
- orderdetails -- pozycje zamówień,
- customers -- klienci,
- products -- produkty.

W tym wariancie, aby połączyć zamówienia z pozycjami zamówień, używamy JOIN.

### Model zagnieżdżony

Dodatkowo przygotowana jest kolekcja:

- orders_nested.

W tej kolekcji jeden dokument odpowiada jednemu zamówieniu, a pozycje zamówienia są zapisane wewnątrz dokumentu w tablicy items. W tym wariancie do rozbicia pozycji zamówienia używamy UNNEST.

### Jak korzystać ze ściągi

Do laboratorium dołączona jest ściąga Couchbase_SQLPP_sciaga.md. Korzystaj z niej jak z dokumentacji pomocniczej: sprawdzaj składnię JOIN, UNNEST, IFMISSINGORNULL, CREATE INDEX i EXPLAIN, ale nie kopiuj bezrefleksyjnie gotowych rozwiązań. Oceniane są również komentarze i interpretacja.

### Sprawozdanie

Oddawane sprawozdanie powinno zawierać:

- kod zapytań,
- wyniki zapytań jako tabele albo zrzuty ekranu,
- krótkie komentarze interpretacyjne,
- odpowiedzi na pytania wskazane w zadaniach.

**Format sprawozdania:** PDF albo Markdown.

**Kod SQL++ / N1QL formatuj jako bloki kodu.**

**Nie oddawaj samych zrzutów ekranu bez komentarza.**

### Punktacja

| Zadanie   | Temat                                                 | Punkty |
| --------- | ----------------------------------------------------- | ------ |
| 0         | Gotowość środowiska                                   | 0      |
| 1         | Pierwsze poznanie Couchbase i danych                  | 1      |
| 2         | Indeksy: brak indeksu, primary index, secondary index | 2      |
| 3         | JOIN na kolekcjach dokumentów                         | 2      |
| 4         | Model niezagnieżdżony vs zagnieżdżony: JOIN vs UNNEST | 2      |
| 5         | Agregacja biznesowa                                   | 1      |
| 6         | EXPLAIN i refleksja końcowa                           | 2      |
| **Razem** |                                                       | **10** |

---

## 0. Gotowość środowiska -- 0 pkt

To zadanie nie jest punktowane, ale jest warunkiem rozpoczęcia pracy.

### Wykonaj

1. Uruchom środowisko:

```bash
docker compose --profile init up -d
```

2. Sprawdź, czy działają kontenery:

```bash
docker ps
```

3. Wejdź do panelu Couchbase:

```
http://localhost:8091
```

4. Zaloguj się:

```
Login: student
Hasło: student
```

5. Sprawdź, czy widzisz bucket:

```
north0
```

6. Wejdź do Query Workbench i uruchom:

```sql
SELECT 1 AS test;
```

### Do sprawozdania

Nie trzeba dołączać pełnych logów. Wystarczy jedno zdanie:

Środowisko Couchbase zostało uruchomione, logowanie działa, bucket north0 jest widoczny, a Query Workbench wykonuje zapytania.

---

## 2. Indeksy: brak indeksu, primary index, secondary index -- 2 pkt

### Cel

Zobacz, że Couchbase nie wykonuje zapytań bez odpowiedniego indeksu. Następnie porównaj indeks główny z indeksem celowym.

### Część A -- zapytanie bez indeksu

Wykonaj zapytanie:

```sql
SELECT
  c.Country,
  COUNT(1) AS customers_count
FROM `north0`._default.customers AS c
GROUP BY c.Country
ORDER BY customers_count DESC;
```

![img](./_img/zad2_A.png)

**Oczekiwane zachowanie**

W świeżo uruchomionym środowisku zapytanie powinno zakończyć się błędem informującym o braku indeksu. Jeżeli zapytanie działa od razu, oznacza to najczęściej, że w środowisku pozostał wcześniej utworzony indeks.

### Część B -- primary index

Utwórz primary index:

```sql
CREATE PRIMARY INDEX idx_customers_primary
ON `north0`._default.customers;
```

![img](./_img/zad2_B.png)

Powtórz zapytanie z części A.

```json
[
  {
    "Country": "USA",
    "customers_count": 13
  },
  {
    "Country": "France",
    "customers_count": 11
  },
  {
    "Country": "Germany",
    "customers_count": 11
  },
  {
    "Country": "Brazil",
    "customers_count": 9
  },
  {
    "Country": "UK",
    "customers_count": 7
  },
  {
    "Country": "Spain",
    "customers_count": 5
  },
  {
    "Country": "Mexico",
    "customers_count": 5
  },
  {
    "Country": "Venezuela",
    "customers_count": 4
  },
  {
    "Country": "Argentina",
    "customers_count": 3
  },
  {
    "Country": "Canada",
    "customers_count": 3
  },
  {
    "Country": "Italy",
    "customers_count": 3
  },
  {
    "Country": "Finland",
    "customers_count": 2
  },
  {
    "Country": "Denmark",
    "customers_count": 2
  },
  {
    "Country": "Austria",
    "customers_count": 2
  },
  {
    "Country": "Portugal",
    "customers_count": 2
  },
  {
    "Country": "Sweden",
    "customers_count": 2
  },
  {
    "Country": "Belgium",
    "customers_count": 2
  },
  {
    "Country": "Switzerland",
    "customers_count": 2
  },
  {
    "Country": "Ireland",
    "customers_count": 1
  },
  {
    "Country": "Norway",
    "customers_count": 1
  },
  {
    "Country": "Poland",
    "customers_count": 1
  }
]
```

### Część C -- indeks celowy

Usuń primary index:

```sql
DROP INDEX idx_customers_primary
ON `north0`._default.customers;
```

![img](./_img/zad2_C1.png)

Utwórz indeks celowy na polu Country:

```sql
CREATE INDEX idx_customers_country
ON `north0`._default.customers(Country);
```

![img](./_img/zad2_C2.png)

Wykonaj zapytanie z warunkiem indeksowym:

```sql
SELECT
  c.Country,
  COUNT(1) AS customers_count
FROM `north0`._default.customers AS c
WHERE c.Country IS NOT MISSING
GROUP BY c.Country
ORDER BY customers_count DESC;
```

```json
[
  {
    "Country": "USA",
    "customers_count": 13
  },
  {
    "Country": "France",
    "customers_count": 11
  },
  {
    "Country": "Germany",
    "customers_count": 11
  },
  {
    "Country": "Brazil",
    "customers_count": 9
  },
  {
    "Country": "UK",
    "customers_count": 7
  },
  {
    "Country": "Spain",
    "customers_count": 5
  },
  {
    "Country": "Mexico",
    "customers_count": 5
  },
  {
    "Country": "Venezuela",
    "customers_count": 4
  },
  {
    "Country": "Argentina",
    "customers_count": 3
  },
  {
    "Country": "Canada",
    "customers_count": 3
  },
  {
    "Country": "Italy",
    "customers_count": 3
  },
  {
    "Country": "Finland",
    "customers_count": 2
  },
  {
    "Country": "Belgium",
    "customers_count": 2
  },
  {
    "Country": "Austria",
    "customers_count": 2
  },
  {
    "Country": "Portugal",
    "customers_count": 2
  },
  {
    "Country": "Sweden",
    "customers_count": 2
  },
  {
    "Country": "Denmark",
    "customers_count": 2
  },
  {
    "Country": "Switzerland",
    "customers_count": 2
  },
  {
    "Country": "Ireland",
    "customers_count": 1
  },
  {
    "Country": "Poland",
    "customers_count": 1
  },
  {
    "Country": "Norway",
    "customers_count": 1
  }
]
```

### W komentarzu napisz

**Co się stało przy próbie wykonania zapytania bez indeksu?**

Couchbase zwrócił błąd informujący o braku indeksu na kolekcji customers. Zapytanie się nie wykonało w odróżnieniu od typowej bazy relacyjnej, gdzie brak indeksu skutkuje tylko wolniejszym czasem odpowiedzi, w Couchbase planner odmawia wykonania zapytania, jeśli nie znajdzie żadnego indeksu, z którego mógłby skorzystać.

**Czym różni się primary index od indeksu celowego?**

Primary index obejmuje klucze wszystkich dokumentów w kolekcji i pozwala plannerowi obsłużyć dowolne zapytanie, ale w praktyce wymusza pełen skan kolekcji. Indeks celowy jest zbudowany na konkretnym polu i działa skutecznie tylko dla zapytań, które tego pola używają w filtrach lub grupowaniach. W zamian indeks celowy jest dużo szybszy, ponieważ planner od razu sięga do uporządkowanej struktury z wartościami pola, bez przeglądania całych dokumentów.

**Dlaczego w zapytaniu po utworzeniu indeksu celowego dodano warunek WHERE c.Country IS NOT MISSING?**

Indeks celowy obejmuje wyłącznie dokumenty, które posiadają indeksowane pole. Warunek IS NOT MISSING jest sygnałem dla plannera, że zapytanie dotyczy tylko takich dokumentów, dzięki czemu indeks może zostać użyty. Bez tego warunku planner może uznać, że indeks nie pokrywa pełnego zbioru i odmówić jego wykorzystania.

**Dlaczego w środowisku produkcyjnym nie powinno się traktować primary index jako rozwiązania docelowego?**

Ponieważ wymusza operację Primary Scan, czyli pobieranie i sprawdzanie każdego dokumentu w kolekcji przy każdym zapytaniu. W środowisku produkcyjnym, gdzie danych są tysiące lub miliony, takie podejście jest niewydajne, bardzo wolne i niepotrzebnie obciąża procesor oraz pamięć serwera.

---

## 4. Model niezagnieżdżony vs zagnieżdżony: JOIN vs UNNEST -- 2 pkt

### Cel

Porównaj dwa sposoby modelowania tych samych danych:

1. model niezagnieżdżony: orders + orderdetails,
2. model zagnieżdżony: orders_nested, gdzie pozycje zamówienia są tablicą items.

### Część A -- obejrzyj dokument zagnieżdżony

Podejrzyj dokument zamówienia o numerze 10248 z kolekcji orders_nested.

Zwróć uwagę na pole:

```
items
```

Zapytanie:

```sql
SELECT n
FROM `north0`._default.orders_nested AS n
WHERE n.OrderID = 10248;
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
  }
]
```

### Część B -- rozbij tablicę items przez UNNEST

Dla zamówienia 10248 pokaż wszystkie pozycje zamówienia z tablicy items.

Wynik powinien zawierać:

- OrderID,
- CustomerID,
- ProductID,
- UnitPrice,
- Quantity,
- Discount,
- LineValue.

**Wskazówka składniowa**

UNNEST rozbija tablicę zagnieżdżoną w dokumencie na osobne rekordy. Każdy element tablicy staje się oddzielnym wierszem w wyniku:

```sql
SELECT
  n.OrderID,
  item.ProductID
FROM `north0`._default.orders_nested AS n
UNNEST n.items AS item
WHERE n.OrderID = 10248;
```

Rozbuduj to zapytanie o pozostałe kolumny wymienione powyżej.

```sql
SELECT
  n.OrderID,
  n.CustomerID,
  item.ProductID,
  item.UnitPrice,
  item.Quantity,
  item.Discount,
  item.LineValue
FROM `north0`._default.orders_nested AS n
UNNEST n.items AS item
WHERE n.OrderID = 10248;
```

```json
[
  {
    "CustomerID": "VINET",
    "Discount": 0,
    "LineValue": 98,
    "OrderID": 10248,
    "ProductID": 42,
    "Quantity": 10,
    "UnitPrice": 9.8
  },
  {
    "CustomerID": "VINET",
    "Discount": 0,
    "LineValue": 168,
    "OrderID": 10248,
    "ProductID": 11,
    "Quantity": 12,
    "UnitPrice": 14
  },
  {
    "CustomerID": "VINET",
    "Discount": 0,
    "LineValue": 174,
    "OrderID": 10248,
    "ProductID": 72,
    "Quantity": 5,
    "UnitPrice": 34.8
  }
]
```

### Część C -- policz wartość zamówień z modelu zagnieżdżonego

Na kolekcji orders_nested policz:

- OrderID,
- CustomerID,
- order_value,
- liczbę pozycji.

Użyj UNNEST.

Pokaż 10 zamówień o najwyższej wartości.

```sql
SELECT
  n.OrderID,
  n.CustomerID,
  ROUND(SUM(item.UnitPrice * item.Quantity * (1 - IFMISSINGORNULL(item.Discount, 0))), 2) AS order_value,
  COUNT(1) AS items_count
FROM `north0`._default.orders_nested AS n
UNNEST n.items AS item
WHERE n.OrderID IS NOT MISSING
GROUP BY n.OrderID, n.CustomerID
ORDER BY order_value DESC
LIMIT 10;
```

```json
[
  {
    "CustomerID": "QUICK",
    "OrderID": 10865,
    "items_count": 2,
    "order_value": 16387.5
  },
  {
    "CustomerID": "HANAR",
    "OrderID": 10981,
    "items_count": 1,
    "order_value": 15810
  },
  {
    "CustomerID": "SAVEA",
    "OrderID": 11030,
    "items_count": 4,
    "order_value": 12615.05
  },
  {
    "CustomerID": "RATTC",
    "OrderID": 10889,
    "items_count": 2,
    "order_value": 11380
  },
  {
    "CustomerID": "SIMOB",
    "OrderID": 10417,
    "items_count": 4,
    "order_value": 11188.4
  },
  {
    "CustomerID": "KOENE",
    "OrderID": 10817,
    "items_count": 4,
    "order_value": 10952.84
  },
  {
    "CustomerID": "HUNGO",
    "OrderID": 10897,
    "items_count": 2,
    "order_value": 10835.24
  },
  {
    "CustomerID": "RATTC",
    "OrderID": 10479,
    "items_count": 4,
    "order_value": 10495.6
  },
  {
    "CustomerID": "QUICK",
    "OrderID": 10540,
    "items_count": 4,
    "order_value": 10191.7
  },
  {
    "CustomerID": "QUICK",
    "OrderID": 10691,
    "items_count": 5,
    "order_value": 10164.8
  }
]
```

### Część D -- porównaj wynik z modelem niezagnieżdżonym

Porównaj wynik z części C z wynikiem otrzymanym wcześniej przez JOIN na orders i orderdetails (zadanie 3C).

Minimum: porównaj wizualnie top 10 zamówień z obu podejść i napisz, czy wyniki są zgodne.

```sql
SELECT
  o.OrderID,
  o.CustomerID,
  ROUND(SUM(od.UnitPrice * od.Quantity * (1 - IFMISSINGORNULL(od.Discount, 0))), 2) AS order_value,
  COUNT(1) AS items_count
FROM `north0`._default.orders AS o
JOIN `north0`._default.orderdetails AS od
  ON od.OrderID = o.OrderID
WHERE o.OrderID IS NOT MISSING
GROUP BY o.OrderID, o.CustomerID
ORDER BY order_value DESC
LIMIT 10;
```

```json
[
  {
    "CustomerID": "QUICK",
    "OrderID": 10865,
    "items_count": 2,
    "order_value": 16387.5
  },
  {
    "CustomerID": "HANAR",
    "OrderID": 10981,
    "items_count": 1,
    "order_value": 15810
  },
  {
    "CustomerID": "SAVEA",
    "OrderID": 11030,
    "items_count": 4,
    "order_value": 12615.05
  },
  {
    "CustomerID": "RATTC",
    "OrderID": 10889,
    "items_count": 2,
    "order_value": 11380
  },
  {
    "CustomerID": "SIMOB",
    "OrderID": 10417,
    "items_count": 4,
    "order_value": 11188.4
  },
  {
    "CustomerID": "KOENE",
    "OrderID": 10817,
    "items_count": 4,
    "order_value": 10952.84
  },
  {
    "CustomerID": "HUNGO",
    "OrderID": 10897,
    "items_count": 2,
    "order_value": 10835.24
  },
  {
    "CustomerID": "RATTC",
    "OrderID": 10479,
    "items_count": 4,
    "order_value": 10495.6
  },
  {
    "CustomerID": "QUICK",
    "OrderID": 10540,
    "items_count": 4,
    "order_value": 10191.7
  },
  {
    "CustomerID": "QUICK",
    "OrderID": 10691,
    "items_count": 5,
    "order_value": 10164.8
  }
]
```

Opcjonalnie: jeżeli chcesz potwierdzić zgodność formalnie, możesz napisać zapytanie z WITH, które porówna wartości zamówień z obu modeli dla wszystkich 830 zamówień.

```sql
WITH
  flat AS (
    SELECT
      o.OrderID,
      SUM(od.UnitPrice * od.Quantity * (1 - IFMISSINGORNULL(od.Discount, 0))) AS value_flat
    FROM `north0`._default.orders AS o
    JOIN `north0`._default.orderdetails AS od ON od.OrderID = o.OrderID
    WHERE o.OrderID IS NOT MISSING
    GROUP BY o.OrderID
  ),
  nested AS (
    SELECT
      n.OrderID,
      SUM(item.UnitPrice * item.Quantity * (1 - IFMISSINGORNULL(item.Discount, 0))) AS value_nested
    FROM `north0`._default.orders_nested AS n
    UNNEST n.items AS item
    WHERE n.OrderID IS NOT MISSING
    GROUP BY n.OrderID
  )
SELECT
  flat.OrderID,
  ROUND(flat.value_flat, 2) AS value_flat,
  ROUND(nested.value_nested, 2) AS value_nested,
  ROUND(ABS(flat.value_flat - nested.value_nested), 2) AS diff
FROM flat
JOIN nested ON nested.OrderID = flat.OrderID
WHERE ABS(flat.value_flat - nested.value_nested) > 0.01
ORDER BY diff DESC;
```

```json
{
  "results": []
}
```

Zrobiłam jeszcze wersję z EXCEPT:

```sql
(SELECT
   n.OrderID,
   n.CustomerID,
   ROUND(SUM(item.UnitPrice * item.Quantity * (1 - IFMISSINGORNULL(item.Discount, 0))), 2) AS order_value,
   COUNT(1) AS items_count
 FROM `north0`._default.orders_nested AS n
 UNNEST n.items AS item
 WHERE n.OrderID IS NOT MISSING
 GROUP BY n.OrderID, n.CustomerID
 ORDER BY order_value DESC
 LIMIT 10)
EXCEPT
(SELECT
   o.OrderID,
   o.CustomerID,
   ROUND(SUM(od.UnitPrice * od.Quantity * (1 - IFMISSINGORNULL(od.Discount, 0))), 2) AS order_value,
   COUNT(1) AS items_count
 FROM `north0`._default.orders AS o
 JOIN `north0`._default.orderdetails AS od ON od.OrderID = o.OrderID
 WHERE o.OrderID IS NOT MISSING
 GROUP BY o.OrderID, o.CustomerID
 ORDER BY order_value DESC
 LIMIT 10);
```

```json
{
  "results": []
}
```

### W komentarzu napisz

**Na czym polega różnica między JOIN i UNNEST?**

JOIN łączy dwie osobne kolekcje przez warunek na wspólnym polu, używamy go wtedy, kiedy dane są rozdzielone między różne dokumenty. UNNEST rozbija tablicę, która już jest wewnątrz jednego dokumentu, na osobne wiersze. Wynik jest taki sam, ale punkt wyjścia jest zupełnie inny, JOIN wymaga, żeby dane do połączenia istniały w dwóch miejscach, UNNEST zakłada, że są w jednym.

**Dlaczego w modelu zagnieżdżonym nie trzeba łączyć orders z orderdetails?**

Bo nie ma osobnej kolekcji orderdetails. Pozycje są w dokumencie zamówienia jako tablica items. Wystarczy odczytać dokument i rozbić tę tablicę. Nie ma czego z czym łączyć.

**Czy oba podejścia dają ten sam wynik biznesowy?**

Tak. Top 10 zamówień z obu zapytań wyszło identycznie - te same numery, te same wartości, te same liczby pozycji.

**Kiedy zagnieżdżanie pozycji zamówienia w dokumencie może być wygodne?**

Wtedy, kiedy aplikacja prawie zawsze czyta pozycje razem z zamówieniem, np. wyświetla szczegóły zamówienia, generuje fakturę, pokazuje historię klienta. W takiej sytuacji jedno pobranie dokumentu zwraca komplet danych, bez konieczności łączenia z drugą kolekcją. Działa też dobrze, kiedy pozycji jest niedużo i kiedy aktualizują się atomowo razem z zamówieniem.

**Kiedy lepiej zostawić dane w osobnych kolekcjach?**

Kiedy pozycje są analizowane niezależnie od zamówień, np. raporty sprzedaży po produktach, gdzie agregujemy pozycje z setek różnych zamówień. W zagnieżdżonym modelu trzeba by za każdym razem rozbijać tablice ze wszystkich zamówień, żeby dostać się do pozycji. Drugi powód to rozmiar. Jeśli pozycji mogłoby być tysiące w jednym zamówieniu, dokument urośnie do nieprzyzwoitych rozmiarów i każda aktualizacja stanie się droga.

---

## 6. EXPLAIN i refleksja końcowa -- 2 pkt

### Cel

Nie wystarczy wiedzieć, że zapytanie działa. Trzeba jeszcze rozumieć, w jaki sposób baza je wykonuje.

### Część A -- plan dla zapytania z JOIN

Wybierz zapytanie z zadania 3 albo 5 i uruchom je z EXPLAIN (albo za pomocą przycisku w menu).

Przykład:

```sql
EXPLAIN
SELECT
  o.OrderID,
  o.CustomerID,
  ROUND(SUM(od.UnitPrice * od.Quantity * (1 - IFMISSINGORNULL(od.Discount, 0))), 2) AS order_value,
  COUNT(1) AS items_count
FROM `north0`._default.orders AS o
JOIN `north0`._default.orderdetails AS od
  ON od.OrderID = o.OrderID
WHERE o.OrderID IS NOT MISSING
GROUP BY o.OrderID, o.CustomerID
ORDER BY order_value DESC
LIMIT 10;
```

![img](./_img/zad6_A.png)

### Część B -- plan dla zapytania z UNNEST

Wybierz zapytanie z zadania 4 i uruchom je z EXPLAIN.

```sql
EXPLAIN
SELECT
  n.OrderID,
  n.CustomerID,
  ROUND(SUM(item.UnitPrice * item.Quantity * (1 - IFMISSINGORNULL(item.Discount, 0))), 2) AS order_value,
  COUNT(1) AS items_count
FROM `north0`._default.orders_nested AS n
UNNEST n.items AS item
WHERE n.OrderID IS NOT MISSING
GROUP BY n.OrderID, n.CustomerID
ORDER BY order_value DESC
LIMIT 10;
```

![img](./_img/zad6_B.png)

### Część C -- porównanie

Porównaj oba plany na poziomie ogólnym.

Nie opisuj całego planu. Wystarczy wskazać, z jakich indeksów korzysta zapytanie, czy pojawia się JOIN albo UNNEST, oraz gdzie widać agregację i sortowanie.

Wskaż elementy typu:

- IndexScan,
- Fetch,
- NestedLoopJoin,
- Unnest,
- Group,
- Order,
- Limit.

Najwyraźniejsza różnica to obecność NestedLoopJoin w planie A i Unnest w planie B. Plan A musi pracować z dwoma kolekcjami i dwoma indeksami - dla każdego zamówienia z orders planner sięga przez idx_orderdetails_orderid po pasujące pozycje, a potem dociąga je drugim Fetch. Plan B obchodzi się jedną kolekcją i jednym indeksem, bo pozycje są już wewnątrz dokumentu zamówienia, wystarczy je rozwinąć operatorem Unnest. Indeks idx_orders_nested_orderid w planie B służy tylko do wyboru zamówień, sam Unnest indeksu nie potrzebuje, bo operuje na danych z dokumentu pobranego wczesniej przez Fetch. W planie A drugi indeks jest konieczny, bo dla każdego zamówienia trzeba odnaleźć pasujące pozycje w osobnej kolekcji. Końcówka obu planów (agregacja → projekcja → sortowanie z limitem) jest praktycznie identyczna.

### W komentarzu końcowym napisz

Odpowiedz w kilku zdaniach:

**Co było największą różnicą między Couchbase a klasyczną bazą relacyjną?**

Najbardziej widać to w dwóch rzeczach. Po pierwsze, elastyczność dokumentu. W bazie relacyjnej kolumna albo ma wartość, albo jest NULL. W Couchbase pole może w ogóle nie istnieć MISSING, więc trzeba świadomie pisać IFMISSINGORNULL albo IS NOT MISSING, żeby zapytania działały sensownie na różnych dokumentach. Po drugie, rola indeksów. W bazie relacyjnej indeks to optymalizacja, bez niego zapytanie po prostu działa wolniej. W Couchbase bez pasujacego indeksu zapytanie często się nie wykona, bo planner odmawia. To wymusza inny styl pracy, w którym indeksy projektuje się równolegle do zapytań, nie po fakcie.

**Dlaczego indeksy są tak ważne w Couchbase?**

Bo to podstawowa struktura, z której korzysta planner. Bez indeksu nie ma jak dotrzeć do dokumentów inaczej niż przez ich klucz, a tego klucza zwykle nie znamy z góry, bo szukamy po polach wewnątrz JSONa. Dzięki indeksom zamiast szukać wśród wszystkich dokumentów można znaleźć konkretne wartości w posortowanej strukturze.

**Co pokazało porównanie JOIN i UNNEST?**

Pokazało, że ten sam wynik można uzyskać dwoma drogami, ale plan wykonania wygląda inaczej. JOIN potrzebuje dwóch indeksów, dwóch operacji Fetch i operatora łączącego NestedLoopJoin. UNNEST obchodzi się jednym indeksem, jednym Fetch i rozbiciem tablicy Unnest. To nie jest tylko różnica składniowa, ale konsekwencja decyzji, czy dane trzymamy osobno, czy zagnieżdżamy.

**Czy dokumentowy model danych wyklucza analizę i raportowanie?**

Nie. Couchbase ma wszystkie elementy potrzebne do raportów, czyli agregacje, sortowanie, grupowanie, JOIN-y. Różnica jest taka, że klasyczna hurtownia danych jest projektowana pod analitykę, a baza dokumentowa zwykle pod aplikację.

**Gdybyś projektował system zamówień, kiedy rozważyłbyś zagnieżdżenie pozycji zamówienia w dokumencie zamówienia?**

Wtedy, kiedy aplikacja prawie zawsze odczytuje pozycje razem z zamówieniem, czyli przy szczegółach w panelu klienta, fakturze, potwierdzeniu na maila. Jedno pobranie dokumentu zamiast JOIN-a to konkretna oszczędność. Drugi argument to atomowość, bo pozycje zmieniają się razem z zamówieniem, więc nie da się przypadkiem zaktualizować jednego bez drugiego. Z drugiej strony, gdyby pozycje miały być analizowane masowo niezależnie od zamówień (np raporty po produktach) albo gdyby ich liczba w jednym zamówieniu mogła być duża, wtedy zagnieżdżanie zaczyna przeszkadzać i lepiej trzymać dane w osobnych kolekcjach.

---

## Zadanie dodatkowe dla chętnych

### Materializacja KPI klienta

Utwórz kolekcję customer_kpis, a następnie zapisz do niej gotowe dokumenty z metrykami klienta:

- CustomerID,
- CompanyName,
- Revenue,
- OrdersCount.

Następnie wykonaj zapytanie raportowe na kolekcji customer_kpis.

**Uwaga**: wskazówki do rozwiązania zadania znajdziesz w ściądze.

W komentarzu napisz:

- czym różni się liczenie raportu „w locie" od czytania gotowej kolekcji KPI,
- kiedy takie podejście może być użyteczne,
- jakie jest ryzyko materializowania wyników, jeśli dane źródłowe się zmieniają.
