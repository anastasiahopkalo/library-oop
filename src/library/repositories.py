from typing import Protocol

from src.library.book import Book
from src.library.member import Member


class BookReader(Protocol):
    def get(self, isbn: str) -> Book | None: ...
    def all(self) -> tuple[Book, ...]: ...

class BookRepository(BookReader, Protocol):
    def add(self, book: Book) -> None: ...

class MemberReader(Protocol):
    def get(self, member_id: str) -> Member | None: ...
    def all(self) -> tuple[Member, ...]: ...

class MemberRepository(MemberReader, Protocol):
    def add(self, member: Member) -> None: ...

class InMemoryBookRepository:
    def __init__(self) -> None:
        self._books: dict[str, Book] = {}

    def get(self, isbn: str) -> Book | None:
        return self._books.get(isbn)

    def all(self) -> tuple[Book, ...]:
        return tuple(self._books.values())

    def add(self, book: Book) -> None:
        self._books[book.isbn] = book


class InMemoryMemberRepository:
    def __init__(self) -> None:
        self._members: dict[str, Member] = {}

    def get(self, member_id: str) -> Member | None:
        return self._members.get(member_id)

    def all(self) -> tuple[Member, ...]:
        return tuple(self._members.values())

    def add(self, member: Member) -> None:
        self._members[member.member_id] = member