from datetime import date
from decimal import Decimal
from typing import Protocol
from src.library.loan import Loan
from src.library.exceptions import ValidationError

class FineCalculator(Protocol):
    def calculate(self, loan: Loan, returned_on: date) -> Decimal: ...

class FlatRateFineCalculator:
    def __init__(self, rate_per_day: Decimal = Decimal("0.50")) -> None:
        if rate_per_day < Decimal("0"):
            raise ValidationError("Fine rate per day cannot be negative")
        self.rate_per_day = rate_per_day
    def calculate(self, loan: Loan, returned_on: date) -> Decimal:
        days_late = max(0, (returned_on - loan.due_date).days)
        return self.rate_per_day * days_late