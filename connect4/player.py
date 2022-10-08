from abc import ABC, abstractmethod
from random import randrange

from connect4.board import Connect4Board, Connect4DiskColour


class Connect4Player(ABC):
    """
    Abstract connect-4 player.

    Attributes
    ----------
    board: Connect4Board
        The board of the game
    colour: Connect4DiskColour
        This player's disk colour
    """

    def __init__(self, board: Connect4Board, colour: Connect4DiskColour):
        """
        Parameters
        ----------
        board: Connect4Board
            The board of the game
        colour: Connect4DiskColour
            This player's disk colour
        """
        self.board = board
        self.colour = colour

    @abstractmethod
    def choose_column(self) -> int:
        """
        Choose where to insert the next disk.

        Returns
        ----------
        int
            Chosen column index
        """
        ...


class Connect4DummyPlayer(Connect4Player):
    """
    Dummy connect-4 AI player. It draws random numbers
    """

    def choose_column(self) -> int:
        """
        Choose where to insert the next disk.

        This dummy player just extracts a random column.

        Returns
        ----------
        int
            Chosen column index
        """
        disks_per_column = [self.board.disks_in_column(col_idx) for col_idx in range(self.board.columns)]
        valid_columns = [column_idx for column_idx, disks in enumerate(disks_per_column) if disks < self.board.rows]
        return valid_columns[randrange(len(valid_columns))]


class Connect4HumanPlayer(Connect4Player):
    """
    Human connect-4 player. The input is collected from the standard input.
    """

    def choose_column(self) -> int:
        """
        Choose where to insert the next disk.

        The input is collected from the standard input.

        Returns
        ----------
        int
            Chosen column index
        """
        input_str = input("Choose column:")
        return int(input_str)
