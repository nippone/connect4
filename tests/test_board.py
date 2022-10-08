import pytest

from connect4.board import Connect4Board, Connect4Disk, Connect4DiskColour


def test_board_full():
    board = Connect4Board(rows=6, columns=7)
    assert board.is_full() is False
    for idx in range(board.rows):
        board.insert_disk(Connect4DiskColour.yellow, column_index=0)
    assert board.disks_in_column(column_index=0) == board.rows


@pytest.mark.parametrize(
    "insertion_list, disk, expected_connections",
    [
        ([(Connect4DiskColour.yellow, 0)], Connect4Disk(0, 1, Connect4DiskColour.yellow), 2),
        ([(Connect4DiskColour.yellow, 0)], Connect4Disk(1, 0, Connect4DiskColour.yellow), 1),
        ([(Connect4DiskColour.yellow, 0)], Connect4Disk(0, 2, Connect4DiskColour.yellow), 1),
    ],
)
def test_horizontal_connections(insertion_list, disk, expected_connections):
    board = Connect4Board(rows=6, columns=7)
    for colour, column in insertion_list:
        board.insert_disk(colour, column_index=column)
    hor_connections = board._horizontally_connected_disks(disk)
    assert len(hor_connections) == expected_connections
