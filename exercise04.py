import sqlite3

# Connect to the database
conn = sqlite3.connect('library.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS Books 
             (BookID TEXT PRIMARY KEY, Title TEXT, Author TEXT, ISBN TEXT, Status TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Users 
             (UserID TEXT PRIMARY KEY, Name TEXT, Email TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS Reservations 
             (ReservationID INTEGER PRIMARY KEY AUTOINCREMENT, BookID TEXT, UserID TEXT, ReservationDate TEXT,
             FOREIGN KEY(BookID) REFERENCES Books(BookID),
             FOREIGN KEY(UserID) REFERENCES Users(UserID))''')


# Function to add a new book to the database
def add_book():
    book_id = input("Enter Book ID: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    isbn = input("Enter ISBN: ")
    status = input("Enter Status: ")

    c.execute("INSERT INTO Books (BookID, Title, Author, ISBN, Status) VALUES (?, ?, ?, ?, ?)",
              (book_id, title, author, isbn, status))
    conn.commit()
    print("Book added successfully!")


# Function to find a book's detail based on BookID
def find_book(book_id):
    c.execute(
        "SELECT Books.*, Users.Name, Users.Email FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID LEFT JOIN Users ON Reservations.UserID = Users.UserID WHERE Books.BookID=?",
        (book_id,))
    result = c.fetchone()
    if result:
        print("BookID:", result[0])
        print("Title:", result[1])
        print("Author:", result[2])
        print("ISBN:", result[3])
        print("Status:", result[4])
        if result[5]:
            print("Reserved by:", result[5])
            print("User Name:", result[6])
            print("User Email:", result[7])
    else:
        print("Book not found!")


# Function to find a book's reservation status based on BookID, Title, UserID, and ReservationID
def find_reservation(identifier):
    c.execute(
        "SELECT Books.Title, Books.Status, Users.Name, Users.Email FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID LEFT JOIN Users ON Reservations.UserID = Users.UserID WHERE Books.BookID=? OR Books.Title LIKE ? OR Users.UserID=? OR CAST(Reservations.ReservationID AS TEXT)=?",
        (identifier, '%' + identifier + '%', identifier, identifier))
    result = c.fetchone()
    if result:
        print("Title:", result[0])
        print("Status:", result[1])
        print("User Name:", result[2])
        print("User Email:", result[3])
    else:
        print("Book or reservation not found!")


# Function to find all the books in the database
def find_all_books():
    c.execute(
        "SELECT Books.*, Users.Name, Users.Email FROM Books LEFT JOIN Reservations ON Books.BookID = Reservations.BookID LEFT JOIN Users ON Reservations.UserID = Users.UserID")
    results = c.fetchall()
    if results:
        for result in results:
            print("BookID:", result[0])
            print("Title:", result[1])
            print("Author:", result[2])
            print("ISBN:", result[3])
            print("Status:", result[4])
            if result[5]:
                print("Reserved by:", result[5])
                print("User Name:", result[6])
                print("User Email:", result[7])
            print("-------------------------")
    else:
        print("No books found!")


# Function to modify/update book details based on its BookID
def modify_book(book_id):
    status = input("Enter new status: ")

    c.execute("UPDATE Books SET Status=? WHERE BookID=?", (status, book_id))
    c.execute("UPDATE Reservations SET ReservationDate=NULL WHERE BookID=?", (book_id,))
    conn.commit()
    print("Book details updated successfully!")


# Function to delete a book based on its BookID
def delete_book(book_id):
    c.execute("DELETE FROM Books WHERE BookID=?", (book_id,))
    c.execute("DELETE FROM Reservations WHERE BookID=?", (book_id,))
    conn.commit()
    print("Book deleted successfully!")


# Main program loop
while True:
    print("Library Management System")
    print("-------------------------")
    print("1. Add a new book")
    print("2. Find a book's detail")
    print("3. Find a book's reservation status")
    print("4. Find all the books")
    print("5. Modify/Update book details")
    print("6. Delete a book")
    print("7. Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == '1':  # Add a new book
        add_book()
    elif choice == '2':  # Find a book's detail
        book_id = input("Enter Book ID: ")
        find_book(book_id)
    elif choice == '3':  # Find a book's reservation status
        identifier = input("Enter Book ID, Title, UserID, or ReservationID: ")
        find_reservation(identifier)
    elif choice == '4':  # Find all the books
        find_all_books()
    elif choice == '5':  # Modify/Update book details
        book_id = input("Enter Book ID: ")
        modify_book(book_id)
    elif choice == '6':  # Delete a book
        book_id = input("Enter Book ID: ")
        delete_book(book_id)
    elif choice == '7':  # Exit
        break
    else:
        print("Invalid choice! Please try again.")

conn.close()
