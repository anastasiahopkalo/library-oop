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
    book = Book("Dune", "Frank Herbert", "9780441172719")
    library.register_member(member)
    library.add_book(book)
    return library, member, book

def test_checkout_marks_book_unavailable(library_with_book_and_member):
    library, member, book = library_with_book_and_member
    library.checkout(member.member_id, book.isbn)
    assert book.is_available is False

def test_create_book_defaults_to_available():
    book = Book("The Hobbit", "J.R.R. Tolkien", "054792822X".replace("X", "0"))
    assert book.title == "The Hobbit"
    assert book.author == "J.R.R. Tolkien"
    assert book.isbn == "0547928220"
    assert book.is_available is True

def test_create_member_empty_borrowed_list():
    member = Member("Bob", "M002")
    assert member.name == "Bob"
    assert member.member_id == "M002"
    assert len(member.borrowed_books) == 0
    assert member.borrowed_books == ()

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

    b1 = Book("Book 1", "Author 1", "1000000001")
    b2 = Book("Book 2", "Author 2", "1000000002")
    b3 = Book("Book 3", "Author 3", "1000000003")
    b4 = Book("Book 4", "Author 4", "1000000004")

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
    book = Book("Dune", "Frank Herbert", "9780441172719")
    library.add_book(book)

    found_book = library.find_book_by_title("Dune")
    assert found_book == book
    assert found_book.isbn == "9780441172719"

    missing_book = library.find_book_by_title("Non-Existent Book")
    assert missing_book is None

@pytest.mark.parametrize("invalid_isbn", ["123", "abcdefghij", "", "12345678901234"])
def test_invalid_isbn_raises_value_error(invalid_isbn: str) -> None:
    with pytest.raises(ValueError):
        Book("Title", "Author", invalid_isbn)

def test_isbn_normalization() -> None:
    book = Book("Dune", "Frank Herbert", "978-0-441-01359-3")
    assert book.isbn == "9780441013593"

@pytest.mark.parametrize("title, author", [("", "Author"), ("   ", "Author"), ("Title", ""), ("Title", "   ")])
def test_empty_or_whitespace_title_author_raises(title: str, author: str) -> None:
    with pytest.raises(ValueError):
        Book(title, author, "9780441013593")

def test_book_from_string_valid() -> None:
    book = Book.from_string("Dune | Frank Herbert | 9780441013593")
    assert book.title == "Dune"
    assert book.author == "Frank Herbert"
    assert book.isbn == "9780441013593"

@pytest.mark.parametrize("malformed_line", ["Part1 | Part2", "Part1 | Part2 | Part3 | Part4"])
def test_book_from_string_malformed_raises(malformed_line: str) -> None:
    with pytest.raises(ValueError):
        Book.from_string(malformed_line)

def test_books_equality_ignores_is_available() -> None:
    b1 = Book("Dune", "Frank Herbert", "9780441013593", is_available=True)
    b2 = Book("Dune", "Frank Herbert", "9780441013593", is_available=False)
    assert b1 == b2

def test_member_name_stripping_and_validation() -> None:
    m = Member("  Alice  ", "M001")
    assert m.name == "Alice"

    with pytest.raises(ValueError):
        Member("   ", "M002")

def test_member_borrowed_books_immutability() -> None:
    m = Member("Alice", "M001")
    book = Book("Dune", "Frank Herbert", "9780441013593")

    with pytest.raises(AttributeError):
        m.borrowed_books.append(book)

    with pytest.raises(AttributeError):
        m.borrowed_books = []

def test_add_duplicate_isbn_raises(empty_library: Library) -> None:
    b1 = Book("Dune", "Frank Herbert", "9780441013593")
    b2 = Book("Dune 2", "Frank Herbert", "9780441013593")
    empty_library.add_book(b1)

    with pytest.raises(ValueError):
        empty_library.add_book(b2)

def test_member_from_dict() -> None:
    m = Member.from_dict({"name": "Alice", "member_id": "M001"})
    assert m.name == "Alice"
    assert m.member_id == "M001"