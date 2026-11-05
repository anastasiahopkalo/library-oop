class Book:
    def __init__(self, title: str, author : str, isbn : str) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_available = True
    def __str__(self) -> str:
        status = "available" if self.is_available else "checked out"
        return f"'{self.title}' by {self.author} ({status})"
    def __repr__(self) -> str:
        return f"Book(title={self.title!r}, author={self.author!r}, isbn={self.isbn!r})"