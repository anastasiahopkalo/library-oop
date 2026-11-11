from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path
from typing import Self

from src.library.book import Book
from src.library.exceptions import (
    BookNotFoundError,
    BookUnavailableError,
    DuplicateError,
    MemberNotFoundError,
)
from src.library.loan import Loan
from src.library.member import RegularMember


class Library:
    def __init__(self)-> None:
        self._books: dict[str, Book] = {}
        self._members: dict[str, RegularMember] = {}
        self._loans: dict[str, Loan] = {}

    def __len__(self) -> int:
        """Return the total number of books in the catalog."""
        return len(self._books)

    def __iter__(self) -> Iterator[Book]:
        """Yield books from the catalog."""
        yield from self._books.values()

    def __contains__(self, isbn: object) -> bool:
        """Check if a book with the given ISBN exists in the library."""
        if not isinstance(isbn, str):
            return False
        return isbn in self._books

    @property
    def books(self) -> tuple[Book, ...]:
        return tuple(self._books.values())

    @property
    def sorted_books(self) -> list[Book]:
        """Return books sorted by title and author (using Book's __lt__)."""
        return sorted(self._books.values())

    @property
    def members(self) -> tuple[RegularMember, ...]:
        return tuple(self._members.values())

    @property
    def active_loans(self) -> tuple[Loan, ...]:
        return tuple(self._loans.values())

    def loans_for(self, member_id: str) -> tuple[Loan, ...]:
        if member_id not in self._members:
            raise MemberNotFoundError(member_id)
        return tuple(
            loan for loan in self._loans.values()
            if loan.member_id == member_id
        )

    def add_book(self, book: Book)-> None:
        if book.isbn in self._books:
            raise DuplicateError(f"Book {book.title} already exists in the library")
        self._books[book.isbn] = book
    def register_member(self, member: RegularMember)-> None:
        if member.member_id in self._members:
            raise DuplicateError(f"Member {member.member_id} is already registered in the library")
        self._members[member.member_id] = member
    def find_book_by_title(self,title : str) -> Book | None:
        for book in self._books.values():
            if book.title == title:
                return book
        return None
    def checkout(self, member_id : str, isbn: str) -> date:
        if member_id not in self._members:
            raise MemberNotFoundError(member_id)
        if isbn not in self._books:
            raise BookNotFoundError(isbn)
        member = self._members[member_id]
        book = self._books[isbn]
        if not book.is_available:
            raise BookUnavailableError(book)
        due_date = date.today() + timedelta(days=member.LOAN_DAYS)
        member.borrow(book)
        book.is_available = False
        self._loans[isbn] = Loan(book = book, member_id=member_id, due_date=due_date)
        return due_date

    def return_book(self, member_id: str, isbn: str) -> None:
        if member_id not in self._members:
            raise MemberNotFoundError(member_id)
        if isbn not in self._books:
            raise BookNotFoundError(isbn)
        member = self._members[member_id]
        book = self._books[isbn]
        member.return_book(book)
        book.is_available = True
        self._loans.pop(isbn, None)

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

