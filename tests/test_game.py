import io
import time

import pytest

from connect4.artist import Connect4ArtistMatplotlib
from connect4.board import Connect4Board, Connect4DiskColour
from connect4.game import Connect4Game, Connect4GameResult
from connect4.player import Connect4DummyPlayer, Connect4HumanPlayer


@pytest.mark.parametrize(
    "red_moves, yellow_moves, expected_result",
    [
        (["1", "4", "6", "5"], ["2", "2", "2", "2"], Connect4GameResult.yellow_wins),
        (["1", "2", "3", "3", "4", "4"], ["2", "2", "3", "4", "4", "4"], Connect4GameResult.red_wins),
    ],
)
def test_game_automatic(monkeypatch, red_moves, yellow_moves, expected_result):
    board = Connect4Board(rows=6, columns=7)
    artist = Connect4ArtistMatplotlib(board)
    human1 = Connect4HumanPlayer(board, Connect4DiskColour.red)
    human2 = Connect4HumanPlayer(board, Connect4DiskColour.yellow)

    game = Connect4Game(board, yellow_player=human2, red_player=human1, artist=artist)
    moves_list = [f"{r}\n{y}" for r, y in zip(red_moves, yellow_moves)]
    moves_list.append("a")  # any key to terminate
    input_str = "\n".join(moves_list)
    monkeypatch.setattr("sys.stdin", io.StringIO(input_str))
    result = game.play()
    assert result == expected_result


def test_game_visual_inspection(monkeypatch, games_to_play=5):
    for game_idx in range(games_to_play):
        board = Connect4Board(rows=6, columns=7)
        artist = Connect4ArtistMatplotlib(board)
        dummy1 = Connect4DummyPlayer(board, Connect4DiskColour.red)
        dummy2 = Connect4DummyPlayer(board, Connect4DiskColour.yellow)

        game = Connect4Game(board, yellow_player=dummy2, red_player=dummy1, artist=artist)
        monkeypatch.setattr("sys.stdin", io.StringIO("a"))
        game.play()
        time.sleep(5)
