import pytest

from src.library.book import Book
from src.library.library import Library
from src.library.member import Member


@pytest.fixture
def empty_library() -> Library:
    return Library()

@pytest.fixture
def library_with_book_and_member() -> tuple[Library, Member, Book]:
    library = Library()
    member = Member("Ana", "M1")
    book = Book("Dune", "Frank Herbert", "111")
    library.register_member(member)
    library.add_book(book)
    return library, member, book

def test_checkout_marks_book_unavailable(library_with_book_and_member):
    library, member, book = library_with_book_and_member
    library.checkout(member.member_id, book.isbn)
    assert book.is_available is False

def test_create_book_defaults_to_available():
    book = Book("The Hobbit", "J.R.R. Tolkien", "ISBN-000")
    assert book.title == "The Hobbit"
    assert book.author == "J.R.R. Tolkien"
    assert book.isbn == "ISBN-000"
    assert book.is_available is True

def test_create_member_empty_borrowed_list():
    member = Member("Bob", "M002")
    assert member.name == "Bob"
    assert member.member_id == "M002"
    assert len(member.borrowed_books) == 0
    assert member.borrowed_books == []

def test_successful_checkout(library_with_book_and_member):
    library, member, book = library_with_book_and_member
    library.checkout(member.member_id, book.isbn)
    assert book in member.borrowed_books
    assert len(member.borrowed_books) == 1

def test_checkout_already_borrowed_book_raises_value_error(library_with_book_and_member):
    library, member1, book = library_with_book_and_member
    member2 = Member("Bob", "M002")
    library.register_member(member2)

    library.checkout(member1.member_id, book.isbn)

    with pytest.raises(ValueError):
        library.checkout(member2.member_id, book.isbn)

def test_exceeding_max_books_raises_and_fourth_book_stays_available(empty_library):
    library = empty_library
    member = Member("Charlie", "M003")
    library.register_member(member)

    b1 = Book("Book 1", "Author 1", "ISBN-1")
    b2 = Book("Book 2", "Author 2", "ISBN-2")
    b3 = Book("Book 3", "Author 3", "ISBN-3")
    b4 = Book("Book 4", "Author 4", "ISBN-4")

    for b in (b1, b2, b3, b4):
        library.add_book(b)

    library.checkout(member.member_id, b1.isbn)
    library.checkout(member.member_id, b2.isbn)
    library.checkout(member.member_id, b3.isbn)

    with pytest.raises(ValueError):
        library.checkout(member.member_id, b4.isbn)

    assert b4.is_available is True
    assert b4 not in member.borrowed_books

def test_returning_book_makes_it_available_again(library_with_book_and_member):
    library, member, book = library_with_book_and_member

    library.checkout(member.member_id, book.isbn)
    assert book.is_available is False

    library.return_book(member.member_id, book.isbn)
    assert book.is_available is True
    assert book not in member.borrowed_books

def test_find_book_by_title(empty_library):
    library = empty_library
    book = Book("Dune", "Frank Herbert", "ISBN-999")
    library.add_book(book)

    found_book = library.find_book_by_title("Dune")
    assert found_book == book
    assert found_book.isbn == "ISBN-999"

    missing_book = library.find_book_by_title("Non-Existent Book")
    assert missing_book is None