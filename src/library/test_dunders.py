from src.library.book import Book
from src.library.library import Library
from src.library.member import RegularMember


def test_member_equality_and_hashing() -> None:
    m1 = RegularMember("Alice Smith", "M001")
    m2 = RegularMember("Alice Johnson", "M001")

    assert m1 == m2
    assert hash(m1) == hash(m2)

    member_set = {m1, m2}
    assert len(member_set) == 1

def test_sorted_members_orders_by_name_case_insensitive() -> None:
    m1 = RegularMember("charlie", "M003")
    m2 = RegularMember("Alice", "M001")
    m3 = RegularMember("bob", "M002")

    sorted_list = sorted([m1, m2, m3])
    assert [m.name for m in sorted_list] == ["Alice", "bob", "charlie"]

def test_library_dunders_len_contains_list_and_truthiness() -> None:
    library = Library()

    assert len(library) == 0
    assert not library

    b1 = Book("Dune", "Frank Herbert", "9780441172719")
    b2 = Book("1984", "George Orwell", "9780451524936")

    library.add_book(b1)
    library.add_book(b2)

    assert len(library) == 2
    assert bool(library) is True
    assert "9780441172719" in library
    assert "0000000000" not in library
    assert list(library) == [b1, b2]

def test_library_iterating_twice_yields_same_books() -> None:
    library = Library()
    b1 = Book("Dune", "Frank Herbert", "9780441172719")
    b2 = Book("1984", "George Orwell", "9780451524936")

    library.add_book(b1)
    library.add_book(b2)

    first_pass = list(library)
    second_pass = list(library)

    assert first_pass == second_pass == [b1, b2]