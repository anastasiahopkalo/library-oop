from datetime import date, timedelta
from decimal import Decimal

import pytest

from src.library.book import Book
from src.library.exceptions import ValidationError
from src.library.fines import FlatRateFineCalculator
from src.library.library import Library
from src.library.loan import Loan
from src.library.member import RegularMember


def test_return_on_time_gives_zero_fine() -> None:
    current_day = date(2026, 11, 1)
    lib = Library(clock=lambda: current_day)
    member = RegularMember(name="Alice", member_id="M1")
    book = Book(isbn="978-0132350884", title="Clean Code", author="Robert Martin")

    lib.register_member(member)
    lib.add_book(book)
    due_date = lib.checkout("M1", book.isbn)

    current_day = due_date
    fine = lib.return_book("M1", book.isbn)

    assert fine == Decimal("0.00")

def test_return_three_days_late_gives_expected_fine() -> None:
    current_day = date(2026, 11, 1)
    lib = Library(
        fines=FlatRateFineCalculator(Decimal("0.50")),
        clock=lambda: current_day,
    )
    member = RegularMember(name="Alice", member_id="M1")
    book = Book(isbn="978-0132350884", title="Clean Code", author="Robert Martin")

    lib.register_member(member)
    lib.add_book(book)
    due_date = lib.checkout("M1", book.isbn)

    current_day = due_date + timedelta(days=3)
    fine = lib.return_book("M1", book.isbn)

    assert fine == Decimal("1.50")

def test_flat_rate_fine_calculator_standalone() -> None:
    calc = FlatRateFineCalculator(Decimal("0.50"))
    book = Book(isbn="978-0132350884", title="Clean Code", author="Robert Martin")
    due = date(2026, 11, 10)
    loan = Loan(book=book, member_id="M1", due_date=due)

    assert calc.calculate(loan, date(2026, 11, 8)) == Decimal("0.00")
    assert calc.calculate(loan, date(2026, 11, 10)) == Decimal("0.00")
    assert calc.calculate(loan, date(2026, 11, 14)) == Decimal("2.00")

def test_flat_rate_calculator_rejects_negative_rate() -> None:
    with pytest.raises(ValidationError):
        FlatRateFineCalculator(Decimal("-0.01"))

def test_dip_stub_fine_calculator() -> None:
    class StubFineCalculator:
        def calculate(self, loan: Loan, returned_on: date) -> Decimal:
            return Decimal("9.99")

    lib = Library(fines=StubFineCalculator())
    member = RegularMember(name="Alice", member_id="M1")
    book = Book(isbn="978-0132350884", title="Clean Code", author="Robert Martin")

    lib.register_member(member)
    lib.add_book(book)
    lib.checkout("M1", book.isbn)
    assert lib.return_book("M1", book.isbn) == Decimal("9.99")


