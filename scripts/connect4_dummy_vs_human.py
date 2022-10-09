import logging

from connect4.artist import Connect4ArtistMatplotlib
from connect4.board import Connect4Board, Connect4DiskColour
from connect4.game import Connect4Game
from connect4.player import Connect4DummyPlayer, Connect4HumanPlayer

logging.basicConfig(level=logging.DEBUG)

board = Connect4Board(rows=6, columns=7)
artist = Connect4ArtistMatplotlib(board)
human = Connect4HumanPlayer(board, Connect4DiskColour.red)
dummy = Connect4DummyPlayer(board, Connect4DiskColour.yellow)

game = Connect4Game(board, yellow_player=dummy, red_player=human, artist=artist)
result = game.play()
