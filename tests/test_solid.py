from datetime import date, timedelta

import pytest

from src.library.book import Book
from src.library.exceptions import BorrowLimitError, DuplicateError
from src.library.library import Library
from src.library.member import Member, RegularMember
from src.library.member_types import PremiumMember, StudentMember
from src.library.repositories import BookReader
from src.library.staff import StaffMember


def _make_book(index: int) -> Book:
    isbn = f"978000000{index:04d}"
    return Book(isbn=isbn, title=f"Book {index}", author=f"Author {index}")

def test_library_default_constructor_works() -> None:
    lib = Library()
    member = RegularMember(name="Alice", member_id="M1")
    book = _make_book(1)

    lib.register_member(member)
    lib.add_book(book)
    lib.checkout("M1", book.isbn)

    assert len(lib) == 1
    assert book.isbn in lib
    assert not book.is_available

def test_dip_fake_book_repository_records_add_calls() -> None:
    class SpyBookRepository:
        def __init__(self) -> None:
            self.added_books: list[Book] = []

        def add(self, book: Book) -> None:
            self.added_books.append(book)

        def get(self, isbn: str) -> Book | None:
            for b in self.added_books:
                if b.isbn == isbn:
                    return b
            return None

        def all(self) -> tuple[Book, ...]:
            return tuple(self.added_books)

    spy_repo = SpyBookRepository()
    lib = Library(books=spy_repo)
    book = _make_book(1)

    lib.add_book(book)

    assert spy_repo.added_books == [book]

def test_dip_fake_clock_sets_checkout_due_date() -> None:
    fake_today = date(2026, 5, 10)
    lib = Library(clock=lambda: fake_today)
    member = RegularMember(name="Alice", member_id="M1")
    book = _make_book(1)

    lib.register_member(member)
    lib.add_book(book)
    due_date = lib.checkout("M1", book.isbn)

    assert due_date == fake_today + timedelta(days=member.LOAN_DAYS)

@pytest.mark.parametrize(
    "member_cls",
    [RegularMember, StudentMember, PremiumMember, StaffMember],
)
def test_member_contract(member_cls: type[Member]) -> None:
    if member_cls is StudentMember:
        member: Member = StudentMember(name="Bob", member_id="M1", school="KNU")
    elif member_cls is PremiumMember:
        member = PremiumMember(name="Clara", member_id="M1", annual_fee=100.0)
    else:
        member = member_cls(name="Alex", member_id="M1")

    borrowed: list[Book] = []
    for i in range(member.MAX_BOOKS):
        book = _make_book(i + 1)
        member.borrow(book)
        borrowed.append(book)

    assert len(member.borrowed_books) == member.MAX_BOOKS

    extra_book = _make_book(999)
    with pytest.raises(BorrowLimitError):
        member.borrow(extra_book)

    member.return_book(borrowed[0])
    member.borrow(extra_book)
    assert extra_book in member.borrowed_books

def print_catalog(reader: BookReader, capsys: pytest.CaptureFixture[str] | None = None) -> list[str]:
    lines = [f"{b.title} ({b.isbn})" for b in reader.all()]
    for line in lines:
        print(line)
    return lines


def test_isp_print_catalog_with_read_only_fake(capsys: pytest.CaptureFixture[str]) -> None:
    class ReadOnlyBookFake:

        def __init__(self, books: list[Book]) -> None:
            self._books = {b.isbn: b for b in books}

        def get(self, isbn: str) -> Book | None:
            return self._books.get(isbn)

        def all(self) -> tuple[Book, ...]:
            return tuple(self._books.values())

    b1 = _make_book(1)
    b2 = _make_book(2)
    fake_reader = ReadOnlyBookFake([b1, b2])

    assert not hasattr(fake_reader, "add")
    print_catalog(fake_reader)

    captured = capsys.readouterr().out
    assert "Book 1" in captured
    assert "Book 2" in captured

def test_ocp_staff_member_through_library_checkout() -> None:
    fake_today = date(2026, 1, 1)
    lib = Library(clock=lambda: fake_today)
    staff = StaffMember(name="Dr. Ivanenko", member_id="ST1")
    lib.register_member(staff)

    for i in range(20):
        book = _make_book(i + 1)
        lib.add_book(book)
        due = lib.checkout("ST1", book.isbn)
        assert due == fake_today + timedelta(days=60)

    book_21 = _make_book(21)
    lib.add_book(book_21)
    with pytest.raises(BorrowLimitError):
        lib.checkout("ST1", book_21.isbn)

def test_duplicate_isbn_and_member_id_raise_duplicate_error() -> None:
    lib = Library()
    book = _make_book(1)
    member = RegularMember(name="Alice", member_id="M1")

    lib.add_book(book)
    with pytest.raises(DuplicateError):
        lib.add_book(book)

    lib.register_member(member)
    with pytest.raises(DuplicateError):
        lib.register_member(member)
