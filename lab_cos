**Laboratorium -- dokumentowe bazy danych: Couchbase**

**Temat:** Couchbase, dokumenty JSON, indeksy, JOIN, UNNEST i analiza
danych Northwind

**Baza:** Couchbase Community uruchomiony w Dockerze

**Bucket:** north0

**Scope:** \_default

**Główne kolekcje:** orders, orderdetails, customers, products,
orders_nested

**Imię i nazwisko:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Grupa:**
\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

**Cel ćwiczenia**

Po wykonaniu laboratorium student powinien umieć:

> 1\. uruchomić i zweryfikować środowisko Couchbase,
>
> 2\. poruszać się po panelu Couchbase i korzystać z Query Workbench,
>
> 3\. rozumieć strukturę bucket → scope → collection,
>
> 4\. wykonać podstawowe zapytania SQL++ / N1QL na dokumentach JSON,
>
> 5\. wyjaśnić, dlaczego Couchbase wymaga indeksów do wykonywania
> zapytań,
>
> 6\. odróżnić primary index od indeksu celowego,
>
> 7\. wykonać JOIN między kolekcjami dokumentów,
>
> 8\. porównać model niezagnieżdżony z modelem zagnieżdżonym,
>
> 9\. użyć UNNEST do rozbijania tablicy zagnieżdżonej w dokumencie,
>
> 10\. wykorzystać EXPLAIN do podstawowej interpretacji planu zapytania.

**Ważne informacje**

W tym laboratorium pracujemy na danych Northwind załadowanych do
Couchbase.

Dane są dostępne w dwóch wariantach modelowania:

**Model niezagnieżdżony**

Dane są podzielone na osobne kolekcje:

- orders -- zamówienia,

- orderdetails -- pozycje zamówień,

- customers -- klienci,

- products -- produkty.

W tym wariancie, aby połączyć zamówienia z pozycjami zamówień, używamy
JOIN.

**Model zagnieżdżony**

Dodatkowo przygotowana jest kolekcja:

- orders_nested.

W tej kolekcji jeden dokument odpowiada jednemu zamówieniu, a pozycje
zamówienia są zapisane wewnątrz dokumentu w tablicy items. W tym
wariancie do rozbicia pozycji zamówienia używamy UNNEST.

**Jak korzystać ze ściągi**

Do laboratorium dołączona jest ściąga Couchbase_SQLPP_sciaga.md.
Korzystaj z niej jak z dokumentacji pomocniczej: sprawdzaj składnię
JOIN, UNNEST, IFMISSINGORNULL, CREATE INDEX i EXPLAIN, ale nie kopiuj
bezrefleksyjnie gotowych rozwiązań. Oceniane są również komentarze i
interpretacja.

**Sprawozdanie**

Oddawane sprawozdanie powinno zawierać:

- kod zapytań,

- wyniki zapytań jako tabele albo zrzuty ekranu,

- krótkie komentarze interpretacyjne,

- odpowiedzi na pytania wskazane w zadaniach.

**Format sprawozdania:** PDF albo Markdown.

**Kod SQL++ / N1QL formatuj jako bloki kodu.**

**Nie oddawaj samych zrzutów ekranu bez komentarza.**

**Punktacja**

  -----------------------------------------------------------------------
  **Zadanie**             **Temat**               **Punkty**
  ----------------------- ----------------------- -----------------------
  0                       Gotowość środowiska     0

  1                       Pierwsze poznanie       1
                          Couchbase i danych      

  2                       Indeksy: brak indeksu,  2
                          primary index,          
                          secondary index         

  3                       JOIN na kolekcjach      2
                          dokumentów              

  4                       Model niezagnieżdżony   2
                          vs zagnieżdżony: JOIN   
                          vs UNNEST               

  5                       Agregacja biznesowa     1

  6                       EXPLAIN i refleksja     2
                          końcowa                 

  **Razem**                                       **10**
  -----------------------------------------------------------------------

**0. Gotowość środowiska -- 0 pkt**

To zadanie nie jest punktowane, ale jest warunkiem rozpoczęcia pracy.

