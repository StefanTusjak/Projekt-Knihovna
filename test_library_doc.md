
# 🧪 Testování knihovního systému (`test_library.py`)

Tento soubor obsahuje automatizované testy pro knihovní systém, které ověřují správnou funkčnost přidávání knih, členů, výpůjček a vracení knih. Využívá se testovací databáze `LibraryDB_test`.

---

## 📦 Importy

```python
import mysql.connector
import pytest
from test_init import create_test_tables
```

- `mysql.connector`: Připojení k MySQL databázi.
- `pytest`: Knihovna pro spouštění testů.
- `create_test_tables`: Pomocná funkce pro přípravu databáze před testováním.

---

## 🔧 Fixtures

### `setup_test_db()`
- Automaticky se spouští při startu testovací relace.
- Vytvoří testovací databázové tabulky.

### `db_connection()`
- Otevře připojení k testovací databázi `LibraryDB_test`.
- Po dokončení testu připojení uzavře pomocí `yield`.

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
