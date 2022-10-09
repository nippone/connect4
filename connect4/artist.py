import logging
from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

from connect4.board import Connect4Board, Connect4DiskColour


class Connect4Artist(ABC):
    """
    Artists drawing the graphics of connect-4

    Attributes
    ----------
    board: Connect4Board
        the board used for the game
    """

    @abstractmethod
    def __init__(self, board: Connect4Board) -> None:
        """
        Parameters
        ----------
        board: Connect4Board
            board for the game
        """
        ...

    @abstractmethod
    def draw(self) -> None:
        """Draw graphical representation of the board."""
        ...

    @abstractmethod
    def draw_gameover(self, winner: Connect4DiskColour) -> None:
        """
        Draw game-over screen.

        Parameters
        ----------
        winner: Connect4DiskColour
            winning colour
        """
        ...


class Connect4ArtistTrivial(Connect4Artist):
    """
    Trivial artist drawing the graphics of connect-4. It does not do anything.

    Attributes
    ----------
    board: Connect4Board
        the board used for the game
    """

    def __init__(self, board: Connect4Board) -> None:
        """
        Parameters
        ----------
        board: Connect4Board
            board for the game
        """
        ...

    def draw(self) -> None:
        """Draw graphical representation of the board."""
        ...

    def draw_gameover(self, winner: Connect4DiskColour) -> None:
        """
        Draw game-over screen.

        Parameters
        ----------
        winner: Connect4DiskColour
            winning colour
        """
        ...


class Connect4ArtistMatplotlib(Connect4Artist):
    """
    Artists drawing the graphics of connect-4 using Matplotlib

    Attributes
    ----------
    board: Connect4Board
        the board used for the game
    """

    def __init__(self, board: Connect4Board) -> None:
        """
        Parameters
        ----------
        board: Connect4Board
            board for the game
        """
        self.board = board
        plt.set_loglevel("critical")
        logging.getLogger("PIL").setLevel(logging.WARNING)
        self._fig, self._axis = plt.subplots(1, 1)
        self._axis.set_xticks(range(0, self.board.columns))
        self._axis.set_yticks(range(0, self.board.rows))
        self._axis.set_xticks(np.arange(-0.5, self.board.columns), minor=True)
        self._axis.set_yticks(np.arange(-0.5, self.board.rows), minor=True)
        self._axis.set_xticklabels(range(0, self.board.columns))
        self._axis.set_yticklabels(range(0, self.board.rows))
        self._axis.grid(which="minor", color="k", linewidth=2)
        self.cmap = colors.ListedColormap(["y", "w", "r"])
        plt.show(block=False)

    def _refresh(self) -> None:
        self._fig.canvas.draw()
        self._fig.canvas.flush_events()

    def draw(self) -> None:
        """Draw graphical representation of the board."""
        self._axis.imshow(
            self.board.as_matrix(),
            origin="lower",
            cmap=self.cmap,
            vmin=Connect4DiskColour.yellow.value,
            vmax=Connect4DiskColour.red.value,
        )
        self._refresh()

    def draw_gameover(self, winner: Connect4DiskColour) -> None:
        """
        Draw game-over screen.

        Parameters
        ----------
        winner: Connect4DiskColour
            winning colour
        """
        self._fig.suptitle(f"{winner.name.upper()} WINS")
        self._refresh()
        input("Game over. Press any key to return.")
