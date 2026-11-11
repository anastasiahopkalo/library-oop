from abc import ABC, abstractmethod
from functools import total_ordering
from typing import ClassVar, Self

from src.library.book import Book
from src.library.exceptions import (
    BorrowLimitError,
    NotBorrowedError,
    ValidationError,
)


@total_ordering
class Member(ABC):
    MAX_BOOKS: ClassVar[int] = 3
    LOAN_DAYS: ClassVar[int] = 21

    def __init__ (self, name: str, member_id :str) -> None:
        self.name = name
        self.member_id = member_id
        self._borrowed_books : list[Book] = []

    def describe(self) -> str:
        return f"Member [{self.membership_type.capitalize()}]: {self.name} (ID: {self.member_id})"

    @property
    @abstractmethod
    def membership_type(self) -> str:
        """Return the membership type identifier."""
        ...

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value : str) -> None:
        value = value.strip()
        if not value:
            raise ValidationError("Name cannot be empty")
        self._name = value

    @property
    def borrowed_books(self) -> tuple[Book, ...]:
        return tuple(self._borrowed_books)

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        return cls(data["name"], data["member_id"])

    def borrow (self, book : Book) -> None:
        if len(self._borrowed_books) >= self.MAX_BOOKS:
            raise BorrowLimitError(self, self.MAX_BOOKS)
        self._borrowed_books.append(book)

    def return_book(self, book : Book) -> None:
        if book not in self.borrowed_books:
            raise NotBorrowedError(self, book)
        self._borrowed_books.remove(book)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Member):
            return NotImplemented
        return self.member_id == other.member_id

    def __hash__(self) -> int:
        return hash(self.member_id)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Member):
            return NotImplemented
        return self.name.casefold() < other.name.casefold()

    def __repr__ (self) -> str:
        return f"{type(self).__name__}(name={self.name!r}, member_id={self.member_id!r})"

class RegularMember(Member):
    @property
    def membership_type(self) -> str:
        return "regular"