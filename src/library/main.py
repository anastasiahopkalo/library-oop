from src.library.book import Book
from src.library.library import Library
from src.library.member import Member


def main() -> None:
    library = Library()
    alice = Member(name = 'Alice', member_id = "M001")
    bob = Member(name = 'Bob', member_id = "M002")
    library.register_member(alice)
    library.register_member(bob)

    raw_books = [
        "The Land of Stories | Chris Colfer | 978-0451524935",
        "The Hobbit | J.R.R. Tolkien | 978-0547928227",
        "Dune | Frank Herbert | 978-0441172719",
        "Fahrenheit 451 | Ray Bradbury | 978-1451673319",
    ]

    for line in raw_books:
        library.add_book(Book.from_string(line))

    # Зберігаємо посилання для зручного виводу
    book1 = library.find_book_by_title("The Land of Stories")
    book2 = library.find_book_by_title("The Hobbit")
    book3 = library.find_book_by_title("Dune")
    book4 = library.find_book_by_title("Fahrenheit 451")

    try:
        malformed_book = Book.from_string("Brave New World | Aldous Huxley")
        library.add_book(malformed_book)
    except ValueError as e:
        print(f"Format error: {e}\n")

    library.checkout(member_id="M001", isbn="978-0451524935")  # Alice takes 1984
    print(f"Alice borrowed: {book1}")

    library.checkout(member_id="M001", isbn="978-0547928227")  # Alice takes The Hobbit
    print(f"Alice borrowed: {book2}")

    library.checkout(member_id="M002", isbn="978-0441172719")  # Bob takes Dune
    print(f"Bob borrowed: {book3}")

    try:
        library.checkout(member_id="M002", isbn="978-0451524935")
    except ValueError as e:
        print(f"Book is already booked: {e}")

    try:
        library.checkout(member_id="M999", isbn="978-1451673319")
    except ValueError as e:
        print(f"Member ID doesn't exist: {e}")

    library.checkout(member_id="M001", isbn="978-1451673319")  # Alice takes 3rd book
    print(f"\nAlice borrowed 3rd book: {book4}")

    extra_book = Book(title="Brave New World", author="Aldous Huxley", isbn="978-0060850524")
    library.add_book(extra_book)
    try:
        library.checkout(member_id="M001", isbn="978-0060850524")
    except ValueError as e:
        print(f"You have reached your limit (max 3): {e}")

    print(f"Alice: {alice.borrowed_books}")


if __name__ == "__main__":
    main()

