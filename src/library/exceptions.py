class LibraryError(Exception):
    """Base class for all library errors."""


class ValidationError(LibraryError, ValueError):
    """Bad input data (empty name, invalid ISBN...)."""


class NotFoundError(LibraryError):
    """Base class for lookup failures."""


class BookNotFoundError(NotFoundError):
    """Raised when a book with the given ISBN is not found.

    Carries: .isbn
    """

    def __init__(self, isbn: str):
        self.isbn = isbn
        super().__init__(f"Book with ISBN '{isbn}' was not found.")


class MemberNotFoundError(NotFoundError):
    """Raised when a member with the given ID is not found.

    Carries: .member_id
    """

    def __init__(self, member_id: str):
        self.member_id = member_id
        super().__init__(f"Member with ID '{member_id}' was not found.")


class DuplicateError(LibraryError):
    """Raised when an item with identical ISBN or member_id already exists."""


class BookUnavailableError(LibraryError):
    """Raised when attempting to borrow a book that is already checked out.

    Carries: .book
    """

    def __init__(self, book: object) -> None:
        self.book = book
        title = getattr(book, "title", str(book))
        super().__init__(f"Book '{title}' is currently unavailable for borrowing.")


class BorrowLimitError(LibraryError):
    """Raised when a member reaches their maximum borrowing limit.

    Carries: .member, .limit
    """

    def __init__(self, member: object, limit: int) -> None:
        self.member = member
        self.limit = limit
        name = getattr(member, "name", str(member))
        super().__init__(f"Member '{name}' has reached the borrowing limit of {limit} books.")


class NotBorrowedError(LibraryError):
    """Raised when trying to return a book that was not borrowed by the member.

    Carries: .member, .book
    """

    def __init__(self, member: object, book: object) -> None:
        self.member = member
        self.book = book
        name = getattr(member, "name", str(member))
        title = getattr(book, "title", str(book))
        super().__init__(f"Book '{title}' was not borrowed by member '{name}'.")