"""CSC148 Lab 4: Abstract Data Types

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
In this module, you will develop an implementation of a new ADT, the Queue.
It will be helpful to review the stack implementation from lecture.

After you've implemented the Queue, you'll write two different functions that
operate on a Queue, paying attention to whether or not the queue should be
modified.
"""
from typing import Generic, List, TypeVar, Optional

# Ignore this line; it is only used to facilitate PyCharm's typechecking.
T = TypeVar('T')


class Queue(Generic[T]):
    """Queue implementation.

    Stores data in first-in, first-out order.
    When removing an item from the queue, the one which was added first
    is removed.
    """

    __items: List[T]

    def __init__(self) -> None:
        self.__items = []

    def is_empty(self) -> bool:
        """Return True iff this Queue is empty.

        >>> q = Queue()
        >>> q.is_empty()
        True
        >>> q.enqueue('hello')
        >>> q.is_empty()
        False
        """
        return len(self.__items) == 0

    def enqueue(self, item: T) -> None:
        """Add <item> to the back of this Queue.
        """
        self.__items.append(item)

    def dequeue(self) -> Optional[T]:
        """Remove and return the item at the front of this Queue.

        Return None if this Queue is empty.

        >>> q = Queue()
        >>> q.enqueue('hello')
        >>> q.enqueue('goodbye')
        >>> q.dequeue()
        'hello'
        """
        # Note: this is slow, better to use collections.deque for popleft.

        return None if self.is_empty() else self.__items.pop(0)


def product(integer_queue: Queue[int]) -> int:
    """Return the product of integers in the Queue.

    Postcondition: integer_queue.is_empty() == True

    >>> q = Queue()
    >>> q.enqueue(2)
    >>> q.enqueue(4)
    >>> q.enqueue(6)
    >>> product(q)
    48
    >>> q.is_empty()
    True
    """
    product = integer_queue.dequeue()
    while not integer_queue.is_empty():
        product *= integer_queue.dequeue()
    return product



def product_star(integer_queue: Queue[int]) -> int:
    """Return the product of integers in the Queue. Do not destroy
    integer_queue.

    Postcondition: the final state of integer_queue is equal to its
        initial state

    >>> q = Queue()
    >>> q.enqueue(2)
    >>> q.enqueue(4)
    >>> product_star(q)
    8
    >>> q.dequeue()
    2
    >>> q.dequeue()
    4
    >>> q.is_empty()
    True
    """
    first_val = integer_queue.dequeue()
    copy = Queue()
    product = first_val
    copy.enqueue(first_val)
    while not integer_queue.is_empty():
        value = integer_queue.dequeue()
        copy.enqueue(value)
        product *= value

    while not copy.is_empty():
        integer_queue.enqueue(copy.dequeue())

    return product


if __name__ == '__main__':
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    prime_line = Queue()
    for prime in primes:
        prime_line.enqueue(prime)

    assert 6469693230 == product_star(prime_line)
    assert not prime_line.is_empty()
    assert 6469693230 == product(prime_line)
    assert prime_line.is_empty()