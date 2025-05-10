
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
```python
def list_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT BookID, Title, Author, Available FROM Books")
    print("\n📚 Seznam knih:")
    for row in cursor.fetchall():
        stav = "Dostupná" if row[3] else "Vypůjčená"
        print(f"{row[0]} – {row[1]} od {row[2]} ({stav})")
    cursor.close()
    conn.close()
```

**conn = get_connection()** - Naváže připojení k databázi.

**cursor = conn.cursor()** - Vytvoří kurzor pro provádění SQL dotazů.

**cursor.execute("SELECT BookID, Title, Author, Available FROM Books")**
- Spustí SQL dotaz, který načte všechny knihy z databáze.
- Dotaz vybírá čtyři sloupce: *ID knihy*, *název*, *autora* a *dostupnost* (Available).

**print("\n📚 Seznam knih:")** - Vypíše nadpis pro uživatele v konzoli.

# Výpis výsledků dotazu:

**for row in cursor.fetchall():**
- Prochází všechny řádky výsledku SQL dotazu.
- Každý row obsahuje hodnoty ve formátu: (*BookID*, *Title*, *Author*, *Available*).

**stav = "Dostupná" if row[3] else "Vypůjčená"**
- Pokud je hodnota ve čtvrtém sloupci (*Available*) `True`, kniha je dostupná. Jinak je označena jako „Vypůjčená“.

**print(f"{row[0]} – {row[1]} od {row[2]} ({stav})")**
- Vytiskne jeden řádek informací o knize ve formátu: `1 – Název knihy od Autor (Dostupná/Vypůjčená)`

**cursor.close() a conn.close()** -Ukončí práci s databází a uzavřou připojení.

---

## 👥 9. Funkce `list_members()`
Vypíše všechny členy z tabulky `Members`.
```python
def list_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MemberID, Name, Email FROM Members")
    print("\n👥 Seznam členů:")
    for row in cursor.fetchall():
        print(f"{row[0]} – {row[1]} ({row[2]})")
    cursor.close()
    conn.close()
```
**conn = get_connection()** - Naváže připojení k databázi.

**cursor = conn.cursor()** - Vytvoří kurzor, který umožňuje spouštět SQL příkazy.

**cursor.execute("SELECT MemberID, Name, Email FROM Members")** 
- Spustí SQL dotaz, který načte všechna data z tabulky Members.
- Vybírá konkrétně ID člena, jméno a e-mail.

**print("\n👥 Seznam členů:")**
- Vypíše nadpis před výpisem dat.

# Výpis dat:
**for row in cursor.fetchall():**
- Prochází všechny řádky výsledku dotazu.
- Každý řádek obsahuje (MemberID, Name, Email).

**print(f"{row[0]} – {row[1]} ({row[2]})")**
- Vypíše informace o členu ve formátu: `1 – Jan Novák (jan@example.com)`

**cursor.close() a conn.close()** - Ukončí práci s databází a uzavřou připojení.

---

## 📄 10. Funkce `list_loans()`
Spojí data z `Loans`, `Books` a `Members` a zobrazí seznam výpůjček včetně data vrácení (nebo označení „NEVRÁCENO“).
```python
def list_loans():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT Loans.LoanID, Books.Title, Members.Name, LoanDate, ReturnDate
        FROM Loans
        JOIN Books ON Loans.BookID = Books.BookID
        JOIN Members ON Loans.MemberID = Members.MemberID
    """)
    print("\n📄 Seznam půjček:")
    for row in cursor.fetchall():
        vraceno = row[4] if row[4] else "NEVRÁCENO"
        print(f"#{row[0]}: {row[1]} – {row[2]} | Vypůjčeno: {row[3]} | Vráceno: {vraceno}")
    cursor.close()
    conn.close()
```

**conn = get_connection()** - Otevře připojení k databázi.

**cursor = conn.cursor()** - Vytvoří kurzor pro provádění SQL příkazů.

# Spojení tabulek pomocí SQL JOIN:
**cursor.execute(""" ... """)**
- SQL dotaz využívá JOIN, aby propojil tři tabulky:
- `Loans` - hlavní tabulka půjček.
- `Books` - spojení přes `Loans.BookID = Books.BookID`.
- `Members` - spojení přes `Loans.MemberID = Members.MemberID`.

**Dotaz vybírá:**
- ID půjčky (LoanID)
- Název knihy (Title)
- Jméno člena (Name)
- Datum výpůjčky (LoanDate)
- Datum vrácení (ReturnDate)

**print("\n📄 Seznam půjček:")** - Vytiskne nadpis sekce.

# Výpis půjček:
**for row in cursor.fetchall():**
- Prochází všechny výsledky dotazu (každý řádek je jedna výpůjčka).

**vraceno = row[4] if row[4] else "NEVRÁCENO"**
- Pokud existuje datum vrácení (`ReturnDate`), uloží ho do proměnné `vraceno`.
- Pokud je hodnota `None` (výpůjčka ještě nebyla vrácena), použije se text "NEVRÁCENO".

**print(...)** - Výpis jedné půjčky ve formátu: `#1: Název knihy - Jméno člena | Vypůjčeno: 2025-05-01 | Vráceno: NEVRÁCENO`

**cursor.close() a conn.close()** - Uzavře kurzor a připojení k databázi.
---

