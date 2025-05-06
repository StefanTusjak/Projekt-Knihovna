import mysql.connector

def create_test_tables():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1111",
        database="LibraryDB_test"
    )
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Loans")
    cursor.execute("DROP TABLE IF EXISTS Books")
    cursor.execute("DROP TABLE IF EXISTS Members")

    cursor.execute("""
    CREATE TABLE Books (
        BookID INT PRIMARY KEY AUTO_INCREMENT,
        Title VARCHAR(255) NOT NULL,
        Author VARCHAR(255) NOT NULL,
        Available BOOLEAN DEFAULT TRUE
    )
    """)
    cursor.execute("""
    CREATE TABLE Members (
        MemberID INT PRIMARY KEY AUTO_INCREMENT,
        Name VARCHAR(255) NOT NULL,
        Email VARCHAR(255) UNIQUE NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE Loans (
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
    print("✅ Testovací tabulky byly vytvořeny.")


if __name__ == "__main__":
    create_test_tables()
