
# 🧪 Testování knihovního systému (`test_library.py`)

Tento soubor obsahuje automatizované testy pro knihovní systém, které ověřují správnou funkčnost přidávání knih, členů, výpůjček a vracení knih. Využívá se testovací databáze `LibraryDB_test`.

---

## 📦 Importy

```python
import mysql.connector
import pytest
from test_init import create_test_tables
```

**import mysql.connector**
- Načte knihovnu `mysql-connector-python`, která umožňuje komunikaci s MySQL databází.
- Používá se k připojení, provádění dotazů a manipulaci s daty.

**import pytest**
- Importuje knihovnu pytest, která slouží k psaní a spouštění automatizovaných testů v Pythonu.
- Umožňuje využívat funkce jako `@pytest.fixture`, `assert`, a `raises`.

**from test_init import create_test_tables**
- Importuje pomocnou funkci `create_test_tables` ze souboru `test_init.py`.
- Tato funkce se stará o vytvoření databázových tabulek v testovací databázi (`LibraryDB_test`) před spuštěním samotných testů.

---

## 🔧 Fixtures

### `setup_test_db()`
```python
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    create_test_tables()
```
- Tato fixture se spustí automaticky jednou za celou testovací relaci (`scope="session"` a `autouse=True`).
- Volá funkci `create_test_tables()`, která vytvoří potřebné tabulky v testovací databázi.
- Slouží jako příprava prostředí - zajistí, že testy mají s čím pracovat.

### `db_connection()`
```python
@pytest.fixture(scope="module")
def db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="LibraryDB_test"  # ⬅️ oddělená testovací databáze
    )
    yield conn
    conn.close()
```
- Otevře připojení k databázi `LibraryDB_test`, určené pouze pro testování.
- `yield conn` zpřístupní připojení testovací funkci, která jej použije.
- Po dokončení všech testů v daném modulu se připojení automaticky zavře (`conn.close()`).

**Parametr scope="module":**
- Znamená, že jedno připojení k databázi je sdílené pro všechny testy v daném souboru (modulu).

---

## ✅ Testované funkce

### `test_add_book`
- Ověřuje, že po přidání knihy do databáze ji lze správně vyhledat.
- Po testu se testovací záznam odstraní.

### `test_add_member`
- Testuje vložení nového člena a kontrolu podle e-mailu.
- Zajišťuje úklid odstraněním testovacího člena.

### `test_loan_book`
- Ověřuje proces výpůjčky knihy.
- Po výpůjčce se zkontroluje, že kniha již není dostupná (`Available = FALSE`).
- Po testu probíhá kompletní úklid.

### `test_return_book`
- Testuje vrácení knihy – nastavuje `ReturnDate` a mění `Available` zpět na `TRUE`.
- Obsahuje úklid testovacích dat.

### `test_duplicate_member_email_raises_error`
- Testuje, že při pokusu o vložení člena se stejným e-mailem vznikne chyba (`IntegrityError`).
- Potvrzuje správné fungování omezení `UNIQUE` na sloupci `Email`.

---

📌 **Poznámka:**
Každý test je navržen tak, aby byl samostatný a nezávislý – obsahuje vlastní přípravu dat a úklid. Výsledkem je spolehlivé a opakovatelné testování.