## 🔬 11. Funkce `run_tests()`
- Spustí `test_init.py` pro vytvoření testovací databáze/tabulek. Nabídne spuštění jednotlivých testovacích případů přes `pytest`.
```python
def run_tests():
    # Nejdříve vytvoříme test tabulky
    subprocess.run(["python", "test_init.py"])

    print("\n🔬 Co chceš testovat?")
    print("1 – Přidání knihy")
    print("2 – Přidání člena")
    print("3 – Výpůjčka knihy")
    print("4 – Vrácení knihy")
    print("5 – Spustit vše")
    print("0 – Zpět do menu")

    choice = input("Zadej číslo testu: ")

    tests = {
        "1": "test_library.py::test_add_book",
        "2": "test_library.py::test_add_member",
        "3": "test_library.py::test_loan_book",
        "4": "test_library.py::test_return_book",
        "5": "test_library.py"
    }

    if choice in tests:
        print("\n🧪 Spouštím test...")
        subprocess.run(["pytest", "-v", tests[choice]])
    elif choice == "0":
        return
    else:
        print("⚠️ Neplatná volba.")
```

**subprocess.run(["python", "test_init.py"])** 
- Spustí skript `test_init.py`, který slouží k přípravě databáze nebo vytvoření testovacích tabulek.
- Spouští se pomocí modulu subprocess, který umožňuje volat externí příkazy jako v terminálu.

**Výběr testovacího scénáře:**
- print(...) - Vypíše nabídku testovacích scénářů, které může uživatel spustit.

**choice = input("Zadej číslo testu: ")**
- Načte od uživatele volbu jako textový řetězec (např. "1" nebo "5").

**Slovník `tests`**
```python
tests = {
    "1": "test_library.py::test_add_book",
    "2": "test_library.py::test_add_member",
    "3": "test_library.py::test_loan_book",
    "4": "test_library.py::test_return_book",
    "5": "test_library.py"
}
```
- Obsahuje přiřazení mezi volbou uživatele a konkrétním testem, který se má spustit.
- `::` v názvu říká Pytestu, který konkrétní testovací případ z daného souboru spustit.

# Spuštění testu:
**if choice in tests:**
- Ověří, zda je zadaná volba platná.

**subprocess.run(["pytest", "-v", tests[choice]])**
- Spustí Pytest s parametrem `-v` (verbose), aby byly zobrazeny podrobnosti o prováděných testech.

# Ostatní možnosti:
**elif choice == "0":** - Uživatel se může vrátit do hlavního menu.

**else:** - Zobrazí chybovou hlášku, pokud uživatel zadal neplatné číslo.

---

## 📖 12. Funkce `menu()`
Textové menu pro obsluhu knihovního systému

```python
def menu():
    while True:
        print("\n📖 KNIHOVNÍ MENU")
        print("1. Přidat knihu")
        print("2. Přidat člena")
        print("3. Vypůjčit knihu")
        print("4. Vrátit knihu")
        print("5. Zobrazit knihy")
        print("6. Zobrazit členy")
        print("7. Zobrazit půjčky")
        print("8. 🔬 Spustit testy")
        print("0. Konec")
        volba = input("Zadej volbu: ")

        if volba == "1":
            add_book()
        elif volba == "2":
            add_member()
        elif volba == "3":
            loan_book()
        elif volba == "4":
            return_book()
        elif volba == "5":
            list_books()
        elif volba == "6":
            list_members()
        elif volba == "7":
            list_loans()
        elif volba == "8":
            run_tests()
        elif volba == "0":
            print("👋 Ukončuji program.")
            break
        else:
            print("⚠️ Neplatná volba!")
```
**while True:** - Nekonečná smyčka, která stále zobrazuje menu, dokud uživatel nezvolí konec ("0").

**print(...)** - Vypíše nabídku možností pro uživatele. Každé číslo odpovídá jedné akci systému knihovny.

**volba = input("Zadej volbu: ")** - Načte volbu uživatele jako řetězec.

**Rozhodovací struktura if:**
- Každá volba spouští konkrétní funkci podle zadání:
- "1" → `add_book()` - přidání knihy
- "2" → `add_member()` - přidání člena
- "3" → `loan_book()` - vypůjčení knihy
- "4" → `return_book()` - vrácení knihy
- "5" → `list_books()` - seznam všech knih
- "6" → `list_members()` - seznam členů
- "7" → `list_loans()` - seznam výpůjček
- "8" → `run_tests()` - spuštění testů
- "0" → ukončení programu

**else: print("⚠️ Neplatná volba!")** - Pokud uživatel zadá něco mimo nabízené možnosti, vypíše se upozornění.

---

## 🧷 13. Blok `if __name__ == "__main__":`
```python
if __name__ == "__main__":
    create_tables()
    menu()
```
**if __name__ == "__main__":**
- Tento řádek říká: „Spusť následující kód pouze tehdy, když je tento skript spuštěn přímo (a ne importován jako modul).“
- Díky tomu je možné tento soubor importovat do jiných Python skriptů (například pro testování), aniž by se automaticky spustil celý program.

**create_tables()** 
- Zavolá se funkce, která vytvoří databázové tabulky, pokud ještě neexistují.
- Tím se zajistí, že program nebude padat kvůli chybějící databázi.

**menu()**
- Spustí hlavní ovládací rozhraní aplikace - zobrazí textové menu a umožní uživateli pracovat se systémem knihovny.

---
