"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple, TypeVar
from block import Block

T = TypeVar('T')


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A player goal in the game of Blocky that aims to create the largest
    connected "blob" of a given colour c, where a blob is a group of connected
    blocks with the same colour.

    Two blocks are connected if their sides touch.

    Touching corners doesn’t count.
    """

    def score(self, board: Block) -> int:
        """Return the number of unit cells in the largest blob of colour c.
        """
        lst = board.flatten()
        visited = [[-1 for _ in col] for col in lst]
        scores = []
        for col in range(2 ** (board.max_depth - board.level)):
            for row in range(2 ** (board.max_depth - board.level)):
                scores.append(self._undiscovered_blob_size((col, row), lst,
                                                           visited))
        score = max(scores)
        return score

    def description(self) -> str:
        """Return the description of this player goal.
        """
        return 'Create the largest connected blob of this goal\'s target' + \
               ' colour, anywhere within the Block'

    @staticmethod
    def _get_nested(pos: Tuple[int, int], array: List[List[T]]) -> T:
        """Return the item in the nested array at the given index <pos>.

        Preconditions:
         - pos[0] and pos[1] > 0
         - array[pos[0]][pos[1]] exists and is not out of range.
        """
        return array[pos[0]][pos[1]]

    @staticmethod
    def _set_nested(pos: Tuple[int, int],
                    array: List[List[T]], value: [T]) -> None:
        """Set the item in the nested array at the given index <pos>.

        Preconditions:
         - pos[0] and pos[1] > 0
         - array[pos[0]][pos[1]] exists and is not out of range.
        """
        array[pos[0]][pos[1]] = value

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
        (1) -1, if this cell has never been visited.
        (2) 0, if this cell has been visited and discovered not to be of
        the target colour.
        (3) 1, if this cell has been visited and discovered to be of
        the target colour.

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        if pos[0] < 0 or pos[0] > len(board[0]) - 1:
            return 0
        elif pos[1] < 0 or pos[1] > len(board) - 1:
            return 0

        is_visited = self._get_nested(pos, visited)
        if is_visited != -1:
            return 0
        value = self._get_nested(pos, board)
        if value == self.colour:
            self._set_nested(pos, visited, 1)
            return 1 + sum([
                self._undiscovered_blob_size((pos[0], pos[1] + 1), board,
                                             visited),
                self._undiscovered_blob_size((pos[0] + 1, pos[1]), board,
                                             visited),
                self._undiscovered_blob_size((pos[0], pos[1] - 1), board,
                                             visited),
                self._undiscovered_blob_size((pos[0] - 1, pos[1]), board,
                                             visited)
            ])
        else:
            self._set_nested(pos, visited, 0)
            return 0


class PerimeterGoal(Goal):
    """A player goal in the game of Blocky that aims to put the most possible
    units of a given colour c on the outer perimeter of the board.
    """

    def score(self, board: Block) -> int:
        """Return the total number of unit cells of colour c that are on the
        perimeter.

        Corner cells count twice towards the score.
        """
        score = 0
        lst = board.flatten()
        for col in range(2 ** (board.max_depth - board.level)):
            if lst[col][0] == self.colour:
                score += 1
            if lst[col][2 ** (board.max_depth - board.level) - 1] \
                    == self.colour:
                score += 1
        for row in range(2 ** (board.max_depth - board.level)):
            if lst[0][row] == self.colour:
                score += 1
            if lst[2 ** (board.max_depth - board.level) - 1][row] \
                    == self.colour:
                score += 1
        return score

    def description(self) -> str:
        """Return the description of this player goal.
        """
        return 'Put the most possible units of this goal\'s target' + \
               ' colour on the outer perimeter of the board'


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
