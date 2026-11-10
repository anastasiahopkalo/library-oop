from dataclasses import dataclass
from datetime import date

from src.library.book import Book


@dataclass(frozen=True)
class Loan:
    book: Book
    member_id: str
    due_date: date
