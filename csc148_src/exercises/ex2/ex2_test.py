"""CSC148 Exercise 2: Inheritance and Introduction to Stacks

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Exercise 2.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

For more information on hypothesis (one of the testing libraries we're using),
please see
<http://www.teach.cs.toronto.edu/~csc148h/fall/software/hypothesis.html>.

Note: this file is for support purposes only, and is not part of your
submission.
"""
from hypothesis import given, assume
from hypothesis.strategies import integers, text

from ex2 import SuperDuperManager, reverse_top_two
from obfuscated_stack import Stack

from math import ceil, sqrt


##############################################################################
# Task 1: Cars and other vehicles
##############################################################################
@given(text(min_size=1), integers(min_value=1, max_value=100000))
def test_new_car_attributes(id_, fuel):
    manager = SuperDuperManager()
    manager.add_vehicle('Car', id_, fuel)
    assert manager.get_vehicle_fuel(id_) == fuel
    assert manager.get_vehicle_position(id_) == (0, 0)


@given(text(min_size=1), integers(min_value=1, max_value=100000))
def test_new_helicopter_attributes(id_, fuel):
    manager = SuperDuperManager()
    manager.add_vehicle('Helicopter', id_, fuel)
    assert manager.get_vehicle_fuel(id_) == fuel
    assert manager.get_vehicle_position(id_) == (3, 5)


@given(text(min_size=1), integers(min_value=1, max_value=100000))
def test_new_carpet_attributes(id_, fuel):
    manager = SuperDuperManager()
    manager.add_vehicle('UnreliableMagicCarpet', id_, fuel)
    assert manager.get_vehicle_fuel(id_) == fuel
    pos = manager.get_vehicle_position(id_)
    assert abs(pos[0]) <= 10
    assert abs(pos[1]) <= 10


@given(text(min_size=1), integers(min_value=1),
       integers(min_value=-200, max_value=200),
       integers(min_value=-200, max_value=200))
def test_move_car_changes_attributes(id_, fuel, new_x, new_y):
    # Similar to an assert: retries test when this property is false
    assume(abs(new_x) + abs(new_y) <= fuel)

    manager = SuperDuperManager()
    manager.add_vehicle('Car', id_, fuel)
    manager.move_vehicle(id_, new_x, new_y)
    assert manager.get_vehicle_position(id_) == (new_x, new_y)
    assert manager.get_vehicle_fuel(id_) == fuel - abs(new_x) - abs(new_y)

@given(text(min_size=1),
       integers(min_value=-200, max_value=200),
       integers(min_value=-200, max_value=200))
def test_move_car_no_fuel(id_, new_x, new_y):
    # Similar to an assert: retries test when this property is false

    manager = SuperDuperManager()
    manager.add_vehicle('Car', id_, 0)
    manager.move_vehicle(id_, new_x, new_y)
    assert manager.get_vehicle_position(id_) == (0,0)



@given(text(min_size=1), integers(min_value=1),
       integers(min_value=-200, max_value=200),
       integers(min_value=-200, max_value=200))
def test_move_magic_carpet(id_, fuel, new_x, new_y):
    # Similar to an assert: retries test when this property is false

    manager = SuperDuperManager()
    manager.add_vehicle('UnreliableMagicCarpet', id_, fuel)
    manager.move_vehicle(id_, new_x, new_y)
    result_x, result_y = manager.get_vehicle_position(id_)

    assert abs(new_x - result_x) <= 2
    assert abs(new_y - result_y) <= 2

    assert manager.get_vehicle_fuel(id_) == fuel


@given(text(min_size=1), integers(min_value=1),
       integers(min_value=-200, max_value=200),
       integers(min_value=-200, max_value=200))
def test_move_heli(id_, fuel, new_x, new_y) -> None:
    # Similar to an assert: retries test when this property is false
    dx = abs(new_x - 3)
    dy = abs(new_y - 5)
    assume(int(ceil(sqrt(dx ** 2 + dy ** 2))) <= fuel)

    manager = SuperDuperManager()
    manager.add_vehicle('Helicopter', id_, fuel)
    manager.move_vehicle(id_, new_x, new_y)
    assert manager.get_vehicle_position(id_) == (new_x, new_y)
    assert manager.get_vehicle_fuel(id_) \
        == fuel - int(ceil(sqrt(dx ** 2 + dy ** 2)))


@given(text(min_size=1),
       integers(min_value=-200, max_value=200),
       integers(min_value=-200, max_value=200))
def test_move_heli_no_fuel(id_, new_x, new_y) -> None:
    # Similar to an assert: retries test when this property is false
    dx = abs(new_x - 3)
    dy = abs(new_y - 5)

    manager = SuperDuperManager()
    manager.add_vehicle('Helicopter', id_, 0)
    manager.move_vehicle(id_, new_x, new_y)
    assert manager.get_vehicle_position(id_) == (3, 5)
    assert manager.get_vehicle_fuel(id_) == 0


@given(text(min_size=1), integers(min_value=-200, max_value=200),
       integers(min_value=-200, max_value=200))
def test_move_magic_carpet_no_fuel(id_, new_x, new_y):
    # Similar to an assert: retries test when this property is false

    manager = SuperDuperManager()
    manager.add_vehicle('UnreliableMagicCarpet', id_, 0)
    manager.move_vehicle(id_, new_x, new_y)
    result_x, result_y = manager.get_vehicle_position(id_)

    assert abs(new_x - result_x) <= 2
    assert abs(new_y - result_y) <= 2

    assert manager.get_vehicle_fuel(id_) == 0
##############################################################################
# Task 2: Introduction to Stacks
##############################################################################
def test_simple_reverse_top_two():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    reverse_top_two(stack)
    assert stack.pop() == 1
    assert stack.pop() == 2
    assert stack.is_empty()


if __name__ == '__main__':
    import pytest
    pytest.main()