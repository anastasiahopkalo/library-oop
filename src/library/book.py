from dataclasses import dataclass, field
from typing import Self


@dataclass
class Book:
    title: str
    author: str
    isbn: str
    is_available: bool = field(default=True, compare=False)

    def __post_init__(self) -> None:
        self.title = self.title.strip()
        self.author = self.author.strip()
        if not self.title or not self.author:
            raise ValueError("Title and author cannot be empty")
        cleaned = self.isbn.replace("-", "").replace(" ", "")
        if not Book.is_valid_isbn(cleaned):
            raise ValueError(f"Invalid ISBN: {self.isbn!r}")
        self.isbn = cleaned

    @staticmethod
    def is_valid_isbn(isbn: str) -> bool:
        return isbn.isdigit() and len(isbn) in (10, 13)

    @classmethod
    def from_string(cls, line: str) -> Self:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            raise ValueError(f"Expected 'title | author | isbn', got {line!r}")
        title, author, isbn = parts
        return cls(title, author, isbn)

    def __str__(self) -> str:
        status = "available" if self.is_available else "checked out"
        return f"'{self.title}' by {self.author} ({status})"