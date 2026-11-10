from datetime import date, timedelta
from pathlib import Path
from typing import Self

from src.library.book import Book
from src.library.loan import Loan
from src.library.member import Member


class Library:
    def __init__(self)-> None:
        self._books: dict[str, Book] = {}
        self._members: dict[str, Member] = {}
        self._loans: dict[str, Loan] = {}

    @property
    def books(self) -> tuple[Book, ...]:
        return tuple(self._books.values())

    @property
    def members(self) -> tuple[Member, ...]:
        return tuple(self._members.values())

    @property
    def active_loans(self) -> tuple[Loan, ...]:
        return tuple(self._loans.values())

    def loans_for(self, member_id: str) -> tuple[Loan, ...]:
        if member_id not in self._members:
            raise ValueError(f"Member {member_id} not available")
        return tuple(
            loan for loan in self._loans.values()
            if loan.member_id == member_id
        )

    def add_book(self, book: Book)-> None:
        if book.isbn in self._books:
            raise ValueError(f"Book {book.title} already exists in the library")
        self._books[book.isbn] = book
    def register_member(self, member: Member)-> None:
        if member.member_id in self._members:
            raise ValueError(f"Member {member.member_id} is already registered in the library")
        self._members[member.member_id] = member
    def find_book_by_title(self,title : str) -> Book | None:
        for book in self._books.values():
            if book.title == title:
                return book
        return None
    def checkout(self, member_id : str, isbn: str) -> date:
        if member_id not in self._members:
            raise ValueError(f"Member {member_id} not available")
        if isbn not in self._books:
            raise ValueError(f"ISBN {isbn} not available")
        member = self._members[member_id]
        book = self._books[isbn]
        if not book.is_available:
            raise ValueError(f"Book {isbn} is not available")
        due_date = date.today() + timedelta(days=member.LOAN_DAYS)
        member.borrow(book)
        book.is_available = False
        self._loans[isbn] = Loan(book = book, member_id=member_id, due_date=due_date)
        return due_date

    def return_book(self, member_id: str, isbn: str) -> None:
        if member_id not in self._members:
            raise ValueError(f"Member {member_id} not available")
        if isbn not in self._books:
            raise ValueError(f"ISBN {isbn} not available")
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

