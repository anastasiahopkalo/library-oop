from src.library.book import Book


class Member:
    MAX_BOOKS = 3

    def __init__ (self, name: str, member_id :str) -> None:
        self.name = name
        self.member_id = member_id
        self.borrowed_books : list[Book] = []

    def borrow (self, book : Book) -> None:
        if len(self.borrowed_books) >= self.MAX_BOOKS:
            raise ValueError(f"{self.name} reached the limit of {self.MAX_BOOKS} books")
        self.borrowed_books.append(book)

    def return_book(self, book : Book) -> None:
        if book not in self.borrowed_books:
            raise ValueError("This member did not borrow that book")
        self.borrowed_books.remove(book)

    def __repr__ (self) -> str:
        return f"Member(name={self.name!r}, member_id={self.member_id!r})"

