from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QLineEdit, QFormLayout, QCheckBox, QInputDialog
from repo import BookRepository
from book import Book

class BookshelfGUI(QWidget):
    def __init__(self, repo: BookRepository):
        # Get access to sibling class methods
        super().__init__()
        self.repo = repo # define repository for the class as global variable

        # Set title for the GUI and the geometry
        self.setWindowTitle("Bookshelf")
        self.setGeometry(200,200,900,640)

        # Set the widgets vertically 
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Creates a scrollable list of books as a blank screen on the GUI
        self.book_list = QListWidget()
        self.layout.addWidget(self.book_list)

        # Create layout for the book items and asks for input for book attributes
        self.form_layout = QFormLayout()
        self.title_input = QLineEdit()  # Asks for title in the main screen
        self.author_input = QLineEdit() # Asks for author in the main screen
        self.pages_input = QLineEdit()  # Asks for page count in the main screen
        self.genre_input = QLineEdit()  # Asks for genre in the main screen

        # Set the type spaces on the GUI atop each other
        self.form_layout.addRow("Title", self.title_input)
        self.form_layout.addRow("Author", self.author_input)
        self.form_layout.addRow("Pages", self.pages_input)
        self.form_layout.addRow("Genre", self.genre_input)
        self.layout.addLayout(self.form_layout)

        # Crete a button to refresh the book list
        self.refresh_button = QPushButton("Refresh List")
        self.refresh_button.clicked.connect(self.load_books)
        self.layout.addWidget(self.refresh_button)

        # Create a button for adding book
        self.add_button = QPushButton("Add Book")
        self.add_button.clicked.connect(self.add_book)
        self.layout.addWidget(self.add_button)
        
        # Create a button for marking book as read
        self.mark_read_button = QPushButton("Mark as Read")
        self.mark_read_button.clicked.connect(self.mark_selected_read)
        self.layout.addWidget(self.mark_read_button)

        # Button for deleting books
        self.delete_book_button = QPushButton("Delete Book")
        self.delete_book_button.clicked.connect(self.delete_selected_book)
        self.layout.addWidget(self.delete_book_button)

        # Checkbox for marking book as either owned or not owned
        self.owned_checkbox = QCheckBox("Yes/No")
        self.owned_checkbox.setChecked(True)
        self.form_layout.addRow("Owned", self.owned_checkbox)

        # Update progress button
        self.progress_button = QPushButton("Update Progress")
        self.progress_button.clicked.connect(self.update_progress)
        self.layout.addWidget(self.progress_button)

        # Search function variables
        # Search by title
        self.search_title = QLineEdit()
        self.search_title.setPlaceholderText("Search by title")

        # Search by author
        self.search_author = QLineEdit()
        self.search_author.setPlaceholderText("Search by author")

        # Search by genre
        self.search_genre = QLineEdit()
        self.search_genre.setPlaceholderText("Search by genre")

        # Reaload the list whenever user types
        self.search_title.textChanged.connect(self.load_books)
        self.search_author.textChanged.connect(self.load_books)
        self.search_genre.textChanged.connect(self.load_books)

        # Search layout
        self.search_layout = QFormLayout()
        self.search_layout.addRow("Title:", self.search_title)
        self.search_layout.addRow("Author:", self.search_author)
        self.search_layout.addRow("Genre:", self.search_genre)

        self.layout.addLayout(self.search_layout)

        # Creates a stats display at the bottom of GUI
        self.stats_label = QLabel()
        self.layout.addWidget(self.stats_label)

    # Fetch all books from the repository and create a list for them als oupadting the stats label
    def load_books(self):
        
        # Start with a clear screen
        self.book_list.clear()

        # Fetch books from repository
        books = self.repo.get_all_books()
        
        # Case insesitive search filters
        title_filter = self.search_title.text().lower()
        author_filter = self.search_author.text().lower()
        genre_filter = self.search_genre.text().lower()

        # Filter books to a global list for searching
        self.filtered_books = [
            b for b in books
            if title_filter in b.title.lower() and
                author_filter in b.author.lower() and
                genre_filter in b.genre.lower()
        ]

        # Adds filtered books to the book list space
        for book in self.filtered_books:
            self.book_list.addItem(str(book))

        # Updates stats after every loading
        self.update_stats()

    # Adds a new book object to the repo and reloads the GUI and stats
    def add_book(self):
        
        # Define checked box as owned variable
        owned = self.owned_checkbox.isChecked()

        # Define inputs as either text or integer
        title = self.title_input.text()
        author = self.author_input.text()
        pages = int(self.pages_input.text())
        genre = self.genre_input.text()

        # Create a new book object according to the user inputs
        new_book = Book(title=title, author=author, pages=pages, genre=genre, owned=owned)

        # Add new book to the repostiory and update the book list
        self.repo.add_book(new_book)
        self.load_books()
        self.update_stats()

    # Updates reading progress
    def update_progress(self):

        # If no book in the book list return
        selected = self.book_list.selectedItems()
        if not selected:
            return
        
        # Select book by index
        index = self.book_list.row(selected[0])
        book = self.repo.get_all_books()[index]

        # Fetch selected books page values
        page, ok = QInputDialog.getInt(
            self, "Progress", "Current Page:", book.current_page, 0, book.pages
        )

        # Updates the current page as the page and set min and max
        if ok:
            book.current_page = page

            # Changes status to reading if the book is unread and is updated
            if page > 0 and book.status == "UNREAD":
                book.status = "READING"
        
        # Update repository and load the books list
        self.repo.update(book)
        self.load_books()

    # Gets the selceted item from repo by index and marks it as read
    def mark_selected_read(self):
        selected = self.book_list.selectedItems()
        
        # If book list is empty return
        if not selected:
            return

        # Same logic as with updating progress
        index = self.book_list.row(selected[0])
        book = self.repo.get_all_books()[index]

        # Set set rating and set min and max values
        rating, ok = QInputDialog.getInt(
            self, "Rating", "Rating (1-10):",10, 1, 10
        )

        # Gives read book a rating
        if ok:
            book.mark_read(rating=rating)

            # Updates selected book and load the list again for selected book
            self.repo.update(book)
            self.load_books()

    # Gets selected item from repo by index and deletes it from the database
    def delete_selected_book(self):
        selected = self.book_list.selectedItems()
        if not selected:
            return

        index = self.book_list.row(selected[0])
        book = self.repo.get_all_books()[index]

        # Delete selected book from the the repo and updates the book list
        self.repo.delete_book(book.id)
        self.load_books()

    # Fetches stats from the repository and converts tem to string
    def update_stats(self, books=None):

        # If no books in book list leaves the stats space empty
        if books is None:
            books = self.filtered_books if hasattr(self, "filtered_books") else []

        # Fetch stats from repo
        stats = self.repo.get_stats()

        # Format the average rating
        avg = stats["average_rating"]
        avg_text = f"{avg:.2f}" if avg else "N/A"

        # Format how the stats are shown
        self.stats_label.setText(
            f"Total: {stats['total_books']} |"
            f"Read: {stats['finished']} | "
            f"Pages Read: {stats['pages_read']} | "
            f"Avg Rating: {avg_text}"
        )



# Displays the main window and starts the event loop 
def run_gui(repo):
    app = QApplication([])
    window = BookshelfGUI(repo)
    window.show()
    app.exec()