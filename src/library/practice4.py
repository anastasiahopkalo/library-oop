import math
from abc import ABC, abstractmethod
from functools import total_ordering


@total_ordering
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    def describe(self) -> str:
        return f"{type(self).__name__} with area {self.area():.2f}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return math.isclose(self.area(), other.area())

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Shape):
            return NotImplemented
        return self.area() < other.area()

class Square(Shape):
    def __init__(self, side: float):
        if side < 0:
            raise ValueError("Side length cannot be negative.")
        self.side = side

    def area(self) -> float:
        return self.side ** 2

class Circle(Shape):
    def __init__(self, radius: float):
        if radius < 0:
            raise ValueError("Radius cannot be negative.")
        self.radius = radius

    def area(self) -> float:
        return math.pi * (self.radius ** 2)

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        if width < 0 or height < 0:
            raise ValueError("Dimensions cannot be negative.")
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

if __name__ == "__main__":
    shapes = [
        Circle(radius=3),
        Square(side=4),
        Rectangle(2, 5),
        Square(side=1)
    ]
    sorted_shapes = sorted(shapes)
    for s in sorted_shapes:
        print(f"{s.__class__.__name__}: {s.area():.2f}")

    largest = max(shapes)
    print(f"Max: {largest.describe()}")
