from book import Book
from repo import BookRepository
from library_GUI import run_gui

def main():

    # Define the repository
    repo = BookRepository()
    
    # Run the program for defined repository
    run_gui(repo)

    # Test code to see if the repo works as intended
    #book1 = Book("bookname1", "auhtor1", 608, "Comedy", owned=True)
    #book2 = Book("bookname2", "author2", 701, "Tragedy", owned=False)

    #repo.add_book(book1)
    #repo.add_book(book2)

    #book1.mark_read(rating=8)
    #repo.update(book1)

    #book2.update_prog(241)
    #repo.update(book2)

    #print("\n--- All Books ---")
    #for book in repo.get_all_books():
    #      print(book)

    #print("\n--- Stats ---")
    #stats = repo.get_stats()
    #for key, value in stats.items():
    #      print(f"{key}: {value}")

    #print("\n--- Yearly Stats ---")
    #year  = 2026
    #summary = repo.yearly_summary(year)
    #for key, value in summary.items():
    #     print(f"{key}: {value}")

    # Close repository
    repo.close()


if __name__ == "__main__":
    main()