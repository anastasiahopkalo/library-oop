class BankAccount:
    bank_name = "PyBank"

    def __init__(self, owner: str, balance: float = 0.0) -> None:
        self.owner = owner
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

    def __str__(self) -> str:
        return f"{self.owner}: ${self.balance:.2f}"

    def __repr__(self) -> str:
        return f"BankAccount(owner={self.owner!r}, balance={self.balance!r})"
class Bad :
    def __init__(self, items: list[int]| None = None) -> None:
        self.items = items if items is not None else []
class Shared:
    def __init__ (self, tags : list[str]| None = None) -> None:
        self.tags = tags if tags is not None else []
s1, s2 = Shared(), Shared()
s1.tags.append("a")
print(s2.tags)
