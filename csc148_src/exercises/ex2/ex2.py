"""CSC148 Exercise 2: Inheritance and Introduction to Stacks

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This file contains starter code for Exercise 2.
It is divided into two parts:
- Task 1, which contains a set of classes that build on your work from
  last week.
- Task 2, which contains the skeleton of a simple function involving a new
  data structure, the *Stack*.

Notes:
  1. When you override a method, you can generally just copy the docstring from
     the superclass. However, you should add doctests, which may be omitted
     in the original method when the superclass is abstract.
  2. A lot of starter code has been provided! Read through it carefully
     before starting. You may also find it interesting to compare our work
     against what you did for Exercise 1.
"""
# You will find these imports useful. Please do not import any others.
from math import sqrt, floor
import random  # used to generate random numbers
from typing import Dict, Optional, Tuple


##############################################################################
# Task 1: Cars and other vehicles
##############################################################################
class SuperDuperManager:
    """A class responsible for keeping track of all cars in the system.

    NOTE: Unlike last week, you should not be making any changes to this class.
    Instead, look at how it's using the Vehicle interface and the initializers
    for the three required subclasses.
    """
    # === Private Attributes ===
    # _vehicles:
    #     A map of unique string identifiers to the corresponding vehicles.
    #     For example, _vehicles['car1'] would be a vehicle corresponding to
    #     the id_ 'car1'.
    _vehicles: Dict[str, 'Vehicle']

    def __init__(self) -> None:
        """Initialize a new SuperDuperManager.

        There are no vehicles in the system when first created.
        """
        self._vehicles = {}

    def add_vehicle(self, vehicle_type: str, id_: str, fuel: int) -> None:
        """Add a new vehicle to the system of the given type.

        The new vehicle is identified by the string <id_>,
        and has initial amount of fuel <fuel>.

        Do nothing if there is already a vehicle with the given id.

        Preconditions:
          - <vehicle_type> is one of 'Car', 'Helicopter', or
            'UnreliableMagicCarpet'.
          - fuel >= 0

        NOTE: you'll need to override the initializer for each of the three
        Vehicle subclasses in order to make them compatible with this method.
        That should be your first step (otherwise you won't be able to add
        any cars to this system).
        """
        # Check to make sure the identifier isn't already used.
        if id_ not in self._vehicles:
            if vehicle_type == 'Car':
                self._vehicles[id_] = Car(fuel)
            elif vehicle_type == 'Helicopter':
                self._vehicles[id_] = Helicopter(fuel)
            elif vehicle_type == 'UnreliableMagicCarpet':
                self._vehicles[id_] = UnreliableMagicCarpet(fuel)

    def move_vehicle(self, id_: str, new_x: int, new_y: int) -> None:
        """Move a vehicle with the given id.

        The vehicle called <id_> should be moved to position (<new_x>, <new_y>).
        Do nothing if there is no vehicle with the given id,
        or if the corresponding vehicle does not have enough fuel to move.
        """
        if id_ in self._vehicles:
            self._vehicles[id_].move(new_x, new_y)

    def get_vehicle_position(self, id_: int) -> Optional[Tuple[int, int]]:
        """Return the position of the vehicle with the given id.

        Return a tuple of the (x, y) position of the vehicle.
        Return None if there is no vehicle with the given id.
        """
        if id_ in self._vehicles:
            return self._vehicles[id_].position

    def get_vehicle_fuel(self, id_: str) -> Optional[int]:
        """Return the amount of fuel of the vehicle with the given id.

        Return None if there is no vehicle with the given id.
        """
        if id_ in self._vehicles:
            return self._vehicles[id_].fuel


