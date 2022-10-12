import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, List, Set, Tuple

import numpy as np
import numpy.typing as npt


class Connect4DiskColour(Enum):
    """Enumerator for the colours of connect-4 disks"""

    red = 1
    yellow = -1
    invalid = 0


@dataclass(frozen=True)
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


def disk_distance(disk1: Connect4Disk, disk2: Connect4Disk) -> float:
    """
    Distance between two disks.

    Parameters
    ----------
    disk1: Connect4Disk
        first disk
    disk2: Connect4Disk
        second disk

    Returns
    ----------
    flot
        distance between the two disks
    """
    return np.sqrt((disk1.row - disk2.row) ** 2 + (disk1.column - disk2.column) ** 2)


def consecutive_elements(s: Set[Any], elem: Any, order_fun: Callable[[Any], int]) -> List[Any]:
    """
    Get the consecutive elements in a set according to a given ordering function.

    Parameters
    ----------
    s: Set[Any]
        a set
    elem: Any
        the element from which to calculate the consecutive elements
    order_fun: Callable[[Any], int]
        int-valued ordering function to be called on each element to determine their order.

    Returns
    ----------
    List[Any]
        list of elements consecutive to the given element according to an ordering function
    """
    if elem not in s:
        raise ValueError("elem must be present in the set.")

    sorted_lst = sorted(s, key=order_fun)
    elem_idx = sorted_lst.index(elem)
    return [e for idx, e in enumerate(sorted_lst) if idx - order_fun(e) == elem_idx - order_fun(elem)]


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

    def available_columns(self) -> List[int]:
        """
        Get the list of the available columns, i.e. where there is space for more disks.

        Returns
        -------
        List[int]
            list of the available column indices
        """
        disks_per_column = [self.disks_in_column(col_idx) for col_idx in range(self.columns)]
        return [column_idx for column_idx, disks in enumerate(disks_per_column) if disks < self.rows]

    def _disks_by_colour(self, colour: Connect4DiskColour) -> List[Connect4Disk]:
        """
        Filter inserted disks by colour.

        Parameters
        ----------
        colour: Connect4DiskColour
            colour

        Returns
        ----------
        List[Connect4Disk]
            list of inserted disks matching the colour
        """
        return [d for d in self._disks if d.colour == colour]

    def _horizontally_connected_disks(self, disk: Connect4Disk) -> List[Connect4Disk]:
        """
        Find disks horizontally connected to a given one.

        Parameters
        ----------
        disk: Connect4Disk
            the disk

        Returns
        ----------
        List[Connect4Disk]
            list of horizontally connected disks
        """
        disks_same_row = {d for d in self._disks_by_colour(disk.colour) if d.row == disk.row}
        disks_same_row.add(disk)
        return consecutive_elements(disks_same_row, disk, lambda x: x.column)

    def _vertically_connected_disks(self, disk: Connect4Disk) -> List[Connect4Disk]:
        """
        Find disks vertically connected to a given one.

        Parameters
        ----------
        disk: Connect4Disk
            the disk

        Returns
        ----------
        List[Connect4Disk]
            list of vertically connected disks
        """
        disks_same_column = {d for d in self._disks_by_colour(disk.colour) if d.column == disk.column}
        disks_same_column.add(disk)
        return consecutive_elements(disks_same_column, disk, lambda x: x.row)

    def _diagonally_connected_disks(self, disk: Connect4Disk) -> Tuple[List[Connect4Disk], List[Connect4Disk]]:
        """
        Find disks diagonally connected to a given one.

        Parameters
        ----------
        disk: Connect4Disk
            the disk

        Returns
        ----------
        Tuple[List[Connect4Disk], List[Connect4Disk]]
            connected disks on the two diagonal directions
        """
        # Ordering function used to order disks on the diagonal
        def diagonal_order_fun(d1: Connect4Disk, d2: Connect4Disk) -> int:
            return int(round(disk_distance(d1, d2) / np.sqrt(2)))

        # First diagonal
        disks_diag1 = {d for d in self._disks_by_colour(disk.colour) if (d.row - disk.row) == (d.column - disk.column)}
        disks_diag1.add(disk)
        bottom_diag1_disk = Connect4Disk(0, disk.column - disk.row, Connect4DiskColour.invalid)
        diag1_connections = consecutive_elements(disks_diag1, disk, lambda x: diagonal_order_fun(x, bottom_diag1_disk))

        # Second diagonal
        disks_diag2 = {d for d in self._disks_by_colour(disk.colour) if (d.row - disk.row) == -(d.column - disk.column)}
        disks_diag2.add(disk)
        bottom_diag2_disk = Connect4Disk(0, disk.column + disk.row, Connect4DiskColour.invalid)
        diag2_connections = consecutive_elements(disks_diag2, disk, lambda x: diagonal_order_fun(x, bottom_diag2_disk))
        return diag1_connections, diag2_connections

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
        logging.debug(
            f"Connections for: {disk}, vertical: {len(vertical_connections)}, "
            f"horizontal: {len(horizontal_connections)},"
            f"diagonal: {len(diagonal1_connections)}, {len(diagonal2_connections)}",
        )

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
        new_disk = Connect4Disk(disks_in_col, column_index, colour)
        if disks_in_col >= self.rows:
            raise Connect4InvalidMove("Column is full", new_disk)
        if column_index >= self.columns:
            raise Connect4InvalidMove("Invalid column", new_disk)
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
        mat = np.full((self.rows, self.columns), Connect4DiskColour.invalid.value)
        for disk in self._disks:
            mat[disk.row, disk.column] = disk.colour.value
        return mat
