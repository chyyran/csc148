"""Recursive sorting: mergesort

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the recursive sorting algorithm mergesort.
"""


def mergesort(lst: list) -> list:
    """Return a sorted list with the same elements as <lst>.

    This is a *non-mutating* version of mergesort; it does not mutate the
    input list.

    >>> lst = [0, 2, 1, 6, 5, 4]
    >>> sort_lst = mergesort(lst)
    >>> sort_lst
    [0, 1, 2, 4, 5, 6]
    """
    if len(lst) < 2:
        return lst[:]
    else:
        # Divide the list into two parts, and sort them recursively.
        mid = len(lst) // 2
        left_sorted = mergesort(lst[:mid])
        right_sorted = mergesort(lst[mid:])

        # Merge the two sorted halves. Need a helper here!
        return _merge(left_sorted, right_sorted)


def _merge(lst1: list, lst2: list) -> list:
    """Return a sorted list with the elements in <lst1> and <lst2>.

    Precondition: <lst1> and <lst2> are sorted.
    """
    # Use <index1> and <index2> to keep track of where you are
    # in each list, and <merged> to store the sorted list to return.
    index1 = 0
    index2 = 0
    merged = []

    # for i1, i2 in zip(lst1, lst2):
    #     if i1 <= i2:
    #         index1 += 1
    #         merged.append(i1)
    #     else:
    #         index2 += 1
    #         merged.append(i2)
    while index1 < len(lst1) and index2 < len(lst2):
        if lst1[index1] <= lst2[index2]:
            merged.append(lst1[index1])
            index1 += 1
        else:
            merged.append(lst2[index2])
            index2 += 1

    merged.extend(lst1[index1:])
    merged.extend(lst2[index2:])

    assert len(merged) == len(lst1) + len(lst2)
    return merged
