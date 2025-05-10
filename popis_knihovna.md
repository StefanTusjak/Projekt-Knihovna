
# 🗂️ Popis Python projektu „Knihovna“

### 1. Import knihoven

```python
import mysql.connector
import subprocess
```
**import mysql.connector**

Tento řádek načítá knihovnu *mysql.connector*, která umožňuje pracovat s MySQL databázemi v Pythonu.

Pochází z balíčku mysql-connector-python, který je potřeba nainstalovat pomocí příkazu:
```python
pip install mysql-connector-python
```
Budeme ji používat pro připojení, vykonávání SQL dotazů a správu databáze.

---

**import subprocess**

Slouží k spouštění externích programů nebo příkazů z Python skriptu.

V tomto projektu jej využíváme ke spuštění testovacích souborů pomocí pytest nebo python test_init.py.

Příkaz subprocess.run(...) spustí externí skript tak, jako bychom ho spustili ručně v terminálu.

## 🔗 2. Funkce `get_connection()`
```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",  # změň podle sebe
        database="LibraryDB"
    )
```
Slouží k připojení do databáze `LibraryDB` pomocí přihlašovacích údajů (`localhost`, `root`, `1111`).

**def get_connection():**

- Definujeme novou funkci s názvem get_connection.
- Tato funkce nemá žádné vstupní parametry.
- Jejím úkolem je vytvořit a vrátit připojení k databázi.

**return mysql.connector.connect(...):**
- Pomocí mysql.connector.connect() se pokoušíme navázat spojení s MySQL databází
- Vracíme objekt připojení (Connection object), který bude použit v dalších částech programu (např. pro spouštění SQL dotazů).

**host="localhost"**
- Označuje, že databáze běží lokálně (na stejném počítači jako tento skript).

**user="root"**
- Používá se uživatel root, což je výchozí administrátorský účet v MySQL.

**password="1111"**
- Heslo k účtu root.

- ⚠️ Doporučení: Pro ostré nasazení nikdy neukládej heslo v kódu – použij konfigurační soubor nebo prostředí (env proměnné).**

**database="LibraryDB"**
- Jméno databáze, ke které se chceme připojit.
- Tato databáze musí být v MySQL již vytvořena, jinak dojde k chybě při připojení.

---

## 🗃️ 3. Funkce `create_tables()`
Tato funkce vytváří 3 tabulky:
```python
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Books (
        BookID INT PRIMARY KEY AUTO_INCREMENT,
        Title VARCHAR(255) NOT NULL,
        Author VARCHAR(255) NOT NULL,
        Available BOOLEAN DEFAULT TRUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Members (
        MemberID INT PRIMARY KEY AUTO_INCREMENT,
        Name VARCHAR(255) NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Loans (
        LoanID INT PRIMARY KEY AUTO_INCREMENT,
        BookID INT NOT NULL,
        MemberID INT NOT NULL,
        LoanDate DATE NOT NULL,
        ReturnDate DATE DEFAULT NULL,
        FOREIGN KEY (BookID) REFERENCES Books(BookID),
        FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Tabulky byly úspěšně vytvořeny (nebo již existují).")
```

**conn = get_connection()**
- Zavolá funkci get_connection() a uloží připojení k databázi do proměnné conn.

**cursor = conn.cursor()**
- Vytvoří tzv. kurzor – objekt, který umožňuje posílat SQL příkazy do databáze.

# Vytváření tabulek
**cursor.execute(""" CREATE TABLE IF NOT EXISTS ... """)**
- Každý blok `cursor.execute(...)` vytváří jednu tabulku v databázi.
- Příkaz `CREATE TABLE IF NOT EXISTS` zajistí, že se tabulka vytvoří pouze tehdy, pokud ještě neexistuje - nedojde tedy k chybě při opětovném spuštění.

# Tabulky:

**Books** - informace o knihách (název, autor, dostupnost).

**Members** - členové knihovny (jméno, e-mail).

**Loans** - výpůjčky, napojené na Books a Members pomocí cizích klíčů (FOREIGN KEY).

---

**conn.commit()**
- Uloží změny provedené v databázi (např. vytvoření tabulek).

**cursor.close() a conn.close()**
- Ukončí práci s databází – uzavře kurzor i připojení, aby nedocházelo k úniku prostředků (paměti/síťových spojení).

