"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the player class hierarchy.
"""

import random
from typing import Optional, Callable, Tuple

import pygame

from block import Block
from goal import Goal
from renderer import Renderer

TIME_DELAY = 600


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    renderer:
        The object that draws our Blocky board on the screen
        and tracks user interactions with the Blocky board.
    id:
        This player's number.
        Used by the renderer to refer to the player, for example as "Player 2".
    goal:
        This player's assigned goal for the game.
    """
    renderer: Renderer
    id: int
    goal: Goal

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this Player by setting up its public attributes.
        """
        self.goal = goal
        self.renderer = renderer
        self.id = player_id

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """A human player.

    A HumanPlayer can do a limited number of smashes.

    === Public Attributes ===
    num_smashes:
        The number of smashes which this HumanPlayer has performed.

    === Representation Invariants ===
    - num_smashes >= 0
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that the user has most recently selected for action;
    #     changes upon movement of the cursor and use of arrow keys
    #     to select desired level.
    # _level:
    #     The level of the Block that the user selected
    #
    # == Representation Invariants concerning the private attributes ==
    # - _level >= 0

    # The total number of 'smash' moves a HumanPlayer can make during a game.
    MAX_SMASHES = 1

    num_smashes: int
    _selected_block: Optional[Block]
    _level: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)

        # This HumanPlayer has done no smashes yet.
        self.num_smashes = 0

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._selected_block = None

    def process_event(self, board: Block,
                      event: pygame.event.Event) -> Optional[int]:
        """Process the given pygame <event>.

        Identify the selected block and mark it as highlighted.  Then identify
        what it is that <event> indicates needs to happen to <board>
        and do it.

        Return
           - None if <event> was not a board-changing move (that is, if was
             a change in cursor position, or a change in _level made via
            the arrow keys),
           - 1 if <event> was a successful move, and
           - 0 if <event> was an unsuccessful move (for example in the case of
             trying to smash in an invalid location or when the player is not
             allowed further smashes).
        """
        # Get the new "selected" block from the position of the cursor
        block = board.get_selected_block(pygame.mouse.get_pos(), self._level)

        # Remove the highlighting from the old "_selected_block"
        # before highlighting the new one
        if self._selected_block is not None:
            self._selected_block.highlighted = False
        self._selected_block = block
        self._selected_block.highlighted = True

        # Since get_selected_block may have not returned the block at
        # the requested level (due to the level being too low in the tree),
        # set the _level attribute to reflect the level of the block which
        # was actually returned.
        self._level = block.level

        if event.type == pygame.MOUSEBUTTONDOWN:
            block.rotate(event.button)
            return 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if block.parent is not None:
                    self._level -= 1
                return None

            elif event.key == pygame.K_DOWN:
                if len(block.children) != 0:
                    self._level += 1
                return None

            elif event.key == pygame.K_h:
                block.swap(0)
                return 1

            elif event.key == pygame.K_v:
                block.swap(1)
                return 1

            elif event.key == pygame.K_s:
                if self.num_smashes >= self.MAX_SMASHES:
                    print('Can\'t smash again!')
                    return 0
                if block.smash():
                    self.num_smashes += 1
                    return 1
                else:
                    print('Tried to smash at an invalid depth!')
                    return 0

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.

        This method will hold focus until a valid move is performed.
        """
        self._level = 0
        self._selected_block = board

        # Remove all previous events from the queue in case the other players
        # have added events to the queue accidentally.
        pygame.event.clear()

        # Keep checking the moves performed by the player until a valid move
        # has been completed. Draw the board on every loop to draw the
        # selected block properly on screen.
        while True:
            self.renderer.draw(board, self.id)
            # loop through all of the events within the event queue
            # (all pending events from the user input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1

                result = self.process_event(board, event)
                self.renderer.draw(board, self.id)
                if result is not None and result > 0:
                    # un-highlight the selected block
                    self._selected_block.highlighted = False
                    return 0


class RandomPlayer(Player):
    """A random player.

    A RandomPlayer is a computer player that chooses moves randomly.

    Random players have no limit on their smashes.
    But if they randomly choose to smash the top-level block or a unit cell,
    neither of which is permitted, they forfeit their turn.
    """

    def make_move(self, board: Block) -> int:
        """Choose a move randomly to make on the given board,
         and apply it, mutating the Board as appropriate.

        Return 0 to keep the game going.

        When the player tries to smash the top-level block or a unit cell,
        the board will be unaffected and the turn is forfeited.
        """
        random_x = random.randint(0, board.size)
        random_y = random.randint(0, board.size)
        random_loc = (random_x, random_y)
        random_level = random.randint(0, board.max_depth)
        selected_block = board.get_selected_block(random_loc, random_level)

        selected_block.highlighted = True
        self.renderer.draw(board, self.id)
        pygame.time.wait(TIME_DELAY)

        RandomPlayer._apply_random_action(board, selected_block)
        selected_block.highlighted = False
        self.renderer.draw(board, self.id)
        return 0

    @staticmethod
    def _apply_random_action(board: Block, selected_block: Block) -> None:
        """Randomly choose one of the 5 possible types of action, and apply it
        on the chosen block.

        5 possible types of action on the chosen block include:
        (1) swap vertically,
        (2) swap horizontally,
        (3) rotate clockwise,
        (4) rotate counterclockwise,
        (5) smash.
        """
        random_type = random.randint(0, 4)
        if random_type == 0:
            selected_block.swap(1)
        elif random_type == 1:
            selected_block.swap(0)
        elif random_type == 2:
            selected_block.rotate(1)
        elif random_type == 3:
            selected_block.rotate(3)
        else:
            if selected_block.level == 0 or \
                            selected_block.level == board.max_depth:
                # chooses to smash the top-level block or a unit cell
                pass
            else:
                selected_block.smash()


class SmartPlayer(Player):
    """A smart player.

    A SmartPlayer is a computer player that chooses moves more intelligently.

    It generates a set of random moves and, for each,
    checks what its score would be if it were to make that move.
    Then it picks the one that yields the best score.

    Smart players cannot smash.

    A SmartPlayer has a "difficulty" level, which indicates how difficult it is
    to play against it.

    === Public Attributes ===
    difficulty:
        The difficulty level to play against this SmartPlayer.
        Note the integer value indicates how many possible moves this
        SmartPlayer compares when choosing a move to make. For example,
        if difficulty is 0, it compares 5 possible moves.

    === Representation Invariants ===
    difficulty >= 0
    """

    # The number of moves to search per difficulty level.
    # If a difficulty level is given past the maximum index of
    # this list, then the last value in this list is the
    # number of moved made.
    DIFFICULTY_LEVELS = [5, 10, 25, 50, 100, 150]

    difficulty: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal,
                 difficulty: int) -> None:
        """Initialize this SmartPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)

        # This SmartPlayer has a given "difficulty" level.
        self.difficulty = difficulty

    def make_move(self, board: Block) -> int:
        """Choose a move based on score to make on the given board,
         and apply it, mutating the Board as appropriate.

        Return 0 to keep the game going as there are no invalid moves.
        """
        moves = [
            self._evaluate_move(SmartPlayer._get_random_option(),
                                SmartPlayer._get_random_block(board), board)
            for _ in range(self._get_moves_to_compare())
        ]

        chosen_move = max(moves, key=lambda move: move[0])
        selected_block = chosen_move[2]
        selected_block.highlighted = True
        self.renderer.draw(board, self.id)
        pygame.time.wait(TIME_DELAY)
        chosen_move[1](selected_block)
        selected_block.highlighted = False
        self.renderer.draw(board, self.id)
        return 0

    def _evaluate_move(self, move: Tuple[Callable[[Block], None],
                                         Callable[[Block], None]],
                       block: Block, board: Block) -> Tuple[int,
                                                            Callable[[Block],
                                                                     None],
                                                            Block]:
        """Apply the given move, record and return the resultant score, then
        apply the given inverse move.

       Preconditions:
       - move[0] is a function that accepts a block, and applies a valid
         move (swap, rotate), to the board.
       - move[1] is a function that does the inverse of move[0]. In order
         words, after calling move[0](block), calling move[1](block) will
         restore the board to the state before move[0](block) was invoked.
        """
        move[0](block)
        result = self.goal.score(board)
        move[1](block)
        return (result, move[0], block)

    def _get_moves_to_compare(self) -> int:
        """Return the number of moves to compare for the given difficulty level.
        """
        if self.difficulty <= (len(SmartPlayer.DIFFICULTY_LEVELS) - 1):
            return SmartPlayer.DIFFICULTY_LEVELS[self.difficulty]
        return SmartPlayer.DIFFICULTY_LEVELS[(
            len(SmartPlayer.DIFFICULTY_LEVELS) - 1)]

    @staticmethod
    def _get_random_block(board: Block) -> Block:
        """Return a random block from the given board.

        Precondition:
            board.max_depth > 0
        """
        random_x = random.randint(0, board.size)
        random_y = random.randint(0, board.size)
        random_loc = (random_x, random_y)
        random_level = random.randint(0, board.max_depth)
        return board.get_selected_block(random_loc, random_level)

    @staticmethod
    def _get_random_option() -> Tuple[Callable[[Block], None],
                                      Callable[[Block], None]]:
        """Randomly choose one of the 4 possible types of action, returns
        a function that does the action, and another that undoes the action.

        4 possible types of action on the chosen block include:
        (1) swap vertically,
        (2) swap horizontally,
        (3) rotate clockwise,
        (4) rotate counterclockwise.

        Note the second function is guaranteed to be the inverse of the first
        function.
        """
        random_type = random.randint(0, 3)
        if random_type == 0:
            return (lambda block: block.swap(1),
                    lambda block: block.swap(1))
        elif random_type == 1:
            return (lambda block: block.swap(0),
                    lambda block: block.swap(0))
        elif random_type == 2:
            return (lambda block: block.rotate(1),
                    lambda block: block.rotate(3))
        else:
            return (lambda block: block.rotate(3),
                    lambda block: block.rotate(1))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer',
            'pygame'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
