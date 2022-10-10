import logging

from connect4 import __version__
from connect4.artist import Connect4ArtistMatplotlib
from connect4.board import Connect4Board, Connect4DiskColour
from connect4.game import Connect4Game
from connect4.player import Connect4DummyPlayer, Connect4HumanPlayer

logging.basicConfig(level=logging.INFO)
logging.info(f"Connect4 v: {__version__}")
logging.info("Dummy vs human.")

board = Connect4Board(rows=6, columns=7)
artist = Connect4ArtistMatplotlib(board)
red = Connect4HumanPlayer(board, Connect4DiskColour.red)
yellow = Connect4DummyPlayer(board, Connect4DiskColour.yellow)

game = Connect4Game(board, yellow_player=yellow, red_player=red, artist=artist)
result = game.play()
logging.info(f"The winner is: {result.name}")
