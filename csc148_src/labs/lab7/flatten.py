from typing import List, Union


def flatten1(lst: Union[int, List]) -> List[int]:
    """
    Flattens a list
    >>> flatten1([[1, 5, 7], [[4]], 0, [-4, [6], [7, [8], 8]]])
    [1, 5, 7, 4, 0, -4, 6, 7, 8, 8]
    """
    if isinstance(lst, int):
        return [lst]
    else:
        result = []
        for lst_i in lst:
            result.extend(flatten1(lst_i))
        return result

def count_odd(obj: Union[int, List]) -> int:
    """
    >>> count_odd([1, [2, 6, 5], [9,[8,7]]])
    4
    """
    return obj % 2 if isinstance(obj, int) else sum([count_odd(i) for i in obj])


if __name__ == '__main__':
    import doctest
    doctest.testmod()