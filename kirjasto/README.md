A bookshself software I did to practice the usage of databases and handling a project that contains information from multiple files.
The basic idea is that when run, a screen with a blank list opens up. To the list can be added books by title, author, lentgh and genre,
which then can be modified and rated according to reading updates. 

The structure is as follows: First is the book.py which contains a class, that creates objects called Book, which store information about
the books to be stored and simple functions such as updating reading status for the book and marking as read. Next comes the schema.sql, 
which creates the SQL table called 'books', where the information from the book obejcts are stored as records. After that we have the repo.py 
which creates the database and translates the python script to SQL commands so that we can alter the records in our database. The 
library_GUI.py file utilizes the pyside6 library to create an GUI and the layout for it. After that we have the main.py file which runs the 
software. The test.py file is something I used to quickly delete the created databases from the directory as I was debugging the software, so its 
only a  debugging tool so to say.
