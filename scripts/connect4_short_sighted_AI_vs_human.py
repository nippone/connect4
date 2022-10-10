import logging

from connect4 import __version__
from connect4.artist import Connect4ArtistMatplotlib
from connect4.board import Connect4Board, Connect4DiskColour
from connect4.game import Connect4Game
from connect4.player import Connect4HumanPlayer, Connect4ShortSightedAI

logging.basicConfig(level=logging.INFO)

logging.info(f"Connect4 v: {__version__}")
logging.info("Short-sighted AI vs human.")

board = Connect4Board(rows=6, columns=7)
artist = Connect4ArtistMatplotlib(board)
red = Connect4HumanPlayer(board, Connect4DiskColour.red)
yellow = Connect4ShortSightedAI(board, Connect4DiskColour.yellow)

game = Connect4Game(board, yellow_player=yellow, red_player=red, artist=artist)
result = game.play()
logging.info(f"The winner is: {result.name}")
