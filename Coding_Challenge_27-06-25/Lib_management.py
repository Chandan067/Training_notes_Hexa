class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.is_borrowed = False

    def __str__(self):
        return f"{self.title} by {self.author}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def view_books(self):
        print("\nLibrary Books:")
        if not self.books:
            print("No books in the library.")
            return
        for book in self.books:
            status = "Available" if not book.is_borrowed else "Borrowed"
            print(f"{book} - {status}")

    def borrow_book(self, book_title):
        for book in self.books:
            if book.title.lower() == book_title.lower() and not book.is_borrowed:
                book.is_borrowed = True
                print(f"You borrowed '{book.title}'")
                return
        print("Book not available.")

    def return_book(self, book_title):
        for book in self.books:
            if book.title.lower() == book_title.lower() and book.is_borrowed:
                book.is_borrowed = False
                print(f"You returned '{book.title}'")
                return
        print("Book not found or not borrowed.")


class User(Library):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return f"User: {self.name}"

lib = Library()
user1 = User("Alice")

while True:
    print("\n=== Library Menu ===")
    print("1. Add Book")
    print("2. View Books")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        title = input("Enter book title: ")
        author = input("Enter author name: ")
        lib.add_book(Book(title, author))
        print("Book added successfully.")

    elif choice == "2":
        lib.view_books()

    elif choice == "3":
        title = input("Enter book title to borrow: ")
        lib.borrow_book(title)

    elif choice == "4":
        title = input("Enter book title to return: ")
        lib.return_book(title)

    elif choice == "5":
        print("Exiting... Goodbye!")
        break

    else:
        print("Invalid option. Please choose from 1 to 5.")
