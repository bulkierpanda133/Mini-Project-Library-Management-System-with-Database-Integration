import mysql.connector

# MySQL Connection Function
def sql_connector():
    return mysql.connector.connect(
        host="localhost",  # Replace with your MySQL host
        user="your_username",  # Replace with your MySQL username
        password="your_password",  # Replace with your MySQL password
        database="library_management"  # Replace with your database name
    )

# Main Menu
def main_menu():
    while True:
        print("**** Welcome to the Library Management System! ****")
        print("1. Book Operations")
        print("2. User Operations")
        print("3. Author Operations")
        print("4. Quit")
        
        choice = input("Select an option: ")
        
        if choice == "1":
            book_operations()
        elif choice == "2":
            user_operations()
        elif choice == "3":
            author_operations()
        elif choice == "4":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Book Operations Menu
def book_operations():
    print("Book Operations:")
    print("1. Add a new book")
    print("2. Borrow a book")
    print("3. Return a book")
    print("4. Search for a book")
    print("5. Display all books")

    choice = input("Select an option: ")
    
    if choice == "1":
        add_book()
    elif choice == "2":
        user_id = int(input("Enter your user ID: "))
        book_id = int(input("Enter the book ID to borrow: "))
        borrow_book(user_id, book_id)
    elif choice == "3":
        book_id = int(input("Enter the book ID to return: "))
        return_book(book_id)
    elif choice == "4":
        search_book()
    elif choice == "5":
        display_all_books()

# User Operations Menu
def user_operations():
    print("User Operations:")
    print("1. Add a new user")
    print("2. View user details")
    print("3. Display all users")

    choice = input("Select an option: ")
    
    if choice == "1":
        add_user()
    elif choice == "2":
        user_id = int(input("Enter the user ID: "))
        view_user_details(user_id)
    elif choice == "3":
        display_all_users()

# Author Operations Menu
def author_operations():
    print("Author Operations:")
    print("1. Add a new author")
    print("2. View author details")
    print("3. Display all authors")

    choice = input("Select an option: ")
    
    if choice == "1":
        add_author()
    elif choice == "2":
        author_id = int(input("Enter the author ID: "))
        view_author_details(author_id)
    elif choice == "3":
        display_all_authors()

# Add a New Book
def add_book():
    title = input("Enter book title: ")
    author_id = int(input("Enter author ID: "))
    isbn = input("Enter ISBN: ")
    publication_date = input("Enter publication date (YYYY-MM-DD): ")

    try:
        conn = sql_connector()
        cursor = conn.cursor()
        query = """INSERT INTO books (title, author_id, isbn, publication_date) 
                   VALUES (%s, %s, %s, %s)"""
        cursor.execute(query, (title, author_id, isbn, publication_date))
        conn.commit()
        print("Book added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Borrow a Book
def borrow_book(user_id, book_id):
    try:
        conn = sql_connector()
        cursor = conn.cursor()

        cursor.execute("SELECT availability FROM books WHERE id = %s", (book_id,))
        available = cursor.fetchone()[0]
        
        if available:
            query = """INSERT INTO borrowed_books (user_id, book_id, borrow_date) 
                       VALUES (%s, %s, CURDATE())"""
            cursor.execute(query, (user_id, book_id))
            cursor.execute("UPDATE books SET availability = 0 WHERE id = %s", (book_id,))
            conn.commit()
            print("Book borrowed successfully!")
        else:
            print("The book is not available.")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Return a Book
def return_book(book_id):
    try:
        conn = sql_connector()
        cursor = conn.cursor()

        query = "UPDATE borrowed_books SET return_date = CURDATE() WHERE book_id = %s AND return_date IS NULL"
        cursor.execute(query, (book_id,))
        
        cursor.execute("UPDATE books SET availability = 1 WHERE id = %s", (book_id,))
        conn.commit()
        print("Book returned successfully!")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Search for a Book by Title
def search_book():
    title = input("Enter book title to search: ")
    
    try:
        conn = sql_connector()
        cursor = conn.cursor()
        
        query = "SELECT * FROM books WHERE title LIKE %s"
        cursor.execute(query, ('%' + title + '%',))
        result = cursor.fetchall()
        
        for book in result:
            print(f"ID: {book[0]}, Title: {book[1]}, ISBN: {book[3]}, Available: {'Yes' if book[5] else 'No'}")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Display All Books
def display_all_books():
    try:
        conn = sql_connector()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM books")
        result = cursor.fetchall()
        
        for book in result:
            print(f"ID: {book[0]}, Title: {book[1]}, Author ID: {book[2]}, ISBN: {book[3]}, Available: {'Yes' if book[5] else 'No'}")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Add a New User
def add_user():
    name = input("Enter user name: ")
    library_id = input("Enter library ID: ")

    try:
        conn = sql_connector()
        cursor = conn.cursor()
        query = "INSERT INTO users (name, library_id) VALUES (%s, %s)"
        cursor.execute(query, (name, library_id))
        conn.commit()
        print("User added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# View User Details
def view_user_details(user_id):
    try:
        conn = sql_connector()
        cursor = conn.cursor()

        query = "SELECT * FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()

        if user:
            print(f"User ID: {user[0]}, Name: {user[1]}, Library ID: {user[2]}")
        else:
            print("User not found.")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Display All Users
def display_all_users():
    try:
        conn = sql_connector()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users")
        result = cursor.fetchall()
        
        for user in result:
            print(f"ID: {user[0]}, Name: {user[1]}, Library ID: {user[2]}")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Add a New Author
def add_author():
    name = input("Enter author name: ")
    biography = input("Enter biography: ")

    try:
        conn = sql_connector()
        cursor = conn.cursor()
        query = "INSERT INTO authors (name, biography) VALUES (%s, %s)"
        cursor.execute(query, (name, biography))
        conn.commit()
        print("Author added successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# View Author Details
def view_author_details(author_id):
    try:
        conn = sql_connector()
        cursor = conn.cursor()

        query = "SELECT * FROM authors WHERE id = %s"
        cursor.execute(query, (author_id,))
        author = cursor.fetchone()

        if author:
            print(f"Author ID: {author[0]}, Name: {author[1]}, Biography: {author[2]}")
        else:
            print("Author not found.")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Display All Authors
def display_all_authors():
    try:
        conn = sql_connector()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM authors")
        result = cursor.fetchall()
        
        for author in result:
            print(f"ID: {author[0]}, Name: {author[1]}, Biography: {author[2]}")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Start the system
if __name__ == "__main__":
    main_menu()


