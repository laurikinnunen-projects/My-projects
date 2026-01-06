# Imports
import sqlite3
import os
from book import Book
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_PATH = BASE_DIR / "schema.sql"

# Repository object that connects the sql schemas database with the python script
class BookRepository:

    # Initialize the database using sqlite3
    def __init__(self, db_path='library.db'):
        self.db_path = Path(db_path).resolve()

        # For debugging only, comment out for actual usage !!!
        # self._reset_database()

        # Initialize the sql connection and Cursor
        self.connect = sqlite3.connect(db_path) # Connect to the on-disk database or create one if doesnt exist
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()
        self._initialize_database()

    # debugging method to run test databases and reset it after each run
    def _reset_database(self):
        if self.db_path.exists():
            os.remove(self.db_path)
            print(f"Deleted old database: {self.db_path}")

    # Opens the sql schema file 
    def _initialize_database(self):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            self.cursor.executescript(f.read())
        self.connect.commit()
    
    # Convert rows from the schema to Book objects
    def _row_to_book(self, row):
        return Book(
            id = row["id"],
            title = row["title"],
            author = row["author"],
            pages = row["pages"],
            genre = row["genre"],
            status = row["status"],
            current_page = row["current_page"],
            date_added = row["date_added"],
            date_finished = row["date_finished"],
            owned = bool(row["owned"]),
            rating = row["rating"])
    
    # Add a book to the database
    def add_book(self, book):
        owned = 1 if book.owned else 0
        # Insert in to database a book with the given attribute inputs
        self.cursor.execute("""
                            INSERT INTO books (
                            title, author, pages, current_page, status,
                            genre, owned, date_added, date_finished, rating)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (
                                  book.title,
                                  book.author,
                                  book.pages,
                                  book.current_page,
                                  book.status,
                                  book.genre,
                                  owned,
                                  book.date_added,
                                  book.date_finished,
                                  book.rating
                            ))
        self.connect.commit()
        book.id =self.cursor.lastrowid

    # Return all books from the database
    def get_all_books(self):

        # Select all books from the table
        self.cursor.execute("SELECT * FROM books")
        rows = self.cursor.fetchall()
        return [self._row_to_book(row) for row in rows]
    
    # Update existing information 
    def update(self, book):
        owned = 1 if book.owned else 0

        # Update the table with the given inputs
        self.cursor.execute("""
                            UPDATE books
                            SET
                                title = ?,
                                author = ?,
                                pages = ?,
                                current_page = ?,
                                status = ?,
                                genre = ?,
                                owned = ?,
                                date_added = ?,
                                date_finished = ?,
                                rating = ?
                            WHERE id = ?""",
                            (
                                book.title,
                                book.author,
                                book.pages,
                                book.current_page,
                                book.status,
                                book.genre,
                                owned,
                                book.date_added,
                                book.date_finished,
                                book.rating,
                                book.id
                            ))
        
        self.connect.commit()

    # Delete certain book from the database by index
    def delete_book(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id = ?",
                            (book_id,)
                            )
        self.connect.commit()

    # Delete all books from the database keeping the table and incrementing id (Not implemened yet on the GUI)
    def clear_books(self):
        self.cursor.execute("DELETE FROM books")
        self.connect.commit()

    # Delete the entire database and start from scratch (Not implemened yet on the GUI)
    def reset_database(self):
        self.cursor.execute("DROP TABLE books")
        self.connect.commit()
        self._initialize_datebase()

    # Search for a book by name, author, genre
    def search(self, query):
        wildcard = f"%{query}%"

        self.cursor.execute("""
                            SELECT * FROM books
                            WHERE
                                title LIKE ?
                                OR author LIKE ?
                                OR genre LIKE ?
                            """, (wildcard, wildcard, wildcard))
        rows = self.cursor.fetchall()
        return [self._row_to_book(row) for row in rows]
    
    # Next few methods are for statistics
    # Count all books
    def count_books(self):
        self.cursor.execute("SELECT COUNT(*) FROM books")
        return self.cursor.fetchone()[0]
    
    # Counts books by status, READ, UNREAD, READING
    def count_by_status(self, status):
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE status = ?",
                            (status,)
                            )
        return self.cursor.fetchone()[0]
    
    # Count owned/not owned books
    def count_owned(self):
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE owned = 1")
        return self.cursor.fetchone()[0]
    
    def count_not_owned(self):
        self.cursor.execute("SELECT COUNT(*) FROM books WHERE owned = 0")
        return self.cursor.fetchone()[0]
    
    # Count total pages read
    def total_pages_read(self):
        self.cursor.execute("SELECT SUM(current_page) FROM books")
        result = self.cursor.fetchone()[0]
        return result if result else 0 # Counts also partially read books to the total
    
    def average_rating(self):
        self.cursor.execute("""SELECT AVG(rating)
                            FROM books
                            WHERE rating IS NOT NULL""")
        return self.cursor.fetchone()[0]
    
    # Fetch full list of owned books
    def get_stats(self):
        return {
            "total_books": self.count_books(),
            "owned": self.count_owned(),
            "not_owned": self.count_not_owned(),
            "finished": self.count_by_status("READ"),
            "unread": self.count_by_status("UNREAD"),
            "reading": self.count_by_status("READING"),
            "pages_read": self.total_pages_read(),
            "average_rating": self.average_rating()
        }
    
    # Next few methods for yearly stats (Not implemened yet on the GUI)
    # Count how many books I read in a given year
    def yearly_books(self, year):
        self.cursor.execute("""
                            SELECT COUNT(*)
                            FROM books
                            WHERE status = 'READ'
                                AND strftime('%Y', date_finished) = ?
                            """, (str(year),))
        return self.cursor.fetchone()[0]
    
    # Count how many pages I read in a given year
    def yearly_pages(self, year):
        self.cursor.execute("""
                            SELECT SUM(pages)
                            FROM books
                            WHERE status = 'READ'
                                AND strftime('%Y', date_finished) = ?
                            """, (str(year),))
        result = self.cursor.fetchone()[0]
        return result if result else 0
    
    # Owned and not owned read books in a given year
    def yearly_ownership_breakdown(self, year):
        self.cursor.execute("""
                            SELECT owned, COUNT(*) AS count
                            FROM books
                            WHERE status = 'READ'
                                AND strftime('%Y', date_finished) = ?
                            GROUP BY owned
                            """, (str(year),))
        rows = self.cursor.fetchall()

        breakdown = {"owned": 0, "not_owned": 0}
        for row in rows:
            if row["owned"] == 1:
                breakdown["owned"] = row["count"]
            else:
                breakdown["not_owned"] = row["count"]

        return breakdown
    
    # Average rating in a given year
    def yearly_avg_rating(self, year):
        self.cursor.execute("""
                            SELECT AVG(rating)
                            FROM books
                            WHERE rating IS NOT NULL
                                AND strftime('%Y', date_finished) = ?
                            """, (str(year),))
        return self.cursor.fetchone()[0]
    
    # Yearly total stats
    def yearly_summary(self, year):
        return {
            "year": year,
            "books_finished": self.yearly_books(year),
            "pages_read": self.yearly_pages(year),
            "ownership": self.yearly_ownership_breakdown(year),
            "average_rating": self.yearly_avg_rating(year)
        }
    
    # Close the database
    def close(self):
        self.connect.close()
        