**Wykonaj**

> 1\. Uruchom środowisko:

  -----------------------------------------------------------------------
  docker compose \--profile init up -d
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

> 2\. Sprawdź, czy działają kontenery:

  -----------------------------------------------------------------------
  docker ps
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

> 3\. Wejdź do panelu Couchbase:

  -----------------------------------------------------------------------
  http://localhost:8091
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

> 4\. Zaloguj się:

  -----------------------------------------------------------------------
  Login: student\
  Hasło: student
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

> 5\. Sprawdź, czy widzisz bucket:

  -----------------------------------------------------------------------
  north0
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

> 6\. Wejdź do Query Workbench i uruchom:

  -----------------------------------------------------------------------
  SELECT 1 AS test;
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

**Do sprawozdania**

Nie trzeba dołączać pełnych logów. Wystarczy jedno zdanie:

Środowisko Couchbase zostało uruchomione, logowanie działa, bucket
north0 jest widoczny, a Query Workbench wykonuje zapytania.

**1. Pierwsze poznanie Couchbase i danych -- 1 pkt**

**Cel**

Poznaj podstawową strukturę danych w Couchbase i sprawdź, jakie kolekcje
są dostępne.

**Wykonaj**

1.  W panelu Couchbase za pomocą zakładek w menu bocznym np. 'Buckets',
    'Documents', 'Query' zbadaj strukturę:

  -----------------------------------------------------------------------
  bucket → scope → collection
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

> 2\. W Query Workbench policz liczbę dokumentów w kolekcjach:

- orders,

- orderdetails,

- customers,

- products,

- orders_nested.

W poprawnie zainicjalizowanym środowisku powinieneś otrzymać
orientacyjnie:

  -----------------------------------
  **Kolekcja**        **Liczba
                      dokumentów**
  ------------------- ---------------
  orders              83?

  orderdetails        215?

  customers           9?

  products            7?

  orders_nested       83?
  -----------------------------------

> 3\. Podejrzyj kilka dokumentów z kolekcji orders.
>
> 4\. Podejrzyj jeden dokument z kolekcji orders_nested.

**Wskazówki**

