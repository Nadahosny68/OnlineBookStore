# My Awesome Library App

## App Link: https://onlinebookstore.streamlit.app/ 

This is a Streamlit web application for managing a simple library system. Users can browse available books, register, borrow, return, search for books and users, and even reserve books that are currently unavailable. Administrators have a separate login to potentially manage the system (though more admin features can be added).

## Features

* **Add Book:** Admins can add new books to the library with a title and author (and optionally a genre).
* **Register User:** Users can register with their name.
* **Borrow Book:** Registered users can borrow available books.
* **Return Book:** Users can return borrowed books.
* **Search Books:** Search for books by title, author, or genre.
* **Search Users:** Search for registered users by name.
* **List Books:** View all books in the library, with options to filter by genre and sort by title or author. Details like author and genre are expandable.
* **List Users:** View all registered users and the books they have borrowed.
* **Book Reservation:** If a book is currently borrowed, users can reserve it. A basic notification appears when a reserved book is returned.
* **User Profiles:** Users can select their name to see the books they have currently borrowed and their reservations.
* **Admin Login:** A simple password-protected admin login in the sidebar. (More admin features can be implemented).


## How to Use the App

1.  **Sidebar Navigation:** Use the sidebar on the left to select different actions like "Add Book," "Borrow Book," "List Books," etc.

2.  **User Selection:** In the sidebar, select your name from the "View Profile/Borrow As:" dropdown to act as that user for borrowing and returning books, and to view your reservations.

3.  **Admin Login:** If you know the admin password ("admin123"), enter it in the "Admin Password" field in the sidebar to access potential admin features.

4.  **Adding Books:** Select "Add Book," enter the title and author (and optionally the genre), and click "Add."

5.  **Registering Users:** Select "Register User," enter your name, and click "Register."

6.  **Borrowing Books:** Select "Borrow Book," enter the title of the book you want to borrow, and click "Borrow." Make sure you have selected your user in the sidebar.

7.  **Returning Books:** Select "Return Book," enter the title of the book you are returning, and click "Return." Make sure you have selected your user in the sidebar.

8.  **Searching:** Use the "Search Books" and "Search Users" options to find specific items.

9.  **Listing Books:** Select "List Books" to see all books. Use the filter and sort options at the top to refine the list. Click the expander next to a book to see more details and a "Reserve" button if it's borrowed.

10. **Viewing Reservations:** Select your user in the sidebar and click "View My Reservations" to see the books you have reserved.

## Data Storage

The application uses a JSON file (`library_data.json`) in the same directory to persist the library's data (books, users, and reservations).

## Potential Future Enhancements

* **More Robust Admin Features:** User removal, bulk book addition, etc.
* **User Authentication:** More secure user login system.
* **Detailed Book Information:** ISBN, publication year, descriptions.
* **Advanced Reservation System:** Queue management, notifications when books become available.
* **Borrowing History:** Track user borrowing history.
* **UI/UX Improvements:** More visually appealing design, better feedback mechanisms.
* **Error Handling:** More comprehensive error handling and user-friendly messages.

## Contributing

Feel free to contribute to this project by suggesting improvements or submitting pull requests.
