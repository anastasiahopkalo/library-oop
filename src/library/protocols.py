from typing import Protocol


class HasDescribe(Protocol):
    def describe(self) -> str:
        ...