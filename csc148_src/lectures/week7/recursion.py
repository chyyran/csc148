from typing import Union, List


def count(obj: Union[int, List]) -> int:
    """
    >>> count(18)
    1
    >>> count([4,1,8])
    3
    >>> count([4])
    1
    >>> count([])
    0
    >>> count([4,[2,3],[4,5,6,7,8], 9])
    9
    """
    if isinstance(obj, int):
        return 1
    return sum([count(i) for i in obj])


def unique(obj: Union[int, List]) -> List[int]:
    """
    >>> unique([13, [2, 13], 4])
    [13, 2, 4]
    >>> unique([13, [13, 13], 13])
    [13]
    >>> unique([13, [13, 13, [13, [13,[13]]]], 13, 4])
    [13, 4]
    """
    if isinstance(obj, int):
        return [obj]
    answers = []
    for i in obj:
        if isinstance(i, int) and i not in answers:
            answers.append(i)
        if isinstance(i, list):
            answers.extend([i for i in unique(i) if i not in answers])
    return answers
