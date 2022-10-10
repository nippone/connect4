from abc import ABC, abstractmethod
from random import randrange
from typing import List

import numpy as np

from connect4.board import Connect4Board, Connect4Disk, Connect4DiskColour


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

    def _valid_moves(self) -> List[int]:
        disks_per_column = [self.board.disks_in_column(col_idx) for col_idx in range(self.board.columns)]
        return [column_idx for column_idx, disks in enumerate(disks_per_column) if disks < self.board.rows]

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
        valid_columns = self._valid_moves()
        return valid_columns[randrange(len(valid_columns))]


class Connect4ShortSightedAI(Connect4Player):
    """
    Connect-4 AI player. It looks one move in the future.
    """

    @staticmethod
    def _get_move_score(max_num_connections: int, weight_factor: float = 1.0) -> float:
        """
        Get a score based on the number of connections created by a move.

        Parameters
        ----------
        max_num_connections: int
            max number of disks connected by a move
        Returns
        -------
        float
            Chosen column index
        """
        if max_num_connections >= 4:
            return weight_factor * 1000
        else:
            return weight_factor * max_num_connections

    def choose_column(self) -> int:
        """
        Choose where to insert the next disk.

        This dummy player just extracts a random column.

        Returns
        -------
        int
            Chosen column index
        """
        valid_columns = self._valid_moves()
        opponent_colour = Connect4DiskColour.yellow if self.colour == Connect4DiskColour.red else Connect4DiskColour.red
        connections_my_move = [
            self.board.max_num_connected_disks(Connect4Disk(self.board.disks_in_column(c), c, self.colour))
            for c in valid_columns
        ]
        connections_opponent = [
            self.board.max_num_connected_disks(Connect4Disk(self.board.disks_in_column(c), c, opponent_colour))
            for c in valid_columns
        ]
        my_scores = [self._get_move_score(con) for con in connections_my_move]
        opponents_scores = [self._get_move_score(con, weight_factor=0.7) for con in connections_opponent]

        my_best_move_idx = np.argmax(my_scores)
        opponent_best_move_idx = np.argmax(opponents_scores)

        if my_scores[my_best_move_idx] > opponents_scores[opponent_best_move_idx]:
            return valid_columns[my_best_move_idx]
        else:
            return valid_columns[opponent_best_move_idx]


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
        while True:
            input_str = input(f"{self.colour.name} player. Choose column index (0-{self.board.columns-1}):")
            if input_str.isdigit() and int(input_str) < self.board.columns:
                return int(input_str)
