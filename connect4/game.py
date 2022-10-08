from enum import Enum, auto
from itertools import cycle

from connect4.board import Connect4Board, Connect4DiskColour
from connect4.player import Connect4Player


class Connect4GameResult(Enum):
    """The connect-4 game result"""

    yellow_wins = auto()
    red_wins = auto()
    draw = auto()


class Connect4Game:
    """
    A connect-4 game

    Attributes
    ----------
    board: Connect4Board
        the board used for the game
    yellow_player : Connect4Player
        player using yellow disks
    red_player : Connect4Player
        player using red disks
    """

    def __init__(self, board: Connect4Board, yellow_player: Connect4Player, red_player: Connect4Player) -> None:
        """
        Parameters
        ----------
        board: Connect4Board
            board for the game
        yellow_player : Connect4Player
            player using yellow disks
        red_player : Connect4Player
            player using red disks
        """
        self.board: Connect4Board = board
        self.yellow_player: Connect4Player = yellow_player
        self.red_player: Connect4Player = red_player

    def play(self) -> Connect4GameResult:
        """
        Play the connect-4 game.

        The red player moves first.

        Returns
        ----------
        Connect4GameResult
            The result of the game
        """
        player_cycle = cycle([self.red_player, self.yellow_player])
        while self.board.is_full():
            curr_player = next(player_cycle)
            chosen_column = curr_player.choose_column()
            disk = self.board.insert_disk(curr_player.colour, chosen_column)
            if self.board.max_num_connected_disks(disk) >= 4:
                if curr_player.colour == Connect4DiskColour.red:
                    return Connect4GameResult.red_wins
                else:
                    return Connect4GameResult.yellow_wins
        return Connect4GameResult.draw
