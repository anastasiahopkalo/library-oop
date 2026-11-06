from dataclasses import dataclass, field
from typing import Self


class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        if not self.is_valid_dimension(value):
            raise ValueError("Width must be positive")
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        if not self.is_valid_dimension(value):
            raise ValueError("Height must be positive")
        self._height = value

    @property
    def area(self) -> float:
        return self.width * self.height

    @classmethod
    def square (cls, side: float) -> Self :
        return cls(side, side)

    @staticmethod
    def is_valid_dimension(value: float) -> bool:
        return value >= 0

@dataclass(frozen = True)
class Item:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.price < 0:
            raise ValueError("Price must be positive")