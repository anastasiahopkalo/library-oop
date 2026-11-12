from collections.abc import Callable, Iterator
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Self

from src.library.book import Book
from src.library.exceptions import (
    BookNotFoundError,
    BookUnavailableError,
    DuplicateError,
    MemberNotFoundError,
)
from src.library.fines import FineCalculator, FlatRateFineCalculator
from src.library.loan import Loan
from src.library.member import Member
from src.library.repositories import (
    BookRepository,
    InMemoryBookRepository,
    InMemoryMemberRepository,
    MemberRepository,
)


class Library:
    def __init__(
            self,
            books: BookRepository | None = None,
            members: MemberRepository | None = None,
            fines: FineCalculator | None = None,
            clock: Callable[[], date] = date.today,
    ) -> None:
        self._books = books if books is not None else InMemoryBookRepository()
        self._members = members if members is not None else InMemoryMemberRepository()
        self._fines = fines if fines is not None else FlatRateFineCalculator()
        self._clock = clock
        self._loans: dict[str, Loan] = {}

    def __len__(self) -> int:
        return len(self._books.all())

    def __iter__(self) -> Iterator[Book]:
        yield from self._books.all()

    def __contains__(self, isbn: object) -> bool:
        if not isinstance(isbn, str):
            return False
        return self._books.get(isbn) is not None

    @property
    def books(self) -> tuple[Book, ...]:
        return self._books.all()

    @property
    def sorted_books(self) -> list[Book]:
        return sorted(self._books.all())

    @property
    def members(self) -> tuple[Member, ...]:
        return self._members.all()

    @property
    def active_loans(self) -> tuple[Loan, ...]:
        return tuple(self._loans.values())

    def loans_for(self, member_id: str) -> tuple[Loan, ...]:
        if self._members.get(member_id) is None:
            raise MemberNotFoundError(member_id)
        return tuple(
            loan for loan in self._loans.values()
            if loan.member_id == member_id
        )

    def add_book(self, book: Book)-> None:
        if self._books.get(book.isbn) is not None:
            raise DuplicateError(f"Book {book.title} already exists in the library")
        self._books.add(book)
    def register_member(self, member: Member)-> None:
        if self._members.get(member.member_id) is not None:
            raise DuplicateError(f"Member {member.member_id} is already registered in the library")
        self._members.add(member)
    def find_book_by_title(self,title : str) -> Book | None:
        for book in self._books.all():
            if book.title == title:
                return book
        return None
    def checkout(self, member_id : str, isbn: str) -> date:
        member = self._members.get(member_id)
        if member is None:
            raise MemberNotFoundError(member_id)
        book = self._books.get(isbn)
        if book is None:
            raise BookNotFoundError(isbn)
        if not book.is_available:
            raise BookUnavailableError(book)
        due_date = self._clock() + timedelta(days=member.LOAN_DAYS)
        member.borrow(book)
        book.is_available = False
        self._loans[isbn] = Loan(book = book, member_id=member_id, due_date=due_date)
        return due_date

    def return_book(self, member_id: str, isbn: str) -> Decimal:
        member = self._members.get(member_id)
        if member is None:
            raise MemberNotFoundError(member_id)
        book = self._books.get(isbn)
        if book is None:
            raise BookNotFoundError(isbn)
        loan = self._loans.get(isbn)
        member.return_book(book)
        book.is_available = True
        self._loans.pop(isbn, None)
        if loan is None:
            return Decimal("0.00")
        return self._fines.calculate(loan, self._clock())

    @classmethod
    def from_books_file(cls, path: str | Path) -> Self:
        library = cls()
        file_path = Path(path)
        with file_path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    book = Book.from_string(line)
                    library.add_book(book)
        return library

