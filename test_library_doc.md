
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
```python
def test_add_book(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO Books (Title, Author) VALUES ('Testovací kniha', 'Autor Test')")
    db_connection.commit()

    cursor.execute("SELECT * FROM Books WHERE Title = 'Testovací kniha'")
    result = cursor.fetchone()

    # Úklid – smažeme testovací knihu
    cursor.execute("DELETE FROM Books WHERE Title = 'Testovací kniha'")
    db_connection.commit()

    cursor.close()
    assert result is not None
```
**cursor = db_connection.cursor()**
- Vytvoří kurzor pro provádění SQL příkazů pomocí předané testovací databáze.

**cursor.execute("INSERT INTO Books ...")**
- Vloží testovací knihu s pevně daným názvem a autorem do tabulky Books.

**db_connection.commit()**
- Potvrdí změnu - bez toho by se testovací záznam fyzicky neuložil do databáze.

**cursor.execute("SELECT * FROM Books WHERE Title = 'Testovací kniha'")**
- Pokusí se najít záznam o právě vložené knize podle jejího názvu.

**result = cursor.fetchone()**
- Načte jeden řádek z výsledku - buď najde záznam, nebo vrátí `None`.

#### Úklid po testu:
**cursor.execute("DELETE FROM Books WHERE Title = 'Testovací kniha'")**
- Smaže testovací knihu, aby databáze zůstala čistá pro další testy.

**db_connection.commit()**
- Potvrdí odstranění záznamu.

#### ✅ Vyhodnocení testu:
**assert result is not None**
- Test projde pouze tehdy, pokud se záznam v databázi opravdu našel.
- Pokud ne, test selže - znamená to, že vložení neproběhlo správně.

---

### `test_add_member`
- Testuje vložení nového člena a kontrolu podle e-mailu.
- Zajišťuje úklid odstraněním testovacího člena.
```python
def test_add_member(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO Members (Name, Email) VALUES ('Tester', 'test@example.com')")
    db_connection.commit()

    cursor.execute("SELECT * FROM Members WHERE Email = 'test@example.com'")
    result = cursor.fetchone()

    # Úklid – smažeme testovacího člena
    cursor.execute("DELETE FROM Members WHERE Email = 'test@example.com'")
    db_connection.commit()

    cursor.close()
    assert result is not None
```
**cursor = db_connection.cursor()**
- Vytváří kurzor pro provádění SQL příkazů na testovací databázi.

**cursor.execute("INSERT INTO Members ...")**
- Vloží nového člena s pevně daným jménem a e-mailem do tabulky Members.

**db_connection.commit()**
- Uloží změnu v databázi - bez potvrzení by se záznam neuložil.

**cursor.execute("SELECT * FROM Members WHERE Email = 'test@example.com'")**
- Hledá právě vloženého člena podle e-mailové adresy.

**result = cursor.fetchone()**
- Získá jeden výsledek dotazu - buď záznam existuje, nebo vrátí `None`.

#### 🧹 Úklid po testu:
**cursor.execute("DELETE FROM Members WHERE Email = 'test@example.com'")**
- Odstraní testovacího člena, aby databáze zůstala čistá pro další testy.

**db_connection.commit()**
- Potvrdí smazání.

#### ✅ Vyhodnocení:
**assert result is not None**
- Test projde, pokud byl záznam o členu úspěšně nalezen.
- Pokud ne, test selže, což znamená, že vložení neproběhlo správně.

---

### `test_loan_book`
- Ověřuje proces výpůjčky knihy.
- Po výpůjčce se zkontroluje, že kniha již není dostupná (`Available = FALSE`).
- Po testu probíhá kompletní úklid.

