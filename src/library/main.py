from collections.abc import Iterable
from datetime import date, timedelta
from decimal import Decimal

from src.library.book import Book
from src.library.exceptions import (
    BookNotFoundError,
    BookUnavailableError,
    BorrowLimitError,
    DuplicateError,
    LibraryError,
    MemberNotFoundError,
    ValidationError,
)
from src.library.fines import FlatRateFineCalculator
from src.library.library import Library
from src.library.member import RegularMember
from src.library.member_types import PremiumMember, StudentMember
from src.library.protocols import HasDescribe
from src.library.repositories import InMemoryBookRepository, InMemoryMemberRepository
from src.library.staff import StaffMember


def print_all(items: Iterable[HasDescribe]) -> None:
    for item in items:
        print(item.describe())


def main() -> None:
    current_date = date.today()

    books_repo = InMemoryBookRepository()
    members_repo = InMemoryMemberRepository()
    fine_calculator = FlatRateFineCalculator(Decimal("0.75"))

    library = Library(
        books=books_repo,
        members=members_repo,
        fines=fine_calculator,
        clock=lambda: current_date,
    )

    try:
        malformed_book = Book.from_string("Brave New World | Aldous Huxley")
        library.add_book(malformed_book)
    except ValidationError as e:
        print(f"Format error: {e}\n")

    alice = RegularMember(name="Alice", member_id="M001")
    bob = StudentMember(name="Bob", member_id="S001", school="KPI")
    charlie = PremiumMember(name="Charlie", member_id="P001", annual_fee=100.0)
    diana = StaffMember(name="Diana", member_id="ST001")

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
            except LibraryError as e:
                print(f"'{book.title}' — {e}")

    try:
        library.checkout(member_id="M001", isbn=all_books[0].isbn)
    except BookUnavailableError as e:
        print(f"Book is already booked: {e}")

    try:
        library.checkout(member_id="M999", isbn=all_books[3].isbn)
    except MemberNotFoundError as e:
        print(f"Member ID doesn't exist: {e}")

    print(f"Total books: {len(library)}")
    print(f"Is Dune in library: {'9780441172719' in library}\n")

    print("Sorted catalog:")
    for book in sorted(library):
        print(f"  • {book.title}")

    print_all(library.members)
    print_all(library)

    try:
        library.register_member(alice)
    except DuplicateError as e:
        print(f"Duplicate error: {e}")

    try:
        library.checkout("M001", "9999999999")
    except BookNotFoundError as e:
        print(f"Not found error: {e}")
    except LibraryError as e:
        print(f"General library error: {e}")

    for b in list(bob.borrowed_books):
        library.return_book(bob.member_id, b.isbn)
    free_books = [b for b in library if b.is_available]
    try:
        library.checkout(bob.member_id, free_books[0].isbn)
        library.checkout(bob.member_id, free_books[1].isbn)
        library.checkout(bob.member_id, free_books[2].isbn)
    except BorrowLimitError as e:
        print(f"Limit error: {e}")


    alice_book = alice.borrowed_books[0]
    current_date = date.today() + timedelta(days=20)
    fine = library.return_book(alice.member_id, alice_book.isbn)
    print(f"\nReturned '{alice_book.title}' 20 days later. Fine: ${fine}")


if __name__ == "__main__":
    main()