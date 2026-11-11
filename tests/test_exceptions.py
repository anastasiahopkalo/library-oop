import pytest

from src.library.book import Book
from src.library.exceptions import (
    BookNotFoundError,
    BookUnavailableError,
    BorrowLimitError,
    DuplicateError,
    LibraryError,
    MemberNotFoundError,
    NotFoundError,
    ValidationError,
)
from src.library.library import Library
from src.library.member import Member, RegularMember
from src.library.member_types import StudentMember


def test_member_is_abstract_raises_type_error() -> None:
    with pytest.raises(TypeError):
        Member("Alice", "M001")
    reg = RegularMember("Alice", "M001")
    assert reg.name == "Alice"
    assert reg.membership_type == "regular"

def test_subclass_missing_membership_type_cannot_be_instantiated() -> None:
    class IncompleteMember(Member):
        pass

    with pytest.raises(TypeError):
        IncompleteMember("Bob", "M002")

def test_validation_error_is_caught_by_value_error_and_library_error() -> None:
    err = ValidationError("Bad ISBN")

    with pytest.raises(ValueError):
        raise err

    with pytest.raises(LibraryError):
        raise err

def test_checkout_unknown_isbn_raises_book_not_found_error() -> None:
    library = Library()
    member = RegularMember("Alice", "M001")
    library.register_member(member)

    missing_isbn = "9780000000000"
    with pytest.raises(BookNotFoundError) as exc_info:
        library.checkout(member.member_id, missing_isbn)

    assert exc_info.value.isbn == missing_isbn

def test_checkout_unknown_member_raises_member_not_found_error() -> None:
    library = Library()
    book = Book("Dune", "Frank Herbert", "9780441172719")
    library.add_book(book)

    missing_id = "M999"
    with pytest.raises(MemberNotFoundError) as exc_info:
        library.checkout(missing_id, book.isbn)

    assert exc_info.value.member_id == missing_id

def test_checkout_borrowed_book_raises_book_unavailable_error() -> None:
    library = Library()
    m1 = RegularMember("Alice", "M001")
    m2 = RegularMember("Bob", "M002")
    book = Book("Dune", "Frank Herbert", "9780441172719")

    library.register_member(m1)
    library.register_member(m2)
    library.add_book(book)

    library.checkout(m1.member_id, book.isbn)

    with pytest.raises(BookUnavailableError) as exc_info:
        library.checkout(m2.member_id, book.isbn)

    assert exc_info.value.book == book

def test_student_third_book_raises_borrow_limit_error() -> None:
    library = Library()
    student = StudentMember("Bob", "S001", "KPI")
    library.register_member(student)

    b1 = Book("Book 1", "Author 1", "1000000001")
    b2 = Book("Book 2", "Author 2", "1000000002")
    b3 = Book("Book 3", "Author 3", "1000000003")

    for b in (b1, b2, b3):
        library.add_book(b)

    library.checkout(student.member_id, b1.isbn)
    library.checkout(student.member_id, b2.isbn)

    with pytest.raises(BorrowLimitError) as exc_info:
        library.checkout(student.member_id, b3.isbn)

    assert exc_info.value.member == student
    assert exc_info.value.limit == 2
    assert b3.is_available is True

def test_duplicate_isbn_raises_duplicate_error() -> None:
    library = Library()
    b1 = Book("Dune", "Frank Herbert", "9780441172719")
    b2 = Book("Dune 2", "Frank Herbert", "9780441172719")

    library.add_book(b1)
    with pytest.raises(DuplicateError):
        library.add_book(b2)

@pytest.mark.parametrize(
    "checkout_args, expected_type",
    [
        (("M999", "9780441172719"), MemberNotFoundError),
        (("M001", "9000000000000"), BookNotFoundError),
    ],
)
def test_not_found_error_catches_both_member_and_book_cases(
    checkout_args: tuple[str, str], expected_type: type[NotFoundError]
) -> None:
    library = Library()
    member = RegularMember("Alice", "M001")
    book = Book("Dune", "Frank Herbert", "9780441172719")

    library.register_member(member)
    library.add_book(book)

    with pytest.raises(NotFoundError) as exc_info:
        library.checkout(*checkout_args)

    assert isinstance(exc_info.value, expected_type)

def test_error_message_pattern_match() -> None:
    library = Library()
    member = RegularMember("Alice", "M001")
    library.register_member(member)

    with pytest.raises(BookNotFoundError, match="ISBN '999' was not found"):
        library.checkout(member.member_id, "999")