```python
def test_loan_book(db_connection):
    cursor = db_connection.cursor()

    # Vložení knihy a člena
    cursor.execute("INSERT INTO Books (Title, Author) VALUES ('Test půjčka', 'Autor P')")
    cursor.execute("INSERT INTO Members (Name, Email) VALUES ('Čtenář', 'pujcka@example.com')")
    db_connection.commit()

    cursor.execute("SELECT BookID FROM Books WHERE Title = 'Test půjčka'")
    book_id = cursor.fetchone()[0]
    cursor.execute("SELECT MemberID FROM Members WHERE Email = 'pujcka@example.com'")
    member_id = cursor.fetchone()[0]

    # Výpůjčka
    cursor.execute("INSERT INTO Loans (BookID, MemberID, LoanDate) VALUES (%s, %s, CURDATE())", (book_id, member_id))
    cursor.execute("UPDATE Books SET Available = FALSE WHERE BookID = %s", (book_id,))
    db_connection.commit()

    cursor.execute("SELECT Available FROM Books WHERE BookID = %s", (book_id,))
    available = cursor.fetchone()[0]

    # Úklid – smažeme vše
    cursor.execute("DELETE FROM Loans WHERE BookID = %s", (book_id,))
    cursor.execute("DELETE FROM Books WHERE BookID = %s", (book_id,))
    cursor.execute("DELETE FROM Members WHERE MemberID = %s", (member_id,))
    db_connection.commit()

    cursor.close()
    assert available == 0
```
#### Vytvoření testovacích dat:
- Vloží se jedna kniha a jeden člen do databáze pomocí dvou INSERT příkazů.
- Následuje `commit()`, aby byly záznamy trvale uloženy.

#### Získání ID:
`book_id = cursor.fetchone()[0]`
- Po dotazu na knihu a člena pomocí `SELECT`, se získá jejich `BookID` a `MemberID`, které budeme potřebovat pro výpůjčku.

#### Simulace výpůjčky:
- Kniha je zapůjčena - vytvoří se záznam v tabulce Loans s dnešním datem `(CURDATE()`).
- Stav knihy se aktualizuje na `Available = FALSE`, aby se označila jako nedostupná.

#### Kontrola:
```python
available = cursor.fetchone()[0]
assert available == 0
```
- Ověříme, že sloupec `Available` je nyní nastaven na 0 (což odpovídá FALSE).
- Pokud ano, test projde.

#### Úklid:
- Všechny testovací záznamy (výpůjčka, kniha, člen) se odstraní.
- Na závěr se připojení uzavře.

---

### `test_return_book`
- Testuje vrácení knihy – nastavuje `ReturnDate` a mění `Available` zpět na `TRUE`.
- Obsahuje úklid testovacích dat.
```python
def test_return_book(db_connection):
    cursor = db_connection.cursor()

    # Připravíme záznam pro test vrácení
    cursor.execute("INSERT INTO Books (Title, Author, Available) VALUES ('Vrácená', 'Autor V', FALSE)")
    cursor.execute("INSERT INTO Members (Name, Email) VALUES ('Vrácený Člen', 'vratka@example.com')")
    db_connection.commit()

    cursor.execute("SELECT BookID FROM Books WHERE Title = 'Vrácená'")
    book_id = cursor.fetchone()[0]
    cursor.execute("SELECT MemberID FROM Members WHERE Email = 'vratka@example.com'")
    member_id = cursor.fetchone()[0]

    # Vložíme výpůjčku bez ReturnDate
    cursor.execute("INSERT INTO Loans (BookID, MemberID, LoanDate) VALUES (%s, %s, CURDATE())", (book_id, member_id))
    db_connection.commit()

    cursor.execute("SELECT LoanID FROM Loans WHERE BookID = %s AND ReturnDate IS NULL", (book_id,))
    loan_id = cursor.fetchone()[0]

    # Vrácení
    cursor.execute("UPDATE Loans SET ReturnDate = CURDATE() WHERE LoanID = %s", (loan_id,))
    cursor.execute("UPDATE Books SET Available = TRUE WHERE BookID = %s", (book_id,))
    db_connection.commit()

    cursor.execute("SELECT Available FROM Books WHERE BookID = %s", (book_id,))
    available = cursor.fetchone()[0]

    # Úklid – smažeme záznamy
    cursor.execute("DELETE FROM Loans WHERE LoanID = %s", (loan_id,))
    cursor.execute("DELETE FROM Books WHERE BookID = %s", (book_id,))
    cursor.execute("DELETE FROM Members WHERE MemberID = %s", (member_id,))
    db_connection.commit()

    cursor.close()
    assert available == 1
```
#### Vytvoření testovacích dat:
```python
cursor.execute("INSERT INTO Books (...)")
cursor.execute("INSERT INTO Members (...)")
```
- Do databáze vložíme jednu nedostupnou knihu (Available = FALSE) a jednoho člena.

