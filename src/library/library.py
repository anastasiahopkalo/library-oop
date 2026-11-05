from src.library.book import Book
from src.library.member import Member


class Library:
    def __init__(self)-> None:
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
    def add_book(self, book: Book)-> None:
        self.books[book.isbn] = book
    def register_member(self, member: Member)-> None:
        self.members[member.member_id] = member
    def find_book_by_title(self,title : str) -> Book | None:
        for book in self.books.values():
            if book.title == title:
                return book
        return None
    def checkout(self, member_id : str, isbn: str) -> None:
        if member_id not in self.members:
            raise ValueError(f"Member {member_id} not available")
        if isbn not in self.books:
            raise ValueError(f"ISBN {isbn} not available")
        member = self.members[member_id]
        book = self.books[isbn]
        if not book.is_available:
            raise ValueError(f"Book {isbn} is not available")
        member.borrow(book)
        book.is_available = False

    def return_book(self, member_id: str, isbn: str) -> None:
        if member_id not in self.members:
            raise ValueError(f"Member {member_id} not available")
        if isbn not in self.books:
            raise ValueError(f"ISBN {isbn} not available")
        member = self.members[member_id]
        book = self.books[isbn]
        member.return_book(book)
        book.is_available = True

