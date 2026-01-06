from datetime import date

class Book:
    # Contains book objects that:
    # Mark as read/unread
    # Contains information: Title, Author, Length, Genre
    def __init__(self, title, author, pages, genre, status="UNREAD", current_page=0, date_added=None, date_finished=None, owned=True, id=None, rating=None):
        self.title = title                          # book title, string
        self.author = author                        # book author, string
        self.pages = pages                          # book lenght, int
        self.genre  = genre                         # book genre, string

        self.owned = owned                          # Boolean to track whether or not I own a physical copy of the book
        self.current_page = current_page            # current page if status = READING
        self.status = status                        # book status, "READ", "UNREAD", "READING"

        self.date_added = date_added if date_added is not None else date.today().isoformat() # When was the book acquaired (optional)
        self.date_finished = date_finished          # Mark when the book is finished (optional)
        self.rating = rating                        # Rating for finished book (optional)
        self.id = id                                # Book id in the database, autoincrementing                         
        
    # Gives a finished book a rating after marking it as read
    def rate_book(self, rating):
        if 1 <= rating <= 10:
            self.rating = rating
        else:
            raise ValueError("Rating must be between 1 and 10") # Raise error if rating not between given interval

    # Marks the book as read when called and sets the date of finish
    def mark_read(self, rating=None):
        self.status = "READ" 
        self.current_page = self.pages
        self.date_finished = date.today().isoformat() # For later implementation adds the current date of 

        if rating is not None: # Updates the rating if marked as read multiple times
            self.rating = rating

    # Methods to track whether or not I own book in question (used for if I sell or buy books already in the list, not implemented yet)
    def mark_owned(self):
        self.owned = True

    def mark_not_owned(self):
        self.owned = False

    # Flips the owned value (Not implemented yet)
    def toggle_owned(self):
        self.owned = not self.owned

    # Marks the book as unread when called (Not implemented yet)
    def mark_unread(self):
        self.status = "UNREAD"

    # Formats the book title, author, genre, page count, status and rating
    def __str__(self):
        progress = f"{self.current_page}/{self.pages}"
        owned = "Owned" if self.owned else "Not Owned"
        rating = f"✰{self.rating}" if self.rating else "N/A"
        
        return (
            f"{self.title} by {self.author} | {self.genre} |"
            f"{self.status} | {progress} | {owned} | {rating} |"
        )