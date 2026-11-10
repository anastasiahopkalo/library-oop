from datetime import date, timedelta

import pytest

from src.library.book import Book
from src.library.library import Library
from src.library.member import Member
from src.library.member_types import PremiumMember, StudentMember

# Список валідних ISBN-13 для тестування
VALID_ISBNS = [
    "9780451524935",
    "9780547928227",
    "9780441172719",
    "9781451673319",
    "9780451524936",
    "9780060850524",
    "9780451526342",
    "9780316769488",
    "9780061120084",
    "9780141439518",
]


def test_student_member_is_instance_of_member() -> None:
    student = StudentMember(name="Bob", member_id="S001", school="KPI")
    assert isinstance(student, Member)


def test_max_books_limits() -> None:
    assert StudentMember.MAX_BOOKS == 2
    assert Member.MAX_BOOKS == 3


def test_student_borrow_limit_leaves_third_book_available() -> None:
    student = StudentMember(name="Bob", member_id="S001", school="KPI")
    b1 = Book(title="Book 1", author="Author 1", isbn=VALID_ISBNS[0])
    b2 = Book(title="Book 2", author="Author 2", isbn=VALID_ISBNS[1])
    b3 = Book(title="Book 3", author="Author 3", isbn=VALID_ISBNS[2])

    student.borrow(b1)
    student.borrow(b2)

    with pytest.raises(ValueError):
        student.borrow(b3)

    assert b3.is_available is True


def test_premium_member_can_borrow_more_than_three_books() -> None:
    premium = PremiumMember(name="Charlie", member_id="P001", annual_fee=100.0)
    books = [
        Book(title=f"Book {i}", author="Author", isbn=VALID_ISBNS[i])
        for i in range(5)
    ]

    for book in books:
        premium.borrow(book)

    assert len(premium.borrowed_books) == 5


@pytest.mark.parametrize(
    "member_instance, expected_limit",
    [
        (Member(name="Alice", member_id="M001"), 3),
        (StudentMember(name="Bob", member_id="S001", school="KPI"), 2),
        (PremiumMember(name="Charlie", member_id="P001", annual_fee=100.0), 10),
    ],
)
def test_member_max_books_parametrized(member_instance: Member, expected_limit: int) -> None:
    assert member_instance.MAX_BOOKS == expected_limit


def test_student_member_repr_format() -> None:
    student = StudentMember(name="Bob", member_id="S001", school="KPI")
    assert repr(student).startswith("StudentMember(")


def test_empty_school_raises_value_error() -> None:
    with pytest.raises(ValueError):
        StudentMember(name="Bob", member_id="S001", school="")
    with pytest.raises(ValueError):
        StudentMember(name="Bob", member_id="S001", school="   ")


def test_negative_annual_fee_raises_value_error() -> None:
    with pytest.raises(ValueError):
        PremiumMember(name="Charlie", member_id="P001", annual_fee=-10.0)


def test_checkout_due_date_calculation() -> None:
    library = Library()
    student = StudentMember(name="Bob", member_id="S001", school="KPI")
    premium = PremiumMember(name="Charlie", member_id="P001", annual_fee=100.0)

    library.register_member(student)
    library.register_member(premium)

    b1 = Book(title="Book 1", author="Author 1", isbn=VALID_ISBNS[0])
    b2 = Book(title="Book 2", author="Author 2", isbn=VALID_ISBNS[1])
    library.add_book(b1)
    library.add_book(b2)

    student_due = library.checkout(student.member_id, b1.isbn)
    assert student_due == date.today() + timedelta(days=student.LOAN_DAYS)

    premium_due = library.checkout(premium.member_id, b2.isbn)
    assert premium_due == date.today() + timedelta(days=premium.LOAN_DAYS)


def test_active_loans_tracking() -> None:
    library = Library()
    member = Member(name="Alice", member_id="M001")
    book = Book(title="Book 1", author="Author 1", isbn=VALID_ISBNS[0])

    library.register_member(member)
    library.add_book(book)

    library.checkout(member.member_id, book.isbn)
    assert len(library.active_loans) == 1
    assert library.active_loans[0].book == book

    library.return_book(member.member_id, book.isbn)
    assert len(library.active_loans) == 0


def test_loans_for_returns_only_target_member_loans() -> None:
    library = Library()
    m1 = Member(name="Alice", member_id="M001")
    m2 = Member(name="Bob", member_id="M002")

    b1 = Book(title="Book 1", author="Author 1", isbn=VALID_ISBNS[0])
    b2 = Book(title="Book 2", author="Author 2", isbn=VALID_ISBNS[1])

    library.register_member(m1)
    library.register_member(m2)
    library.add_book(b1)
    library.add_book(b2)

    library.checkout(m1.member_id, b1.isbn)
    library.checkout(m2.member_id, b2.isbn)

    m1_loans = library.loans_for(m1.member_id)
    assert len(m1_loans) == 1
    assert m1_loans[0].member_id == m1.member_id
    assert m1_loans[0].book == b1


def describe_all(members: list[Member]) -> list[str]:
    return [str(member) for member in members]


def test_describe_all_polymorphism() -> None:
    members: list[Member] = [
        Member(name="Alice", member_id="M001"),
        StudentMember(name="Bob", member_id="S001", school="KPI"),
        PremiumMember(name="Charlie", member_id="P001", annual_fee=100.0),
    ]

    descriptions = describe_all(members)
    assert len(descriptions) == 3
    assert any("Alice" in d for d in descriptions)
    assert any("Bob" in d for d in descriptions)
    assert any("Charlie" in d for d in descriptions)
