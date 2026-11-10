from src.library.member import Member


class StudentMember(Member):
    MAX_BOOKS = 2
    LOAN_DAYS = 14

    def __init__(self, name: str, member_id: str, school: str) -> None:
        super().__init__(name, member_id)
        self.school = school

    @property
    def school(self) -> str:
        return self._school

    @school.setter
    def school(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("School cannot be empty")
        self._school = value

class PremiumMember(Member):
    MAX_BOOKS = 10
    LOAN_DAYS = 30
    def __init__(self, name: str, member_id: str, annual_fee: float) -> None:
        super().__init__(name, member_id)
        self.annual_fee = annual_fee

    @property
    def annual_fee(self) -> float:
        return self._annual_fee

    @annual_fee.setter
    def annual_fee(self, value: float) -> None:
        if value < 0 :
            raise ValueError("Annual fee cannot be negative")
        self._annual_fee = value

    def __repr__(self) -> str:
        return super().__repr__() + f", annual_fee={self.annual_fee}"