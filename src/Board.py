import sys
import Movement
import copy

def toFile(file: str)-> int:
	if file == 'a':
		return 0
	if file == 'b':
		return 1
	if file == 'c':
		return 2
	if file == 'd':
		return 3
	if file == 'e':
		return 4
	if file == 'f':
		return 5
	if file == 'g':
		return 6
	if file == 'h':
		return 7
	raise Exception(('File is not valid: {0}').format(file))

def toRank(rank: str)-> int:
	try: 
		r = int(rank)
		return r-1
	except:
		raise Exception(('rank is not valid: {0}').format(rank))



class Board:
	'''
	uppercase is White
	lowercase is Black
	'''
	IdentityBoard: [[str]] = [ 
			['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
			['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
			['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
			['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
	]

	def __init__(self):
		self.boards = [ self.IdentityBoard ] 

	def getFRP(self, movement):
		piece = movement.piece
		if movement.color == 'W':
			piece = piece.upper()
		if movement.color == 'B':
			piece = piece.lower()

		file = toFile(movement.destFile)
		rank = toRank(movement.destRank)

		return file, rank, piece

	def movePawn(self, movement: Movement, board: [[str]]):
		file, rank, piece = self.getFRP(movement)

		side = 1
		if movement.color == 'B':
			side = -1

		if movement.take == False:
			if board[rank-(1 * side)][file] == piece:
				board[rank-(1*side)][file] = ' '
			elif board[rank-(2*side)][file] == piece:
				board[rank-(2*side)][file] = ' '
			else:
				raise Exception('Movement invalid: {0}'.format(movement))
		if movement.take == True:
			fromFile = toFile(movement.disFile)
			# remove the moving piece
			if board[rank-(1*side)][fromFile] == piece:
				board[rank-(1*side)][fromFile] = ' '
			else:
				raise Exception("no way that's possible")
			# remove the taken piece
			if board[rank][file] == ' ': # took the am'pasaund
				board[rank-(1*side)][file] = ' '

		board[rank][file] = piece

	def moveBishop(self, movement: Movement, board: [[str]]):
		file, rank, piece = self.getFRP(movement)

		# TODO: do as rooks,... actually I might need to disambiguate
		whereFrom = self.findPieceWithDelta(board, piece, rank, file, -1, -1, repeat=True)
		if whereFrom:
			board[whereFrom['rank']][whereFrom['file']] = ' '
			board[rank][file] = piece
			return

		whereFrom = self.findPieceWithDelta(board, piece, rank, file, -1, 1, repeat=True)
		if whereFrom:
			board[whereFrom['rank']][whereFrom['file']] = ' '
			board[rank][file] = piece
			return
		whereFrom = self.findPieceWithDelta(board, piece, rank, file, 1, -1, repeat=True)
		if whereFrom:
			board[whereFrom['rank']][whereFrom['file']] = ' '
			board[rank][file] = piece
			return
		whereFrom = self.findPieceWithDelta(board, piece, rank, file, 1, 1, repeat=True)
		if whereFrom:
			board[whereFrom['rank']][whereFrom['file']] = ' '
			board[rank][file] = piece
			return
		raise Exception('not possible to move bishop like that {0}'.format(movement))
	
	def moveRook(self, movement: Movement, board: [[str]]):
		file, rank, piece = self.getFRP(movement)

		possibleRooks = []

		for delta in [(0,1), (0,-1), (-1,0), (1, 0)]:
			whereFrom = self.findPieceWithDelta(board, piece, rank, file, delta[0], delta[1], repeat=True)
			if whereFrom:
				possibleRooks.append(whereFrom)


		if len(possibleRooks) > 1:
			if movement.disRank:
				dr = toRank(movement.disRank)
				possibleRooks = list(filter(lambda x : x['rank'] == dr, possibleRooks ))
			if movement.disFile:
				df = toFile(movement.disFile)
				possibleRooks = list(filter(lambda x : x['file'] == df, possibleRooks ))
		
		if len(possibleRooks) == 1:
			rook = possibleRooks[0]
			board[rook['rank']][rook['file']] = ' '
		else:
			raise Exception('Not possible to move the Rook {0}'.format(movement))

		board[rank][file] = piece

	def moveKnight(self, movement: Movement, board: [[str]]):
		file, rank, piece = self.getFRP(movement)


		def inBoard(r: int, f: int)-> bool:
			if r >= 0 and r < 8 and f >= 0 and f < 8:
				return True
			return False
		
		varF = [ 2, 2, 1, 1,-2,-2,-1,-1]
		varR = [ 1,-1, 2,-2,-1, 1,-2, 2]
		
		possibleKnights = []
		for i in range(8):
			testRank = rank+varR[i]
			testFile = file+varF[i]
			if inBoard(testRank, testFile) and board[testRank][testFile] == piece:
				possibleKnights.append( { 'rank': testRank, 'file': testFile } )

		if len(possibleKnights) > 1 :
			knight = None
			if movement.disFile:
				df = toFile(movement.disFile)
				possibleKnights = list(filter(lambda x : x['file'] == df, possibleKnights))
			if movement.disRank:
				dr = toRank(movement.disRank)
				possibleKnights = list(filter(lambda x : x['rank'] == dr, possibleKnights))

		if len(possibleKnights) == 1:
			knight = possibleKnights[0]
			board[knight['rank']][knight['file']] = ' '
		else:
			raise Exception('Not possible to move the Knight {0}'.format(movement))
	
		board[rank][file] = piece


	def moveQueen(self, movement: Movement, board:[[str]]):
		file, rank, piece = self.getFRP(movement)

		possibleQueens = []
		deltas = [
			#horizontals
			( 0, 1),
			( 0,-1),
			( 1, 0),
			(-1, 0),
			#diagonals
			( 1, 1),
			( 1,-1),
			(-1,-1),
			(-1, 1)
		]

		for delta in deltas:
			whereFrom = self.findPieceWithDelta(board, piece, rank, file, delta[0], delta[1], repeat=True)
			if whereFrom:
				possibleQueens.append(whereFrom)


		if len(possibleQueens) > 1:
			if movement.disRank:
				dr = toRank(movement.disRank)
				possibleQueens = list(filter(lambda x : x['rank'] == dr, possibleQueens ))
			if movement.disFile:
				df = toFile(movement.disFile)
				possibleQueens = list(filter(lambda x : x['file'] == df, possibleQueens ))
		
		if len(possibleQueens) == 1:
			queen = possibleQueens[0]
			board[queen['rank']][queen['file']] = ' '
		else:
			raise Exception('Not possible to move the Queen {0}'.format(movement))

		board[rank][file] = piece

	def moveKing(self, movement: Movement, board:[[str]]):
		file, rank, piece = self.getFRP(movement)

		possibleKings = []
		deltas = [
			#horizontals
			( 0, 1),
			( 0,-1),
			( 1, 0),
			(-1, 0),
			#diagonals
			( 1, 1),
			( 1,-1),
			(-1,-1),
			(-1, 1)
		]

		for delta in deltas:
			whereFrom = self.findPieceWithDelta(board, piece, rank, file, delta[0], delta[1], repeat=False)
			if whereFrom:
				possibleKings.append(whereFrom)


		if len(possibleKings) == 1:
			king = possibleKings[0]
			board[king ['rank']][king['file']] = ' '
		else:
			raise Exception('Not possible to move the King {0}'.format(movement))

		board[rank][file] = piece

	def findPieceWithDelta(self, board: [[str]], piece: str, rank: int, file: int, deltaRank: int, deltaFile: int, repeat: bool): 
		
		def inBoard(r: int, f: int)-> bool:
			if r >= 0 and r < 8 and f >= 0 and f < 8:
				return True
			return False

		if repeat:
			while inBoard(rank, file):
				if board[rank][file] == piece:
					return { 'file': file, 'rank': rank }
				file += deltaFile
				rank += deltaRank
		else:
			file += deltaFile
			rank += deltaRank
			if inBoard(rank, file) and board[rank][file] == piece:
				return { 'file': file, 'rank': rank }

		return None


	def makeMovement(self, movement: Movement):
		# add something to the board
		newBoard = copy.deepcopy(self.boards[-1])
		if movement.piece == 'p':
			self.movePawn(movement, newBoard)

		if movement.piece == 'B':
			self.moveBishop(movement, newBoard)

		if movement.piece == 'N':
			self.moveKnight(movement, newBoard)
		
		if movement.piece == 'R':
			self.moveRook(movement, newBoard)
			# ...

		if movement.piece == 'Q':
			self.moveQueen(movement, newBoard)

		if movement.piece == 'K':
			self.moveKing(movement, newBoard)

		self.boards.append(newBoard)
		
	
	def printBoard(self):
		for file in range(8):
			print("| ---- ", end = '')
		print('| ')
		for rank in range(7,-1, -1):
			for file in range(8):
				print("| %3s  " % (self.boards[-1][rank][file]), end = '')
			print('| ')
			for file in range(8):
				print("| ---- ", end = '')
			print('| ')


	def addBoard(self, board: [[str]]):
		self.boards.append(board)

	def toFENposition(self ) -> str:
		'''
		FEN Notation: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
		Example of initial position (only the board part)
		rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
		'''

		def toFenPiece(boardPiece: str) -> str:
			if boardPiece[0] == 'W':
				return boardPiece[1].upper()
			if boardPiece[0] == 'B':
				return boardPiece[1].lower()
			if boardPiece == ' ':
				return ' '
			raise Exception('was this a piece? {0}'.format(boardPiece))

		if len(self.boards) < 1:
			raise Exception('There are no boards')

		board = self.boards[-1]
		lines = []
		for rank in range(7,-1, -1):
			line = ""
			for file in range(8):
				line += board[rank][file]
			lines.append(line)

		boardWithSpaces = "/".join(lines)
		boardWithoutSpaces = ""

		spacesAcc = 0
		for i in range(len(boardWithSpaces)):
			if boardWithSpaces[i] != ' ':
				if spacesAcc > 0:
					boardWithoutSpaces += str(spacesAcc)
					spacesAcc = 0
				boardWithoutSpaces += boardWithSpaces[i]
			if boardWithSpaces[i] == ' ':
				spacesAcc += 1

		if spacesAcc > 0:
			boardWithoutSpaces += str(spacesAcc)
		return boardWithoutSpaces





