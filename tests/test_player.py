import io

import pytest

from connect4.board import Connect4Board, Connect4DiskColour
from connect4.player import (
    Connect4DummyPlayer,
    Connect4HumanPlayer,
    Connect4ShortSightedAI,
)


def test_dummy_player():
    board = Connect4Board(rows=6, columns=7)
    dummy = Connect4DummyPlayer(board, Connect4DiskColour.red)
    while not board.is_full():
        col = dummy.choose_column()
        assert col < board.columns
        assert board.disks_in_column(col) < board.rows
        board.insert_disk(dummy.colour, col)


def test_AI_player():
    board = Connect4Board(rows=6, columns=7)
    dummy = Connect4ShortSightedAI(board, Connect4DiskColour.red)
    while not board.is_full():
        col = dummy.choose_column()
        assert col < board.columns
        assert board.disks_in_column(col) < board.rows
        board.insert_disk(dummy.colour, col)


@pytest.mark.parametrize(
    "list_inputs",
    [
        ["1", "4", "6", "ee\n5"],
    ],
)
def test_human_player(monkeypatch, list_inputs):
    board = Connect4Board(rows=6, columns=7)
    human = Connect4HumanPlayer(board, Connect4DiskColour.red)
    for my_in in list_inputs:
        if board.is_full():
            return
        monkeypatch.setattr("sys.stdin", io.StringIO(my_in))
        col = human.choose_column()
        assert col < board.columns
        board.insert_disk(human.colour, col)
