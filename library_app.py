# pip install mysql-connector-python

import mysql.connector
import subprocess

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",  # změň podle sebe
        database="LibraryDB"
    )

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

def list_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MemberID, Name, Email FROM Members")
    print("\n👥 Seznam členů:")
    for row in cursor.fetchall():
        print(f"{row[0]} – {row[1]} ({row[2]})")
    cursor.close()
    conn.close()

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

# Navíc
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

if __name__ == "__main__":
    create_tables()
    menu()