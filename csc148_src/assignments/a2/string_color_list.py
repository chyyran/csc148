from typing import Tuple


class Colour:
    def __init__(self, colour: Tuple[int, int, int], name: str):
        self.colour = colour
        self.name = name

    def __getitem__(self, item):
        return self.colour[item]

    def __setitem__(self, key, value):
        return self.colour[key] == value

    def __str__(self):
        return self.colour

    def __eq__(self, other):
        if isinstance(other, Tuple):
            return other == self.colour
        if isinstance(other, Colour):
            return other == self


def make_color(color_list, color_names):
    return [Colour(i[0], i[1]) for i in zip(color_list, color_names)]


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PACIFIC_POINT = (1, 128, 181)
OLD_OLIVE = (138, 151, 71)
REAL_RED = (199, 44, 58)
MELON_MAMBO = (234, 62, 112)
DAFFODIL_DELIGHT = (255, 211, 92)
TEMPTING_TURQUOISE = (75, 196, 213)
COLOUR_LIST_VALUES = [PACIFIC_POINT, REAL_RED, OLD_OLIVE, DAFFODIL_DELIGHT]
COLOUR_NAMES = ['Pacific Point', 'Real Red', 'Old Olive', 'Daffodil Delight']
COLOUR_LIST = make_color(COLOUR_LIST_VALUES, COLOUR_NAMES)
