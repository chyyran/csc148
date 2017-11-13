"""CSC148 Exercise 1: Basic Object-Oriented Programming

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for Exercise 1.
It contains two classes that work together:
- SuperDuperManager, which manages all the cars in the system
- Car, a class which represents a single car in the system

Your task is to design and implement the Car class, and then modify the
SuperDuperManager methods so that they make proper use of the Car class.

You may not modify the public interface of any of the SuperDuperManager methods.
We have marked the parts of the code you should change with TODOs, which you
should remove once you've completed them.

Notes:
  1. We'll talk more about private attributes on Friday's class.
     For now, treat them the same as any other instance attribute.
  2. You'll notice we use a trailing underscore for the parameter name
     "id_" in a few places. It is used to avoid conflicts with Python
     keywords. Here we want to have a parameter named "id", but that is
     already the name of a built-in function. So we call it "id_" instead.
"""
from typing import Dict, Optional, Tuple


class SuperDuperManager:
    """A class that keeps track of all cars in the Super Duper system.
    """
    # === Private Attributes ===
    # _cars:
    #   A map of unique string identifiers to the corresponding Car.
    #   For example, _cars['car1'] would be a Car object corresponding to
    #   the id 'car1'.
    _cars: Dict[str, 'Car']

    def __init__(self) -> None:
        """Initialize a new SuperDuperManager.

        There are no cars in the system when first created.
        """
        self._cars = {}

    def add_car(self, id_: str, fuel: int) -> None:
        """Add a new car to the system.

        The new car is identified by the string <id_>, and has initial amount
        of fuel <fuel>.

        Do nothing if there is already a car with the given id.

        Precondition: fuel >= 0.
        """
        # Check to make sure the identifier isn't already used.
        if id_ not in self._cars:
            self._cars[id_] = Car(fuel)

    def move_car(self, id_: str, new_x: int, new_y: int) -> None:
        """Move the car with the given id.

        The car called <id_> should be moved to position (<new_x>, <new_y>).
        Do nothing if there is no car with the given id,
        or if the corresponding car does not have enough fuel.
        """
        if id_ in self._cars:
            car = self._cars[id_]
            if car.fuel <= 0:
                pass
            car.move(new_x, new_y)

    def get_car_position(self, id_: str) -> Optional[Tuple[int, int]]:
        """Return the position of the car with the given id.

        Return a tuple of the (x, y) position of the car with id <id_>.
        Return None if there is no car with the given id.
        """
        if id_ in self._cars:
            car = self._cars[id_]
            return car.position

    def get_car_fuel(self, id_: str) -> Optional[int]:
        """Return the amount of fuel of the car with the given id.

        Return None if there is no car with the given id.
        """
        if id_ in self._cars:
            car = self._cars[id_]
            return car.fuel

    def dispatch(self, x: int, y: int) -> None:
        """Move a car to the given location.

        Choose a car to move based on the following criteria:
        (1) Only consider cars that *can* move to the location.
            (Ignore ones that don't have enough fuel.)
        (2) After (1), choose the car that would move the *least* distance to
            get to the location.
        (3) If there is a tie in (2), pick the car whose id comes first
            alphabetically. Use < and/or > to compare the strings.
        (4) If no cars can move to the given location, do nothing.
        """

        eligible_cars = sorted(
            # Iterate over key/value pairs in car.
            [(id_, car) for id_, car in self._cars.items()
             # Consider only if the car can move to the location (1).
             if car.can_move_to(x, y)],
            # Sort by the distance, then the ID. (2), (3).
            key=lambda kvp: (kvp[1].get_distance_to(x, y), kvp[0])
        )

        if len(eligible_cars) == 0:  # Do nothing if there are no cars (4)
            return

        eligible_cars[0][1].move(x, y)


class Car:
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
    x: int
    y: int
    __fuel: int

    def __init__(self, fuel: int = 0, x: int = 0, y: int = 0):
        self.fuel = fuel
        self.position = (x, y)

    @property
    def position(self) -> (int, int):
        """
        Gets the current position of the car as a tuple (x, y)
        :return: The current position of the car as a tuple (x, y)
        """
        return self.x, self.y

    @position.setter
    def position(self, position: (int, int)) -> None:
        """
        Sets the position of the car without any checks.
        :param position: The position of the car in a tuple (x, y).
        """
        self.x, self.y = position

    @property
    def fuel(self) -> int:
        """
        Gets the remaining fuel units of the car.
        :return: The remaining fuel units of the car.
        """
        return self.__fuel

    @fuel.setter
    def fuel(self, fuel: int) -> None:
        """
        Sets the amount of fuel units of the car.
        :param fuel: The new amount of fuel units.
                     Must be greater or equal to 0.
        :raises: ValueError: If fuel is a negative number.

        === Representational Invariants===
        fuel >= 0
        """
        if fuel < 0:
            raise ValueError("Fuel must be greater or less than zero.")
        self.__fuel = fuel

    def can_move_to(self, x: int, y: int) -> bool:
        """
        Determines whether or not the car is able to move to a given position
        :param x: The x co-ordinate of the new position
        :param y: The y co-ordinate of the new position
        :return: Whether or not the car is able to move to the given position
        """
        remaining_fuel = self.__calc_remaining_fuel(x, y)
        return remaining_fuel >= 0

    def move(self, x: int, y: int) -> None:
        """
        Moves the car to the given position, consuming fuel units
        in the process.
        If the car can not move to the new position, the car will not be moved.
        :param x: The x co-ordinate of the new position
        :param y: The y co-ordinate of the new position
        """

        # If the car can not move to the new position, then fail silently
        if not self.can_move_to(x, y):
            return

        remaining_fuel = self.__calc_remaining_fuel(x, y)
        self.fuel = remaining_fuel
        self.position = (x, y)

    def get_distance_to(self, new_x: int, new_y: int) -> int:
        """
        Gets the distance from the car's current position to a target position.
        :param new_x: The target x-coordinate.
        :param new_y: The target y-coordinate.
        :return: The distance to the target position
                 from the car's current position.
        """
        x, y = self.position
        return abs(new_x - x) + abs(new_y - y)

    def __calc_remaining_fuel(self, x: int, y: int) -> int:
        """
        Calculates the amount of fuel units remaining
        after a trip to the given position.
        :param x: The target x-coordinate.
        :param y: The target y-coordinate.
        :return: The amount of fuel units remaining
                 after a trip to the given position.
        """
        fuel_cost = self.get_distance_to(x, y)
        return self.fuel - fuel_cost


if __name__ == '__main__':
    # Run python_ta to ensure this module passes all checks for
    # code inconsistencies and forbidden Python features.
    # Useful for debugging!
    import python_ta

    python_ta.check_all()
