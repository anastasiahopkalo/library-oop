from collections.abc import Callable
import pytest

from src.library.book import Book
from src.library.member import Member, RegularMember
from src.library.member_types import PremiumMember, StudentMember
from src.library.staff import StaffMember

MEMBER_FACTORIES: list[Callable[[], Member]] = [
    lambda: RegularMember(name="Alice", member_id="M1"),
    lambda: StudentMember(name="Bohdan", member_id="M2", school="KNU"),
    lambda: PremiumMember(name="Clara", member_id="M3", annual_fee=100.0),
    lambda: StaffMember(name="Dr. Dmytro", member_id="S1"),
]


@pytest.mark.parametrize("make_member", MEMBER_FACTORIES)
def test_member_lsp_contract(make_member: Callable[[], Member]) -> None:
    member = make_member()
    book = Book(isbn="978-0132350884", title="Clean Code", author="Robert C. Martin")

    assert member.MAX_BOOKS >= 1
    assert member.LOAN_DAYS >= 1
    assert isinstance(member.membership_type, str) and member.membership_type

    member.borrow(book)
    assert book in member.borrowed_books

    member.return_book(book)
    assert book not in member.borrowed_books