**db_connection.commit()**
- Potvrzení změn - bez něj by záznamy nebyly uložené.

#### Získání ID:
```python
book_id = cursor.fetchone()[0]
member_id = cursor.fetchone()[0]
```
- Zjišťujeme ID vložené knihy a člena, které budeme potřebovat pro záznam výpůjčky.

#### Výpůjčka (bez vrácení):
```python
INSERT INTO Loans (...) VALUES (..., ..., CURDATE())
```
- Vložíme nový záznam do tabulky `Loans`, ale `ReturnDate` necháme prázdné - výpůjčka ještě nebyla vrácena.

**loan_id = cursor.fetchone()[0]**
- Získáme `LoanID` výpůjčky, která nemá vyplněné `ReturnDate`.

#### Vrácení knihy:
```python
UPDATE Loans SET ReturnDate = CURDATE() WHERE LoanID = %s
UPDATE Books SET Available = TRUE WHERE BookID = %s
```
- Nastavíme aktuální datum vrácení (`ReturnDate`) u výpůjčky.
- Označíme knihu jako opět dostupnou (`Available = TRUE`).

#### Ověření:
```python
available = cursor.fetchone()[0]
assert available == 1
```
- Ověříme, že je kniha opět dostupná.
- Hodnota 1 znamená TRUE, tedy že kniha byla vrácena správně.

#### Úklid:
```python
DELETE FROM Loans ...
DELETE FROM Books ...
DELETE FROM Members ...
```
- Všechny záznamy vytvořené během testu smažeme, aby testy zůstaly nezávislé a databáze čistá.


---

### `test_duplicate_member_email_raises_error`
- Testuje, že při pokusu o vložení člena se stejným e-mailem vznikne chyba (`IntegrityError`).
- Potvrzuje správné fungování omezení `UNIQUE` na sloupci `Email`.

```python
def test_duplicate_member_email_raises_error(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO Members (Name, Email) VALUES ('První', 'dup@example.com')")
    db_connection.commit()

    with pytest.raises(mysql.connector.errors.IntegrityError):
        cursor.execute("INSERT INTO Members (Name, Email) VALUES ('První', 'dup@example.com')")
        db_connection.commit()

    # Úklid
    cursor.execute("DELETE FROM Members WHERE Email = 'dup@example.com'")
    db_connection.commit()
    cursor.close()
```
**cursor = db_connection.cursor()**
- Otevření kurzoru pro komunikaci s databází.

#### Vložení prvního záznamu:
```python
cursor.execute("INSERT INTO Members (...)")
db_connection.commit()
```
- Vložíme testovacího člena s e-mailem dup@example.com.
- Tento e-mail je jedinečný (UNIQUE), takže další pokus o vložení stejného e-mailu musí selhat.

##### Očekávání chyby:
```python
with pytest.raises(mysql.connector.errors.IntegrityError):
    ...
```
- Pomocí `pytest.raises(...)` očekáváme, že daný blok vyvolá chybu.
- V tomto případě jde o `IntegrityError`, protože e-mail porušuje unikátní omezení ve sloupci Email.

- Co se testuje? - Test kontroluje, zda databáze správně odmítne pokus o vložení duplicity.

#### Úklid:
```python
cursor.execute("DELETE FROM Members WHERE Email = 'dup@example.com'")
db_connection.commit()
```
- Smažeme testovací záznam, aby další testy mohly pokračovat bez konfliktu.

**cursor.close()** - Uzavření kurzoru po dokončení testu.

#### Shrnutí:
- Test projde pouze tehdy, pokud druhý pokus o vložení stejného e-mailu skutečně selže a vyvolá očekávanou chybu. Pokud chyba nenastane (např. pokud by tabulka neobsahovala UNIQUE omezení), test selže.


---

📌 **Poznámka:**
Každý test je navržen tak, aby byl samostatný a nezávislý – obsahuje vlastní přípravu dat a úklid. Výsledkem je spolehlivé a opakovatelné testování.
