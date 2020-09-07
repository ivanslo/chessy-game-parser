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


def processPGNFile(pgnFileName: str):
	lexer  = pr.ChessLexer()
	parser = pr.ChessParser()
	board = None
	game = None
	gameNumber = 0

	def newGame():
		nonlocal board, game, gameNumber
		board = Board.Board()
		game = Game()
		gameNumber += 1
		# add initial board
		game.addStep(board.getLastBoardInFEN())

	def processMovement(aa):
		board.makeMovement(aa)
		game.addStep(board.getLastBoardInFEN())

	def processGameInformation(meta):
		game.addInfo(meta)

	def processGameFinished(asd):
		outputFileName = "%s_%d.json" % (pgnFileName[:-4], gameNumber)
		with open(outputFileName, 'w') as outputFile:
			outputFile.writelines(game.toJSON())
		newGame()

	# Setup
	parser.setGameInfoDetectedCallback( processGameInformation )
	parser.setGameFinishedCallback( processGameFinished )
	parser.setMovementDetectedCallback( processMovement )
	newGame()

	# parse the input file
	with open(pgnFileName, 'r') as inputGame:
		pgnFile = "".join(inputGame.readlines())
		parser.parse(lexer.tokenize(pgnFile))

