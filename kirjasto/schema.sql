
-- create an sql table to store the book class information into
CREATE TABLE IF NOT EXISTS books (
    -- stores information of the book class as a database
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    pages INTEGER NOT NULL,
    current_page INTEGER NOT NULL,
    status TEXT CHECK(status IN ('UNREAD', 'READING', 'READ')) DEFAULT 'UNREAD', -- By default set to unread
    genre TEXT,
    owned INTEGER NOT NULL DEFAULT 1,
    date_added TEXT, -- Not added yet to the GUI
    date_finished TEXT, -- Not added yet to the GUI
    rating INTEGER 
);