from src.library.book import Book
from src.library.library import Library
from src.library.member import Member
from src.library.member_types import PremiumMember, StudentMember


def main() -> None:
    library = Library()

    try:
        malformed_book = Book.from_string("Brave New World | Aldous Huxley")
        library.add_book(malformed_book)
    except ValueError as e:
        print(f"Format error: {e}\n")

    alice = Member(name="Alice", member_id="M001")
    bob = StudentMember(name="Bob", member_id="S001", school="KPI")
    charlie = PremiumMember(name="Charlie", member_id="P001", annual_fee=100.0)

    for member in (alice, bob, charlie):
        library.register_member(member)

    raw_books = [
        "The Land of Stories | Chris Colfer | 978-0451524935",
        "The Hobbit | J.R.R. Tolkien | 978-0547928227",
        "Dune | Frank Herbert | 978-0441172719",
        "Fahrenheit 451 | Ray Bradbury | 978-1451673319",
        "1984 | George Orwell | 978-0451524936",
        "Brave New World | Aldous Huxley | 978-0060850524",
        "Animal Farm | George Orwell | 978-0451526342",
        "The Catcher in the Rye | J.D. Salinger | 978-0316769488",
        "To Kill a Mockingbird | Harper Lee | 978-0061120084",
    ]

    for line in raw_books:
        library.add_book(Book.from_string(line))

    all_books = list(library.books)
    book_index = 0

    for member in (alice, bob, charlie):
        for _ in range(3):
            book = all_books[book_index]
            book_index += 1
            try:
                due_date = library.checkout(member.member_id, book.isbn)
                print(f" '{book.title}' borrowed until {due_date}")
            except ValueError as e:
                print(f"'{book.title}' — {e}")

    try:
        library.checkout(member_id="M001", isbn=all_books[0].isbn)
    except ValueError as e:
        print(f"Book is already booked: {e}")

    try:
        library.checkout(member_id="M999", isbn=all_books[3].isbn)
    except ValueError as e:
        print(f"Member ID doesn't exist: {e}")


if __name__ == "__main__":
    main()