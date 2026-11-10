class Animal:
    def __init__(self, name: str) -> None:
        self._name = name

    def speak(self) -> str:
        return '. . .'

    def describe(self) -> str:
        return f"{self._name} says {self.speak()}"

class Dog(Animal):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def speak(self) -> str:
        return "Bark"

class Cat(Animal):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def speak(self) -> str:
        return 'Meow'

class Puppy(Dog):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def speak(self) -> str:
        return super().speak() + "!!!"

animals : list[Animal] = [Dog("Bobik"), Cat("Kytsya"), Puppy("Bobichek"), Animal("General")]
for animal in animals:
    print(animal.describe())

