import logging
from enum import Enum, auto
from itertools import cycle

from connect4.artist import Connect4Artist
from connect4.board import Connect4Board, Connect4DiskColour
from connect4.player import Connect4Player


class Connect4GameResult(Enum):
    """The connect-4 game result"""

    yellow_wins = auto()
    red_wins = auto()
    draw = auto()


class Connect4InvalidGame(Exception):
    pass


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
    artist : Connect4Artist
        artist used to draw the board
    """

    def __init__(
        self,
        board: Connect4Board,
        yellow_player: Connect4Player,
        red_player: Connect4Player,
        artist: Connect4Artist,
    ) -> None:
        """
        Parameters
        ----------
        board: Connect4Board
            board for the game
        yellow_player : Connect4Player
            player using yellow disks
        red_player : Connect4Player
            player using red disks
        artist : Connect4Artist
            artist used to draw the board
        """
        self.board: Connect4Board = board
        self.yellow_player: Connect4Player = yellow_player
        self.red_player: Connect4Player = red_player
        if not yellow_player.colour == Connect4DiskColour.yellow or not red_player.colour == Connect4DiskColour.red:
            raise Connect4InvalidGame("Wrong color configuration")
        self.artist: Connect4Artist = artist

    def play(self) -> Connect4GameResult:
        """
        Play the connect-4 game.

        The red player moves first.

        Returns
        ----------
        Connect4GameResult
            The result of the game
        """
        self.artist.draw()
        player_cycle = cycle([self.red_player, self.yellow_player])
        while not self.board.is_full():
            curr_player = next(player_cycle)
            chosen_column = curr_player.choose_column()
            disk = self.board.insert_disk(curr_player.colour, chosen_column)
            self.artist.draw()
            if self.board.max_num_connected_disks(disk) >= 4:
                self.artist.draw_gameover(curr_player.colour)
                if curr_player.colour == Connect4DiskColour.red:
                    logging.info("Red wins.")
                    return Connect4GameResult.red_wins
                elif curr_player.colour == Connect4DiskColour.yellow:
                    logging.info("Yellow wins.")
                    return Connect4GameResult.yellow_wins
        logging.info("Draw game.")
        return Connect4GameResult.draw