**print(...)**
- Potvrzení pro uživatele, že tabulky byly vytvořeny nebo už existují.


---

## ➕ 4. Funkce `add_book()`
Načte název a autora knihy od uživatele a vloží ji do tabulky `Books`.

```python
def add_book():
    title = input("Název knihy: ")
    author = input("Autor: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Books (Title, Author) VALUES (%s, %s)", (title, author))
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Kniha byla přidána.")
```

**title = input("Název knihy: ")**
- Zobrazí uživateli výzvu k zadání názvu knihy a výsledek uloží do proměnné `title`.

**author = input("Autor: ")**
- Načte jméno autora z uživatelského vstupu a uloží do proměnné `author`.

**conn = get_connection()**
- Vytvoří připojení k databázi pomocí dříve definované funkce `get_connection()`.

**cursor = conn.cursor()**
- Vytvoří kurzor pro práci s databází - umožňuje vykonávat SQL dotazy.

**cursor.execute("INSERT INTO Books (Title, Author) VALUES (%s, %s)", (title, author))**
- Vloží nový záznam (knihu) do tabulky `Books`.
- Používáme parametrizovaný dotaz (pomocí `%s`), což chrání před SQL injection útoky.
- Hodnoty `title` a `author` jsou předány jako druhý argument ve formě n-tice `(title, author)`.

**conn.commit()**
- Potvrdí změny v databázi - bez tohoto kroku by se nová kniha fyzicky neuložila.

**cursor.close() a conn.close()**
- Uzavřou kurzor a připojení k databázi - důležité kvůli uvolnění systémových prostředků.

**print("✅ Kniha byla přidána.")**
- Vytiskne uživateli zprávu o úspěšném přidání knihy.

---

## ➕ 5. Funkce `add_member()`
Načte jméno a e-mail člena a vloží ho do tabulky `Members`. E-mail musí být unikátní.
```python
def add_member():
    name = input("Jméno člena: ")
    email = input("E-mail: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Members (Name, Email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Člen byl přidán.")
```
**name = input("Jméno člena: ")**
- Zobrazí výzvu pro zadání jména člena knihovny a uloží výsledek do proměnné `name`.

**email = input("E-mail: ")**
- Načte e-mailovou adresu člena, uloží do proměnné `email`.

**conn = get_connection()**
- Otevře připojení k databázi.

**cursor = conn.cursor()**
- Vytvoří kurzor pro provádění SQL příkazů.

**cursor.execute("INSERT INTO Members (Name, Email) VALUES (%s, %s)", (name, email))**
- Vloží nového člena do tabulky `Members`.
- Používá parametrizovaný dotaz (`%s`) - zabezpečený způsob předávání hodnot do SQL.
- E-mail musí být v databázi unikátní (`UNIQUE`), takže pokud by se zadal duplicitní, vložení selže.

**conn.commit()**
- Potvrdí provedení změny - bez toho by záznam nebyl trvale uložen.

**cursor.close() a conn.close()**
- Ukončí práci s databází a uzavřou spojení.

**print("✅ Člen byl přidán.")**
- Informuje uživatele o úspěšném vložení člena.

---

## 📕 6. Funkce `loan_book()`
Načte ID knihy a člena. Vytvoří záznam do `Loans`. Nastaví u knihy `Available = FALSE`.
```python
def loan_book():
    book_id = int(input("ID knihy: "))
    member_id = int(input("ID člena: "))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Loans (BookID, MemberID, LoanDate) VALUES (%s, %s, CURDATE())", (book_id, member_id))
    cursor.execute("UPDATE Books SET Available = FALSE WHERE BookID = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("📕 Kniha byla vypůjčena.")
```

**book_id = int(input("ID knihy: "))**
- Uživateli se zobrazí výzva k zadání ID knihy, kterou chce vypůjčit.
- Hodnota se převede na celé číslo a uloží do proměnné `book_id`.

**member_id = int(input("ID člena: "))**
- Uživateli se zobrazí výzva k zadání ID člena, který si knihu půjčuje.
- Hodnota se uloží do proměnné `member_id`.

**conn = get_connection()**
- Otevře připojení k databázi.

**cursor = conn.cursor()**
- Vytvoří kurzor pro provádění SQL dotazů.

