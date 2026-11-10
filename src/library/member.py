from typing import ClassVar, Self

from src.library.book import Book


class Member:
    MAX_BOOKS: ClassVar[int] = 3
    LOAN_DAYS: ClassVar[int] = 21

    def __init__ (self, name: str, member_id :str) -> None:
        self.name = name
        self.member_id = member_id
        self._borrowed_books : list[Book] = []

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value : str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value

    @property
    def borrowed_books(self) -> tuple[Book, ...]:
        return tuple(self._borrowed_books)

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Self:
        return cls(data["name"], data["member_id"])

    def borrow (self, book : Book) -> None:
        if len(self._borrowed_books) >= self.MAX_BOOKS:
            raise ValueError(f"{self.name} reached the limit of {self.MAX_BOOKS} books")
        self._borrowed_books.append(book)

    def return_book(self, book : Book) -> None:
        if book not in self.borrowed_books:
            raise ValueError("This member did not borrow that book")
        self._borrowed_books.remove(book)

    def __repr__ (self) -> str:
        return f"{type(self).__name__}(name={self.name!r}, member_id={self.member_id!r})"
