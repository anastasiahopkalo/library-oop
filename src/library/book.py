from dataclasses import dataclass, field
from functools import total_ordering
from typing import Self

from src.library.exceptions import (
    ValidationError,
)


@total_ordering
@dataclass
class Book:
    title: str
    author: str
    isbn: str
    is_available: bool = field(default=True, compare=False)

    def describe(self) -> str:
        return f"Book: '{self.title}' by {self.author} (ISBN: {self.isbn})"

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        self.author = self.author.strip()
        if not self.title or not self.author:
            raise ValidationError("Title and author cannot be empty")
        cleaned = self.isbn.replace("-", "").replace(" ", "")
        if not Book.is_valid_isbn(cleaned):
            raise ValidationError(f"Invalid ISBN: {self.isbn!r}")
        self.isbn = cleaned

    @staticmethod
    def is_valid_isbn(isbn: str) -> bool:
        return isbn.isdigit() and len(isbn) in (10, 13)

    @classmethod
    def from_string(cls, line: str) -> Self:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            raise ValidationError(f"Expected 'title | author | isbn', got {line!r}")
        title, author, isbn = parts
        return cls(title=title, author=author, isbn=isbn)

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Book):
            return NotImplemented
        return (self.title.casefold(), self.author.casefold()) < (
            other.title.casefold(),
            other.author.casefold(),
        )

    def __str__(self) -> str:
        status = "available" if self.is_available else "checked out"
        return f"'{self.title}' by {self.author} ({status})"