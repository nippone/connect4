from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple

import numpy as np
import numpy.typing as npt


class Connect4DiskColour(Enum):
    """Enumerator for the colours of connect-4 disks"""

    red = 1
    yellow = -1


@dataclass
class Connect4Disk:
    """
    Connect-4 disk in the board

    Attributes
    ----------
    row : int
        row
    column : int
        column
    colour : Connect4DiskColour
        colour
    """

    row: int
    column: int
    colour: Connect4DiskColour


class Connect4InvalidMove(Exception):
    """Raised when the move is invalid"""

    def __init__(self, message: str, position: Connect4Disk):
        self.message = message
        self.position = position


class Connect4Board:
    """
    A connect-4 board

    Attributes
    ----------
    rows : int
        number of rows
    columns : int
        number of columns
    """

    def __init__(self, rows: int, columns: int) -> None:
        """
        Parameters
        ----------
        rows : int
            number of rows
        columns : int
            number of columns
        """
        self.rows: int = rows
        self.columns: int = columns
        self._disks: List[Connect4Disk] = []

    def __len__(self) -> int:
        """
        Number of disks in the board.

        Returns
        ----------
        int
            Number of disks
        """
        return len(self._disks)

    def disks_in_column(self, column_index: int) -> int:
        """
        Disks already present in a given column.

        Parameters
        ----------
        column_index: int
            Column index

        Returns
        ----------
        int
            Number of disks in column
        """
        return len([disk for disk in self._disks if disk.column == column_index])

    def _disks_by_colour(self, colour: Connect4DiskColour) -> List[Connect4Disk]:
        return [d for d in self._disks if d.colour == colour]

    def _horizontally_connected_disks(self, disk: Connect4Disk) -> List[Connect4Disk]:
        disks_same_colour = self._disks_by_colour(disk.colour)
        disks_same_colour.append(disk)
        disks_same_row = sorted([d for d in disks_same_colour if d.row == disk.row], key=lambda x: x.column)
        my_disk_idx = disks_same_row.index(disk)
        return [d for idx, d in enumerate(disks_same_row) if idx - d.column == my_disk_idx - disk.column]

    def _vertically_connected_disks(self, disk: Connect4Disk) -> List[Connect4Disk]:
        pass

    def _diagonally_connected_disks(self, disk: Connect4Disk) -> Tuple[List[Connect4Disk], List[Connect4Disk]]:
        pass

    def max_num_connected_disks(self, disk: Connect4Disk) -> int:
        """
        Given a disk on the board, returns the max number of connected disks, include the current one.

        Parameters
        ----------
        disk: Connect4Disk
            disk to which calculate the connections

        Returns
        ----------
        int
            max number of connected disks, including the current one
        """
        horizontal_connections = self._horizontally_connected_disks(disk)
        vertical_connections = self._vertically_connected_disks(disk)
        diagonal1_connections, diagonal2_connections = self._diagonally_connected_disks(disk)

        # disks_same_column = sorted([d for d in disks_same_colour if d.column == disk.column], key=lambda x: x.row)
        # disk_diag_1 = [d for d in disks_same_colour if (d.row - disk.row) == (d.column - disk.column)]
        # disk_diag_2 = [d for d in disks_same_colour if (d.row - disk.row) == -(d.column - disk.column)]

        return max(
            len(connections)
            for connections in [
                horizontal_connections,
                vertical_connections,
                diagonal1_connections,
                diagonal2_connections,
            ]
        )

    def insert_disk(self, colour: Connect4DiskColour, column_index: int) -> Connect4Disk:
        """
        Insert disk in the board.

        Parameters
        ----------
        colour: Connect4DiskColour
            Colour of the disk
        column_index: int
            Column where to insert the disk

        Returns
        ----------
        Connect4Disk
            Inserted disk
        """
        disks_in_col = self.disks_in_column(column_index)
        new_disk = Connect4Disk(disks_in_col + 1, column_index, colour)
        if disks_in_col >= self.rows:
            raise Connect4InvalidMove("Column is full", new_disk)
        self._disks.append(new_disk)
        return new_disk

    def is_full(self) -> bool:
        """
        True if board is full,

        Returns
        ----------
        bool
            True if full
        """
        return len(self) >= self.rows * self.columns

    def as_matrix(self) -> npt.NDArray[np.int_]:
        """
        Returns the matrix representation of the board.

        Returns
        ----------
        npt.NDArray[int]
            Matrix representing the board
        """
        mat = np.zeros((self.rows, self.columns), dtype=int)
        for disk in self._disks:
            mat[disk.row, disk.column] = disk.colour.value
        return mat
