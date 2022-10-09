import io
import time

from connect4.artist import Connect4ArtistMatplotlib
from connect4.board import Connect4Board, Connect4DiskColour
from connect4.game import Connect4Game
from connect4.player import Connect4DummyPlayer


def test_game(monkeypatch, games_to_play=5):
    for game_idx in range(games_to_play):
        board = Connect4Board(rows=6, columns=7)
        artist = Connect4ArtistMatplotlib(board)
        dummy1 = Connect4DummyPlayer(board, Connect4DiskColour.red)
        dummy2 = Connect4DummyPlayer(board, Connect4DiskColour.yellow)

        game = Connect4Game(board, yellow_player=dummy2, red_player=dummy1, artist=artist)
        monkeypatch.setattr("sys.stdin", io.StringIO("a"))
        game.play()
        time.sleep(5)