class Vehicle:
    """An interface for a vehicle in the Super Duper system.

    Note that this interface specifies *two* public attributes,
    and *two* public methods (the initializer is not considered public).

    Of the public methods, a default implementation is given for move,
    but not fuel_needed.

    It also defines a constructor that should be called by each of its
    subclasses.

    === Attributes ===
    position:
        The position of this vehicle.
    fuel:
        The amount of fuel remaining for this vehicle.

    === Representation invariants ===
    - fuel >= 0
    """
    position: Tuple[int, int]
    fuel: int

    def __init__(self, new_fuel: int, new_position: Tuple[int, int]) -> None:
        """Initialize a new Vehicle with the given fuel and position.

        Precondition: new_fuel >= 0
        """
        self.fuel = new_fuel
        self.position = new_position

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        """Return how much fuel would be used to move to the given position.

        Note: the amount returned may be larger than self.fuel,
        indicating that this vehicle may not move to the given position.
        """
        raise NotImplementedError

    def move(self, new_x: int, new_y: int) -> None:
        """Move this vehicle to a new position.

        Do nothing if this vehicle does not have enough fuel to move
        to the specified position.
        """
        needed = self.fuel_needed(new_x, new_y)
        if needed <= self.fuel:
            self.position = (new_x, new_y)
            self.fuel -= needed


class Car(Vehicle):
    """A car in the Super system.

    === Public attributes ===
    x: the x-coordinate of this car's position
    y: the y-coordinate of this car's position

    === Public properties ===
    fuel: the amount of fuel remaining this car has remaining
    position: The position of the car in a tuple (x, y)

    === Representation invariants ===
    fuel >= 0
    """

    def __init__(self, fuel: int = 0, x: int = 0, y: int = 0):
        super().__init__(fuel, (x, y))

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        """
        Gets the distance from the car's current position to a target position.
        :param new_x: The target x-coordinate.
        :param new_y: The target y-coordinate.
        :return: The distance to the target position
                 from the car's current position.
        """
        x, y = self.position
        return abs(new_x - x) + abs(new_y - y)


class Helicopter(Vehicle):
    """A helicopter. Can travel diagonally between points."""

    def __init__(self, fuel: int):
        super().__init__(fuel, (3, 5))

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        """

        :param new_x:
        :param new_y:
        :return:
        """
        x, y = self.position
        dx = abs(new_x - x)
        dy = abs(new_y - y)
        distance = sqrt(dx ** 2 + dy ** 2)

        # Why floor?
        rounding = 1 if distance % 1 != 0 else 0
        return int(floor(sqrt(dx ** 2 + dy ** 2))) + rounding


class UnreliableMagicCarpet(Vehicle):
    """An unreliable magic carpet.

    Does not need to use fuel to travel, but ends up in a random position
    within two horizontal and two vertical units from the target destination.
    """

    def __init__(self, fuel: int):
        super().__init__(fuel, (random.randint(-10, 10),
                                random.randint(-10, 10)))

    def fuel_needed(self, new_x: int, new_y: int) -> int:
        """
        The magic carpet does not need fuel.
        :param new_x:
        :param new_y:
        :return:
        """
        return 0

    def move(self, new_x: int, new_y: int) -> None:
        """Move this vehicle to a new position.

        """
        self.position = (new_x + random.randint(-2, 2),
                         new_y + random.randint(-2, 2))


##############################################################################
# Task 2: Introduction to Stacks
##############################################################################
def reverse_top_two(stack: 'Stack') -> None:
    """Reverse the top two elements on <stack>.

    Precondition: <stack> has at least two items.

    >>> from obfuscated_stack import Stack
    >>> stack = Stack()
    >>> stack.push(1)
    >>> stack.push(2)
    >>> reverse_top_two(stack)
    >>> stack.pop()
    1
    >>> stack.pop()
    2
    """
    top_item = stack.pop()
    bottom_item = stack.pop()
    stack.push(top_item)
    stack.push(bottom_item)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    # Uncomment and run before final submission. This checks for style errors
    # in addition to code inconsistencies and forbidden Python features.
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'math', 'random', 'obfuscated_stack'
        ]
    })