Przykład zapytania liczącego dokumenty:

  -----------------------------------------------------------------------
  SELECT COUNT(1) AS orders_count\
  FROM \`north0\`.\_default.orders\
  WHERE OrderID IS NOT MISSING;
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

Przykład podejrzenia dokumentu:

  -----------------------------------------------------------------------
  SELECT o\
  FROM \`north0\`.\_default.orders AS o\
  WHERE o.OrderID IS NOT MISSING\
  LIMIT 3;
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

**W komentarzu napisz**

- Co oznaczają pojęcia bucket, scope i collection?

- Ile dokumentów znajduje się w kolekcjach orders, orderdetails,
  customers, products i orders_nested?

- Czym różni się dokument z kolekcji orders od dokumentu z kolekcji
  orders_nested?

**2. Indeksy: brak indeksu, primary index, secondary index -- 2 pkt**

**Cel**

Zobacz, że Couchbase nie wykonuje zapytań bez odpowiedniego indeksu.
Następnie porównaj indeks główny z indeksem celowym.

**Część A -- zapytanie bez indeksu**

Wykonaj zapytanie:

  -----------------------------------------------------------------------
  SELECT\
  c.Country,\
  COUNT(1) AS customers_count\
  FROM \`north0\`.\_default.customers AS c\
  GROUP BY c.Country\
  ORDER BY customers_count DESC;
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

**Oczekiwane zachowanie**

W świeżo uruchomionym środowisku zapytanie powinno zakończyć się błędem
informującym o braku indeksu. Jeżeli zapytanie działa od razu, oznacza
to najczęściej, że w środowisku pozostał wcześniej utworzony indeks.

**Część B -- primary index**

Utwórz primary index:

  -----------------------------------------------------------------------
  CREATE PRIMARY INDEX idx_customers_primary\
  ON \`north0\`.\_default.customers;
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

Powtórz zapytanie z części A.

**Część C -- indeks celowy**

Usuń primary index:

  -----------------------------------------------------------------------
  DROP INDEX idx_customers_primary\
  ON \`north0\`.\_default.customers;
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

Utwórz indeks celowy na polu Country:

  -----------------------------------------------------------------------
  CREATE INDEX idx_customers_country\
  ON \`north0\`.\_default.customers(Country);
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

Wykonaj zapytanie z warunkiem indeksowym:

  -----------------------------------------------------------------------
  SELECT\
  c.Country,\
  COUNT(1) AS customers_count\
  FROM \`north0\`.\_default.customers AS c\
  WHERE c.Country IS NOT MISSING\
  GROUP BY c.Country\
  ORDER BY customers_count DESC;
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

**W komentarzu napisz**

- Co się stało przy próbie wykonania zapytania bez indeksu?

- Czym różni się primary index od indeksu celowego?

- Dlaczego w zapytaniu po utworzeniu indeksu celowego dodano warunek
  WHERE c.Country IS NOT MISSING?

- Dlaczego w środowisku produkcyjnym nie powinno się traktować primary
  index jako rozwiązania docelowego?

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

  -----------------------------------------------------------------------
  CREATE INDEX idx_customers_customerid\
  ON \`north0\`.\_default.customers(CustomerID);
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

Jeżeli indeks już istnieje, Couchbase zwróci komunikat o istniejącym
indeksie. W takiej sytuacji przejdź do kolejnego kroku.

Następnie przygotuj zapytanie łączące orders z customers.

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

**Część C -- wartość zamówienia**

Policz wartość zamówienia według wzoru:

  -----------------------------------------------------------------------
  wartość pozycji = UnitPrice \* Quantity \* (1 - Discount)
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

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

**W komentarzu napisz**

- Czy JOIN w Couchbase przypomina składnię znaną z SQL?

- Czym różni się takie łączenie od relacji w klasycznej bazie relacyjnej
  (np. czy baza wymusza klucze obce i spójność relacji tak jak w typowym
  modelu relacyjnym)?

- Dlaczego indeks po stronie dołączanej kolekcji jest ważny?

- Czy największe zamówienia mają zawsze największą liczbę pozycji?

**4. Model niezagnieżdżony vs zagnieżdżony:** JOIN **vs** UNNEST **-- 2
pkt**

**Cel**

Porównaj dwa sposoby modelowania tych samych danych:

> 1\. model niezagnieżdżony: orders + orderdetails,
>
> 2\. model zagnieżdżony: orders_nested, gdzie pozycje zamówienia są
> tablicą items.

**Część A -- obejrzyj dokument zagnieżdżony**

Podejrzyj dokument zamówienia o numerze 10248 z kolekcji orders_nested.

Zwróć uwagę na pole:

  -----------------------------------------------------------------------
  items
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

**Część B -- rozbij tablicę** items **przez** UNNEST

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

UNNEST rozbija tablicę zagnieżdżoną w dokumencie na osobne rekordy.
Każdy element tablicy staje się oddzielnym wierszem w wyniku:

  -----------------------------------------------------------------------
  SELECT\
  n.OrderID,\
  item.ProductID\
  FROM \`north0\`.\_default.orders_nested AS n\
  UNNEST n.items AS item\
  WHERE n.OrderID = 10248;
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

Rozbuduj to zapytanie o pozostałe kolumny wymienione powyżej.

**\**

**Część C -- policz wartość zamówień z modelu zagnieżdżonego**

Na kolekcji orders_nested policz:

- OrderID,

- CustomerID,

- order_value,

- liczbę pozycji.

Użyj UNNEST.

Pokaż 10 zamówień o najwyższej wartości.

**Część D -- porównaj wynik z modelem niezagnieżdżonym**

Porównaj wynik z części C z wynikiem otrzymanym wcześniej przez JOIN na
orders i orderdetails (zadanie 3C).

Minimum: porównaj wizualnie top 10 zamówień z obu podejść i napisz, czy
wyniki są zgodne.

Opcjonalnie: jeżeli chcesz potwierdzić zgodność formalnie, możesz
napisać zapytanie z WITH, które porówna wartości zamówień z obu modeli
dla wszystkich 830 zamówień.

**W komentarzu napisz**

- Na czym polega różnica między JOIN i UNNEST?

- Dlaczego w modelu zagnieżdżonym nie trzeba łączyć orders z
  orderdetails?

- Czy oba podejścia dają ten sam wynik biznesowy?

- Kiedy zagnieżdżanie pozycji zamówienia w dokumencie może być wygodne?

- Kiedy lepiej zostawić dane w osobnych kolekcjach?

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

  -----------------------------------------------------------------------
  CREATE INDEX idx_products_productid\
  ON \`north0\`.\_default.products(ProductID);\
  \
  CREATE INDEX idx_orderdetails_productid\
  ON \`north0\`.\_default.orderdetails(ProductID);
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

Jeżeli indeks już istnieje, Couchbase zwróci komunikat o istniejącym
indeksie --- to nie jest błąd.

**Wariant B -- top 10 klientów po wartości zakupów**

Dla klientów policz:

- CustomerID,

- CompanyName,

- liczbę zamówień,

- łączną wartość zakupów.

Wykorzystaj kolekcje:

- orders,

- orderdetails,

- customers.

**W komentarzu napisz**

- Który produkt albo klient ma najwyższą wartość sprzedaży?

- Czy wynik jest łatwy do biznesowej interpretacji?

- Czy zapytanie bardziej przypomina klasyczny SQL/BI, czy pracę z
  dokumentami JSON?

**6.** EXPLAIN **i refleksja końcowa -- 2 pkt**

**Cel**

Nie wystarczy wiedzieć, że zapytanie działa. Trzeba jeszcze rozumieć, w
jaki sposób baza je wykonuje.

**Część A -- plan dla zapytania z** JOIN

Wybierz zapytanie z zadania 3 albo 5 i uruchom je z EXPLAIN (albo za
pomocą przycisku w menu).

Przykład:

  -----------------------------------------------------------------------
  EXPLAIN\
  SELECT \...
  -----------------------------------------------------------------------

  -----------------------------------------------------------------------

**Część B -- plan dla zapytania z** UNNEST

Wybierz zapytanie z zadania 4 i uruchom je z EXPLAIN.

**Część C -- porównanie**

Porównaj oba plany na poziomie ogólnym.

Nie opisuj całego planu. Wystarczy wskazać, z jakich indeksów korzysta
zapytanie, czy pojawia się JOIN albo UNNEST, oraz gdzie widać agregację
i sortowanie.

Wskaż elementy typu:

- IndexScan,

- Fetch,

- NestedLoopJoin,

- Unnest,

- Group,

- Order,

- Limit.

**W komentarzu końcowym napisz**

Odpowiedz w kilku zdaniach:

- Co było największą różnicą między Couchbase a klasyczną bazą
  relacyjną?

- Dlaczego indeksy są tak ważne w Couchbase?

- Co pokazało porównanie JOIN i UNNEST?

- Czy dokumentowy model danych wyklucza analizę i raportowanie?

- Gdybyś projektował system zamówień, kiedy rozważyłbyś zagnieżdżenie
  pozycji zamówienia w dokumencie zamówienia?

**Zadanie dodatkowe dla chętnych**

**Materializacja KPI klienta**

Utwórz kolekcję customer_kpis, a następnie zapisz do niej gotowe
dokumenty z metrykami klienta:

- CustomerID,

- CompanyName,

- Revenue,

- OrdersCount.

Następnie wykonaj zapytanie raportowe na kolekcji customer_kpis.

**Uwaga**: wskazówki do rozwiązania zadania znajdziesz w ściądze.

W komentarzu napisz:

- czym różni się liczenie raportu „w locie" od czytania gotowej kolekcji
  KPI,

- kiedy takie podejście może być użyteczne,

- jakie jest ryzyko materializowania wyników, jeśli dane źródłowe się
  zmieniają.
