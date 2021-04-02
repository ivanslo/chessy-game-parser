import parser as pr
import sys
import Board

import json
import copy

class Game:
	def __init__(self):
		self.steps = []
		self.info = {}
		self.id = ""

	def toJSON(self):
		return json.dumps(self, default=lambda o: o.__dict__,
			sort_keys=True, indent=2)

	def addStep(self, fen):
		self.steps.append({'board': fen})


def processPGNText(pgnText: str):
	lexer  = pr.ChessLexer()
	parser = pr.ChessParser()
	board = None
	game = None
	gameNumber = 0

	outputGames = []

	def newGame():
		nonlocal board, game, gameNumber
		board = Board.Board()
		game = Game()
		gameNumber += 1
		# add initial board
		game.addStep(board.getLastBoardInFEN())

	def processMovement(aa):
		nonlocal board, game
		board.makeMovement(aa)
		game.addStep(board.getLastBoardInFEN())

	def processGameInformation(meta):
		nonlocal board
		board.addGameInfo(meta)

	def processGameFinished(asd):
		nonlocal game, outputGames
		game.info = board.getGameInfo()
		game.id = board.getGameId()
		outputGames.append(copy.deepcopy(game))

		newGame()

	# Setup
	parser.setGameInfoDetectedCallback( processGameInformation )
	parser.setGameFinishedCallback( processGameFinished )
	parser.setMovementDetectedCallback( processMovement )
	newGame()

	# parse the input file
	parser.parse(lexer.tokenize(pgnText))
	return outputGames


def processPGNFilePartial(pgnFileName: str, lower: int, upper: int):
	with open(pgnFileName, 'r') as inputGame:
		body = "".join(inputGame.readlines())
		body = body.replace('\r\n', '\n')
		bodyLines = body.split('\n')
		partialBody = '\n'.join(bodyLines[lower:upper])
		processedGames = processPGNText(partialBody)
		for i, pg in enumerate(processedGames):
			outputFileName = "%s_partial_%d.json" % (pgnFileName[:-4], i)
			with open(outputFileName, 'w') as outputFile:
				outputFile.writelines(pg.toJSON())


def processPGNFile(pgnFileName: str):
	with open(pgnFileName, 'r') as inputGame:
		pgnText = "".join(inputGame.readlines())
		processedGames = processPGNText(pgnText.replace('\r\n', '\n'))
		for i, pg in enumerate(processedGames):
			outputFileName = "%s_%d.json" % (pgnFileName[:-4], i)
			with open(outputFileName, 'w') as outputFile:
				outputFile.writelines(pg.toJSON())
