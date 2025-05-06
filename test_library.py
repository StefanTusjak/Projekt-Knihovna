import mysql.connector
import pytest
from test_init import create_test_tables  # ⬅️ importujeme funkci pro vytvoření tabulek


# 🔧 Fixture, která vytvoří tabulky před testy
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    create_test_tables()


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
