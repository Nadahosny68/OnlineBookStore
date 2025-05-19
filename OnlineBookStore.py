import streamlit as st
import re
import json

class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.users = []
        self.load_data()
        if not self.books and not self.users:
            self._load_initial_data() # Load initial data if none exists

    def _load_initial_data(self):
        initial_books = [
            {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "available": True},
            {"title": "Pride and Prejudice", "author": "Jane Austen", "available": True},
            {"title": "1984", "author": "George Orwell", "available": False},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "available": True},
        ]
        initial_users = [
            {"name": "Alice", "borrowed_books": []},
            {"name": "Bob", "borrowed_books": ["1984"]},
            {"name": "Charlie", "borrowed_books": []},
        ]
        for book_data in initial_books:
            self.books.append(Book(**book_data))
        for user_data in initial_users:
            self.users.append(User(**user_data))
        self.save_data()
        st.info("Initial sample data loaded.")

    def add_book(self, book):
        if not isinstance(book, Book):
            st.error("Invalid book object!")
            return
        if not re.match(r'^[a-zA-Z0-9 ]+$', book.title):
            st.error("Book title contains invalid characters!")
            return
        self.books.append(book)
        self.save_data()
        st.success(f"Book '{book.title}' by {book.author} added.")

    def add_user(self, user):
        if not re.match(r'^[a-zA-Z ]+$', user.name):
            st.error("User name contains invalid characters.")
            return
        self.users.append(user)
        self.save_data()
        st.success(f"User '{user.name}' registered.")

    def borrow_book(self, user_name, book_title):
        user = next((u for u in self.users if u.name == user_name), None)
        book = next((b for b in self.books if b.title == book_title and b.available), None)

        if not user:
            st.error("User not found.")
            return
        if not book:
            st.error("Book not available.")
            return

        book.available = False
        user.borrowed_books.append(book.title)
        self.save_data()
        st.info(f"'{book.title}' borrowed by {user.name}.")

    def return_book(self, user_name, book_title):
        user = next((u for u in self.users if u.name == user_name), None)
        book = next((b for b in self.books if b.title == book_title), None)

        if not user or book_title not in user.borrowed_books:
            st.error("User or book not found.")
            return

        book.available = True
        user.borrowed_books.remove(book.title)
        self.save_data()
        st.info(f"'{book.title}' returned by {user.name}.")

    def search_books(self, keyword):
        found_books = [book for book in self.books if keyword.lower() in book.title.lower()]
        if found_books:
            st.subheader("Found Books:")
            for book in found_books:
                book.display_info()
        else:
            st.info("No books found.")

    def search_users(self, keyword):
        found_users = [u for u in self.users if keyword.lower() in u.name.lower()]
        if found_users:
            st.subheader("Matching Users:")
            for user in found_users:
                user.display_user_info()
        else:
            st.info("No users found.")

    def list_books(self):
        st.subheader("Library Books:")
        if self.books:
            for book in self.books:
                book.display_info()
        else:
            st.info("The library has no books.")

    def list_users(self):
        st.subheader("Registered Users:")
        if self.users:
            for user in self.users:
                user.display_user_info()
        else:
            st.info("No users are registered.")

    def save_data(self):
        data = {
            "books": [{"title": b.title, "author": b.author, "available": b.available} for b in self.books],
            "users": [{"name": u.name, "borrowed_books": u.borrowed_books} for u in self.users]
        }
        with open("library_data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open("library_data.json", "r") as f:
                data = json.load(f)
                self.books = [Book(b["title"], b["author"], b["available"]) for b in data["books"]]
                self.users = [User(u["name"], u["borrowed_books"]) for u in data["users"]]
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            st.error("Error decoding library_data.json. Starting with an empty library.")
            self.books = []
            self.users = []

class Book:
    def __init__(self, title, author, available=True):
        self.title = title
        self.author = author
        self.available = available

    def display_info(self):
        """Display book details with formatting."""
        status = "✅ Available" if self.available else "❌ Borrowed"
        st.write(f"{self.title:<30} | {self.author:<20} | {status}")

class User:
    def __init__(self, name, borrowed_books=None):
        self.name = name
        self.borrowed_books = borrowed_books if borrowed_books else []

    def display_user_info(self):
        """Display user details with borrowed books."""
        borrowed = ", ".join(self.borrowed_books) if self.borrowed_books else "None"
        st.write(f"{self.name:<20} | Borrowed Books: {borrowed}")

library_app = Library("City Library")

st.title("📚 Library Management System")

menu = ["Add Book", "Register User", "Borrow Book", "Return Book", "Search Books", "Search Users", "List Books", "List Users"]
choice = st.sidebar.selectbox("Select an action", menu)

if choice == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Title:")
    author = st.text_input("Author:")
    if st.button("Add"):
        if title and author:
            library_app.add_book(Book(title, author))
        else:
            st.warning("Please enter both title and author.")

elif choice == "Register User":
    st.subheader("Register a New User")
    name = st.text_input("User Name:")
    if st.button("Register"):
        if name:
            library_app.add_user(User(name))
        else:
            st.warning("Please enter a user name.")

elif choice == "Borrow Book":
    st.subheader("Borrow a Book")
    user_name = st.text_input("User Name:")
    book_title = st.text_input("Book Title:")
    if st.button("Borrow"):
        if user_name and book_title:
            library_app.borrow_book(user_name, book_title)
        else:
            st.warning("Please enter both user name and book title.")

elif choice == "Return Book":
    st.subheader("Return a Book")
    user_name = st.text_input("User Name:")
    book_title = st.text_input("Book Title:")
    if st.button("Return"):
        if user_name and book_title:
            library_app.return_book(user_name, book_title)
        else:
            st.warning("Please enter both user name and book title.")

elif choice == "Search Books":
    st.subheader("Search Books")
    keyword = st.text_input("Enter keyword:")
    if st.button("Search"):
        if keyword:
            library_app.search_books(keyword)
        else:
            st.warning("Please enter a keyword to search.")

elif choice == "Search Users":
    st.subheader("Search Users")
    keyword = st.text_input("Enter keyword:")
    if st.button("Search"):
        if keyword:
            library_app.search_users(keyword)
        else:
            st.warning("Please enter a keyword to search.")

elif choice == "List Books":
    library_app.list_books()

elif choice == "List Users":
    library_app.list_users()
