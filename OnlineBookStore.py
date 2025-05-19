import streamlit as st
import re
import json

ADMIN_PASSWORD = "admin123"

class Library:
    def __init__(self, name):
        self.name = name
        self.books = []
        self.users = []
        self.reservations = []
        self.load_data()
        if not self.books and not self.users:
            self._load_initial_data()

    def _load_initial_data(self):
        initial_books = [
            {"title": "The Hitchhiker's Guide to the Galaxy", "author": "Douglas Adams", "available": True, "genre": "Science Fiction"},
            {"title": "Pride and Prejudice", "author": "Jane Austen", "available": True, "genre": "Romance"},
            {"title": "1984", "author": "George Orwell", "available": False, "genre": "Dystopian"},
            {"title": "To Kill a Mockingbird", "author": "Harper Lee", "available": True, "genre": "Fiction"},
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
        # Check for reservations
        if book.title in [res["book_title"] for res in self.reservations if res["available"]]:
            reserved_user = next((res["user_name"] for res in self.reservations if res["book_title"] == book.title and res["available"]), None)
            st.info(f"'{book.title}' returned by {user.name}. '{reserved_user}' has a reservation.")
            # In a real system, you'd notify the reserved user
            self.reservations = [res for res in self.reservations if not (res["book_title"] == book.title and res["user_name"] == reserved_user and res["available"])] # Remove fulfilled reservation
        else:
            st.info(f"'{book.title}' returned by {user.name}.")
        self.save_data()

    def search_books(self, keyword):
        found_books = [book for book in self.books if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower() or (book.genre and keyword.lower() in book.genre.lower())]
        if found_books:
            st.subheader("Found Books:")
            for book in found_books:
                book.display_info(show_details_button=True)
        else:
            st.info("No books found matching your search.")

    def search_users(self, keyword):
        found_users = [u for u in self.users if keyword.lower() in u.name.lower()]
        if found_users:
            st.subheader("Matching Users:")
            for user in found_users:
                user.display_user_info()
        else:
            st.info("No users found matching your search.")

    def list_books(self, genre_filter="All Genres", sort_by="Title"):
        st.subheader("Library Books:")
        filtered_books = self.books
        if genre_filter != "All Genres":
            filtered_books = [book for book in filtered_books if book.genre == genre_filter]

        if sort_by == "Title":
            filtered_books.sort(key=lambda book: book.title)
        elif sort_by == "Author":
            filtered_books.sort(key=lambda book: book.author)

        if filtered_books:
            for book in filtered_books:
                book.display_info(show_details_button=True)
        else:
            st.info("No books to show based on the current filters.")

    def list_users(self):
        st.subheader("Registered Users:")
        if self.users:
            for user in self.users:
                user.display_user_info()
        else:
            st.info("No users are registered.")

    def reserve_book(self, user_name, book_title):
        book = next((b for b in self.books if b.title == book_title and not b.available), None)
        user_exists = any(u.name == user_name for u in self.users)

        if not user_exists:
            st.error("User not found.")
            return
        if not book:
            st.error("Book is currently available or does not exist.")
            return
        if any(res["user_name"] == user_name and res["book_title"] == book_title for res in self.reservations):
            st.warning(f"'{user_name}' has already reserved '{book_title}'.")
            return

        self.reservations.append({"user_name": user_name, "book_title": book_title, "available": False})
        self.save_data()
        st.info(f"'{book_title}' reserved by '{user_name}'.")

    def view_reservations(self, user_name):
        user_reservations = [res for res in self.reservations if res["user_name"] == user_name]
        if user_reservations:
            st.subheader(f"Your Reservations ({user_name}):")
            for res in user_reservations:
                st.write(f"- {res['book_title']} (Waiting)")
        else:
            st.info("You have no current reservations.")

    def save_data(self):
        data = {
            "books": [{"title": b.title, "author": b.author, "available": b.available, "genre": b.genre} for b in self.books],
            "users": [{"name": u.name, "borrowed_books": u.borrowed_books} for u in self.users],
            "reservations": self.reservations,
        }
        with open("library_data.json", "w") as f:
            json.dump(data, f)

    def load_data(self):
        try:
            with open("library_data.json", "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data.get("books", [])]
                self.users = [User(**u) for u in data.get("users", [])]
                self.reservations = data.get("reservations", [])
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            st.error("Error decoding library_data.json. Starting with an empty library.")
            self.books = []
            self.users = []
            self.reservations = []

class Book:
    def __init__(self, title, author, available=True, genre=None):
        self.title = title
        self.author = author
        self.available = available
        self.genre = genre

    def display_info(self, show_details_button=False):
        status = "✅ Available" if self.available else "❌ Borrowed"
        st.write(f"{self.title:<30} | {self.author:<20} | {status} | Genre: {self.genre or 'N/A'}")
        if show_details_button:
            with st.expander(f"Details for '{self.title}'"):
                st.write(f"**Author:** {self.author}")
                st.write(f"**Genre:** {self.genre or 'N/A'}")
                st.write(f"**Status:** {status}")
                if not self.available:
                    borrow_options = [user.name for user in library_app.users if self.title not in user.borrowed_books]
                    if borrow_options and st.session_state.get("current_user") and self.title not in [res["book_title"] for res in library_app.reservations if res["user_name"] == st.session_state["current_user"]]:
                        if st.button(f"Reserve '{self.title}'", key=f"reserve_{self.title}"):
                            library_app.reserve_book(st.session_state["current_user"], self.title)
                            st.rerun() # Refresh to update UI

class User:
    def __init__(self, name, borrowed_books=None):
        self.name = name
        self.borrowed_books = borrowed_books if borrowed_books else []

    def display_user_info(self):
        borrowed = ", ".join(self.borrowed_books) if self.borrowed_books else "None"
        st.write(f"{self.name:<20} | Borrowed Books: {borrowed}")

st.title("📚 My Awesome Library")

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

with st.sidebar:
    admin_password = st.text_input("Admin Password:", type="password")
    if admin_password == ADMIN_PASSWORD:
        st.session_state["is_admin"] = True
        st.success("Admin logged in!")
    else:
        st.session_state["is_admin"] = False

    user_names = ["Select User"] + [user.name for user in library_app.users]
    st.session_state["current_user"] = st.selectbox("View Profile/Borrow As:", user_names)
    if st.session_state["current_user"] != "Select User":
        if st.button("View My Reservations"):
            library_app.view_reservations(st.session_state["current_user"])

menu = ["Add Book", "Register User", "Borrow Book", "Return Book", "Search Books", "List Books", "List Users"]
if st.session_state["is_admin"]:
    menu.insert(0, "Admin Panel")
choice = st.sidebar.selectbox("Select an action", menu)

if choice == "Admin Panel" and st.session_state["is_admin"]:
    st.subheader("Admin Control")
    # Add more admin functionalities here if needed

elif choice == "Add Book":
    st.subheader("Add a New Book")
    col1, col2, col3 = st.columns(3)
    title = col1.text_input("Title:")
    author = col2.text_input("Author:")
    genre = col3.text_input("Genre (optional):")
    if st.button("Add"):
        if title and author:
            library_app.add_book(Book(title, author, genre=genre))
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
    if st.session_state["current_user"] == "Select User":
        st.warning("Please select a user in the sidebar to borrow.")
    else:
        book_title = st.text_input("Book Title to Borrow:")
        if st.button("Borrow"):
            if book_title:
                library_app.borrow_book(st.session_state["current_user"], book_title)
            else:
                st.warning("Please enter the book title.")

elif choice == "Return Book":
    st.subheader("Return a Book")
    if st.session_state["current_user"] == "Select User":
        st.warning("Please select a user in the sidebar to return.")
    else:
        book_title = st.text_input("Book Title to Return:")
        if st.button("Return"):
            if book_title:
                library_app.return_book(st.session_state["current_user"], book_title)
            else:
                st.warning("Please enter the book title.")

elif choice == "Search Books":
    st.subheader("Search Books")
    keyword = st.text_input("Enter keyword (title, author, or genre):")
    if st.button("Search"):
        if keyword:
            library_app.search_books(keyword)
        else:
            st.warning("Please enter a keyword to search.")

elif choice == "List Books":
    st.subheader("List Books")
    col1, col2 = st.columns(2)
    genres = ["All Genres"] + sorted(list(set(book.genre for book in library_app.books if book.genre)))
    genre_filter = col1.selectbox("Filter by Genre:", genres)
    sort_options = ["Title", "Author"]
    sort_by = col2.selectbox("Sort by:", sort_options)
    library_app.list_books(genre_filter=genre_filter, sort_by=sort_by)

elif choice == "List Users":
    library_app.list_users()
