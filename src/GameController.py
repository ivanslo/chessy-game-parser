import parser as pr
import sys
import Board

import json

class Game:
	def __init__(self):
		self.steps = []
		self.info = []

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,
			sort_keys=True, indent=2)

	def addStep(self, fen):
		self.steps.append({'board': fen})

	def addInfo(self,info):
		self.info.append(info)

def processGame(gamePGN: str):
	lexer  = pr.ChessLexer()
	parser = pr.ChessParser()
	board = None
	game = None

	def newGame():
		nonlocal board, game
		board = Board.Board()
		game = Game()
		# add initial board
		game.addStep(board.getLastBoardInFEN())

	def processMovement(aa):
		board.makeMovement(aa)
		game.addStep(board.getLastBoardInFEN())

	def processGameInformation(meta):
		game.addInfo(meta)

	def processGameFinished(asd):
		print(game.toJSON())
		newGame()

	parser.setGameInfoDetectedCallback( processGameInformation )
	parser.setGameFinishedCallback( processGameFinished )
	parser.setMovementDetectedCallback( processMovement )
	newGame()

	# parse the rest of the game
	parser.parse(lexer.tokenize(gamePGN))
	# return in JSON Format
	return None
