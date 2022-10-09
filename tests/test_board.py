import pytest

from connect4.board import (
    Connect4Board,
    Connect4Disk,
    Connect4DiskColour,
    consecutive_elements,
)


@pytest.mark.parametrize(
    "int_set, int_elem, expected_consecutive",
    [
        ({1, 3, 5}, 3, 1),
        ({1}, 1, 1),
        ({1, 4, 5}, 5, 2),
        ({1, 2, 4, 5}, 1, 2),
        ({1, 2, 2, 4, 5}, 1, 2),
    ],
)
def test_consecutive_elements(int_set, int_elem, expected_consecutive):
    num_consec = len(consecutive_elements(int_set, int_elem, lambda x: x))
    assert num_consec == expected_consecutive


y = Connect4DiskColour.yellow
r = Connect4DiskColour.red


def test_board_full():
    board = Connect4Board(rows=6, columns=7)
    assert board.is_full() is False
    for idx in range(board.rows):
        board.insert_disk(Connect4DiskColour.yellow, column_index=0)
    assert board.disks_in_column(column_index=0) == board.rows


@pytest.mark.parametrize(
    "insertion_list, disk, expected_connections",
    [
        ([(y, 0)], Connect4Disk(0, 1, y), 2),
        ([(y, 0)], Connect4Disk(1, 0, y), 1),
        ([(y, 0)], Connect4Disk(0, 2, y), 1),
        ([(y, 0), (y, 2)], Connect4Disk(0, 1, y), 3),
        ([(y, 0), (y, 2), (y, 6)], Connect4Disk(0, 1, y), 3),
        ([(y, 0), (y, 2), (y, 6), (r, 2)], Connect4Disk(0, 1, y), 3),
        ([(y, 0), (y, 2), (y, 6), (y, 2), (y, 0)], Connect4Disk(1, 1, y), 3),
    ],
)
def test_horizontal_connections(insertion_list, disk, expected_connections):
    board = Connect4Board(rows=6, columns=7)
    for colour, column in insertion_list:
        board.insert_disk(colour, column_index=column)
    hor_connections = board._horizontally_connected_disks(disk)
    assert len(hor_connections) == expected_connections


@pytest.mark.parametrize(
    "insertion_list, disk, expected_connections",
    [
        ([(y, 0)], Connect4Disk(0, 1, y), 1),
        ([(y, 0)], Connect4Disk(1, 0, y), 2),
        ([(y, 0)], Connect4Disk(2, 0, y), 1),
        ([(y, 0), (y, 2)], Connect4Disk(0, 1, y), 1),
        ([(y, 0), (y, 0), (y, 6)], Connect4Disk(2, 0, y), 3),
        ([(y, 0), (y, 0), (r, 0), (y, 2)], Connect4Disk(0, 2, y), 1),
    ],
)
def test_vertical_connections(insertion_list, disk, expected_connections):
    board = Connect4Board(rows=6, columns=7)
    for colour, column in insertion_list:
        board.insert_disk(colour, column_index=column)
    ver_connections = board._vertically_connected_disks(disk)
    assert len(ver_connections) == expected_connections


@pytest.mark.parametrize(
    "insertion_list, disk, expected_connections",
    [
        ([(y, 0)], Connect4Disk(0, 1, y), (1, 1)),
        ([(y, 0), (y, 1)], Connect4Disk(0, 2, y), (1, 1)),
        ([(y, 0), (y, 1)], Connect4Disk(1, 1, y), (2, 1)),
        ([(y, 0), (r, 1), (y, 1)], Connect4Disk(2, 2, y), (3, 1)),
        ([(y, 0), (r, 1), (r, 1)], Connect4Disk(2, 2, y), (1, 1)),
        ([(y, 0), (y, 1), (y, 1)], Connect4Disk(0, 0, y), (2, 1)),
        ([(y, 0), (y, 1), (y, 1)], Connect4Disk(0, 2, y), (1, 2)),
        ([(r, 1), (y, 1), (r, 2), (r, 2), (y, 2), (r, 3), (r, 3), (r, 3), (y, 3)], Connect4Disk(4, 4, y), (4, 1)),
        ([(r, 1), (y, 1), (r, 2), (r, 2), (y, 2), (r, 3), (r, 3), (r, 3), (y, 3)], Connect4Disk(2, 2, y), (3, 1)),
        (
            [
                (r, 1),
                (y, 1),
                (r, 2),
                (r, 2),
                (y, 2),
                (r, 3),
                (r, 3),
                (r, 3),
                (y, 3),
                (r, 4),
                (r, 4),
                (y, 4),
                (r, 5),
                (y, 5),
            ],
            Connect4Disk(3, 3, y),
            (3, 3),
        ),
    ],
)
def test_diagonal_connections(insertion_list, disk, expected_connections):
    board = Connect4Board(rows=6, columns=7)
    for colour, column in insertion_list:
        board.insert_disk(colour, column_index=column)
    diag1_connections, diag2_connections = board._diagonally_connected_disks(disk)
    assert len(diag1_connections) == expected_connections[0] and len(diag2_connections) == expected_connections[1]
