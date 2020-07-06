import parser as pr
import sys
import Board

import json

class Game:
	def __init__(self):
		self.steps = []

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,
			sort_keys=True, indent=2)

	def addStep(self, fen):
		self.steps.append({'board': fen})

def processGame(gamePGN: str):
	lexer  = pr.ChessLexer()
	parser = pr.ChessParser()
	board = Board.Board()
	game = Game()

	def processMovement(aa):
		board.makeMovement(aa)
		game.addStep(board.getLastBoardInFEN())

	parser.setCallbackFunction( processMovement )

	# add initial board
	game.addStep(board.getLastBoardInFEN())
	# parse the rest of the game
	parser.parse(lexer.tokenize(gamePGN))
	# return in JSON Format
	return game.toJSON()
