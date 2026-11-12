from typing import ClassVar

from src.library.member import Member


class StaffMember(Member):
    MAX_BOOKS: ClassVar[int] = 20
    LOAN_DAYS: ClassVar[int] = 60

    @property
    def membership_type(self) -> str:
        return "staff"