# Vložení výpůjčky:
**cursor.execute(...)** - vložení záznamu do tabulky `Loans`
```python
INSERT INTO Loans (BookID, MemberID, LoanDate)
VALUES (%s, %s, CURDATE())
```
- Vytvoří nový záznam o výpůjčce do tabulky `Loans`.
- `CURDATE()` automaticky nastaví aktuální datum jako den výpůjčky.
- `book_id` a `member_id` jsou dosazeny do dotazu jako hodnoty.

# Aktualizace dostupnosti knihy:
`cursor.execute("UPDATE Books SET Available = FALSE WHERE BookID = %s", (book_id,))`
- Označí knihu jako nedostupnou (`Available = FALSE`).
- Tím se zabrání její další výpůjčce, dokud nebude vrácena.

---

**conn.commit()**
- Potvrdí obě změny - výpůjčku i úpravu dostupnosti.

**cursor.close() a conn.close()**
- Uzavřou kurzor i databázové připojení.

**print("📕 Kniha byla vypůjčena.")**
- Informuje uživatele, že výpůjčka proběhla úspěšně.

---

## 📗 7. Funkce `return_book()`
- Načte ID půjčky a knihy. U půjčky nastaví datum vrácení (`ReturnDate = CURDATE()`). U knihy nastaví `Available = TRUE`.
```python
def return_book():
    loan_id = int(input("ID půjčky: "))
    book_id = int(input("ID knihy: "))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Loans SET ReturnDate = CURDATE() WHERE LoanID = %s", (loan_id,))
    cursor.execute("UPDATE Books SET Available = TRUE WHERE BookID = %s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("📗 Kniha byla vrácena.")
```

**loan_id = int(input("ID půjčky: "))**
- Zobrazí výzvu k zadání ID výpůjčky, kterou chceme označit jako vrácenou.
- Hodnota se převede na celé číslo a uloží do `loan_id`.

**book_id = int(input("ID knihy: "))**
- Uživatel zadá ID vracené knihy.
- Hodnota se převede na celé číslo a uloží do `book_id`.

**conn = get_connection()**
- Připojení k databázi.

**cursor = conn.cursor()**
- Otevře kurzor pro provádění SQL dotazů.

# Aktualizace výpůjčky:
`cursor.execute("UPDATE Loans SET ReturnDate = CURDATE() WHERE LoanID = %s", (loan_id,))`
- Nastaví aktuální datum (`CURDATE()`) jako datum vrácení pro danou výpůjčku.
- Vyhledání výpůjčky probíhá podle zadaného `LoanID`.

# Aktualizace dostupnosti knihy:
` cursor.execute("UPDATE Books SET Available = TRUE WHERE BookID = %s", (book_id,))`
- Změní stav knihy na dostupnou (`Available = TRUE`), aby ji bylo možné znovu vypůjčit.

---

**conn.commit()**
- Potvrdí obě změny - vrácení knihy i její znovuzpřístupnění.

**cursor.close() a conn.close()**
- Uzavřou kurzor a připojení k databázi.

**print("📗 Kniha byla vrácena.")**
- Informuje uživatele, že vrácení knihy bylo úspěšné.

---

## 📚 8. Funkce `list_books()`
Vypíše všechny knihy z tabulky `Books` a jejich dostupnost (`Dostupná` nebo `Vypůjčená`).

---

## 👥 9. Funkce `list_members()`
Vypíše všechny členy z tabulky `Members`.

---

## 📄 10. Funkce `list_loans()`
Spojí data z `Loans`, `Books` a `Members` a zobrazí seznam výpůjček včetně data vrácení (nebo označení „NEVRÁCENO“).

---

## 🔬 11. Funkce `run_tests()`
- Spustí `test_init.py` pro vytvoření testovací databáze/tabulek.
- Nabídne spuštění jednotlivých testovacích případů přes `pytest`.

---

## 📖 12. Funkce `menu()`
Textové menu pro obsluhu knihovního systému:

1. Přidání knihy  
2. Přidání člena  
3. Výpůjčka knihy  
4. Vrácení knihy  
5. Seznam knih  
6. Seznam členů  
7. Seznam půjček  
8. Spuštění testů  
0. Ukončení programu  

---

## 🧷 13. Blok `if __name__ == "__main__":`
- Nejprve vytvoří tabulky (pokud ještě neexistují).
- Spustí hlavní menu.

---
