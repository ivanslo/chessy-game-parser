import sys
import Movement, GameMetadata
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

class PieceMovement:
	def __init__(self, deltas: [(int,int)], isRepeated:bool):
		self.deltas = deltas
		self.isRepeated = isRepeated


class Board:
	'''
	UPPERCASE is White
	lowercase is Black

	top file is White, so I can work as it is in the lower rank compared to black
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
		self.gameInfo = GameMetadata.GameMetadata()

	def addGameInfo(self, info):
		self.gameInfo.add(info)

	def getGameInfo(self):
		return self.gameInfo.getInfo()

	def getGameId(self) -> str:
		return self.gameInfo.getId()

	# board manipulation
	# -----------------------------------------------
	def addBoard(self, board: [[str]]):
		self.boards.append(board)


	def getLastBoard(self) -> [[str]]:
		if len(self.boards) < 1:
			raise Exception('There are no boards')
		return self.boards[-1]


	def addBoardInFEN(self, board: str ):
		spacedBoard = ""
		for i in range(len(board)):
			if board[i].isdigit():
				spacedBoard += " "*int(board[i])
			else:
				spacedBoard +=board[i]
		files = spacedBoard.split('/')

		assert len(files)== 8 , "bad input"
		board = [list(file) for file in files]

		board.reverse() # so white is UP
		self.boards.append(board)


	def getLastBoardInFEN(self ) -> str:
		'''
		FEN Notation: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
		Example of initial position (only the board part)
		rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
		'''
		board = self.getLastBoard()
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


	def getFileRankPiece(self, movement):
		p = movement.piece
		if movement.color == 'W':
			p = p.upper()
		if movement.color == 'B':
			p = p.lower()

		f = toFile(movement.destFile)
		r = toRank(movement.destRank)
		return f, r, p


	# movements in the board
	# -----------------------------------------------
	def makeMovement(self, movement: Movement):
		'''
		the new position is a copy of the previous one, plus a modification
		'''
		newBoard = copy.deepcopy(self.boards[-1])

		if movement.piece == 'p':
			self.movePawn(movement, newBoard)
		if movement.piece == 'B':
			self.moveBishop(movement, newBoard)
		if movement.piece == 'N':
			self.moveKnight(movement, newBoard)
		if movement.piece == 'R':
			self.moveRook(movement, newBoard)
		if movement.piece == 'Q':
			self.moveQueen(movement, newBoard)
		if movement.piece == 'K':
			if movement.castleShort or movement.castleLong:
				self.castle(movement, newBoard)
			else:
				self.moveKing(movement, newBoard)

		self.boards.append(newBoard)


	def movePawn(self, movement: Movement, board: [[str]]):
		file, rank, piece = self.getFileRankPiece(movement)

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
			if board[rank-(1*side)][fromFile] == piece:
				board[rank-(1*side)][fromFile] = ' '
			else:
				raise Exception("no way that's possible: {0}".format(movement))
			if board[rank][file] == ' ': # took the am'pasaund
				board[rank-(1*side)][file] = ' '

		if movement.crown:
			piece = movement.crownTo
			if movement.color == 'W':
				piece = piece.upper()
			if movement.color == 'B':
				piece = piece.lower()

		board[rank][file] = piece


	def moveBishop(self, movement: Movement, board: [[str]]):
		bishopMovement = PieceMovement(
			[(1,1), (1,-1), (-1,1), (-1, -1)],
			isRepeated=True
		)
		self.movePiece(board, movement, bishopMovement)

	
	def moveRook(self, movement: Movement, board: [[str]]):
		rookMovement = PieceMovement(
			[(0,1), (0,-1), (-1,0), (1, 0)],
			isRepeated=True
		)
		self.movePiece(board, movement,rookMovement)


	def moveKnight(self, movement: Movement, board: [[str]]):
		knightMovement = PieceMovement(
			[( 1, 2),( 1,-2),(-1, 2),(-1,-2),
			 ( 2, 1),( 2,-1),(-2, 1),(-2,-1)],
			isRepeated=False
		)
		self.movePiece(board, movement,knightMovement)


	def moveQueen(self, movement: Movement, board:[[str]]):
		queenMovement = PieceMovement(
			[ ( 0, 1), ( 0,-1), ( 1, 0), (-1, 0),
			  ( 1, 1), ( 1,-1), (-1,-1), (-1, 1) ],
			isRepeated=True
		)
		self.movePiece(board, movement, queenMovement)


	def moveKing(self, movement: Movement, board:[[str]]):
		kingMovement = PieceMovement(
			[ ( 0, 1), ( 0,-1), ( 1, 0), (-1, 0),
			  ( 1, 1), ( 1,-1), (-1,-1), (-1, 1) ],
			isRepeated=False
		)
		self.movePiece(board, movement, kingMovement)


	def movePiece(self, board: [[str]], movement: Movement, pieceMovement: PieceMovement):
		file, rank, piece = self.getFileRankPiece(movement)

		possibleFroms = list(map(lambda deltas: self.getPieceInDirection(board, piece, (rank,file), deltas, pieceMovement.isRepeated), pieceMovement.deltas))
		possibleFroms = list(filter( lambda x: x != None, possibleFroms))

		# disambiguation
		if movement.disFile:
			df = toFile(movement.disFile)
			possibleFroms = list(filter(lambda x : x['file'] == df, possibleFroms))
		if movement.disRank:
			dr = toRank(movement.disRank)
			possibleFroms = list(filter(lambda x : x['rank'] == dr, possibleFroms))

		# illegal movements
		if len(possibleFroms) != 1:
			possibleFroms = self.removeIllegalMoves(possibleFroms, movement, board)

		if len(possibleFroms) != 1:
			raise Exception('Not possible to move the Piece [{0}] in game [{1}]'.format(movement, self.gameInfo.getInfo()))

		pieceFrom = possibleFroms[0] 
		board[rank][file] = piece
		board[pieceFrom['rank']][pieceFrom['file']] = ' '


	def getPieceInDirection(self, board: [[str]], piece: str, position:(int,int), direction:(int, int), repeat: bool): 
		''' 
		returns an object with file and rank of the given 'piece' in a certain direction
		returns None if no piece is found is that direction
		'''
		# helper
		def inBoard(r: int, f: int)-> bool:
			if r >= 0 and r < 8 and f >= 0 and f < 8:
				return True
			return False

		rank = position[0]
		file = position[1]
		deltaRank = direction[0]
		deltaFile = direction[1]

		if repeat:
			file += deltaFile
			rank += deltaRank
			while inBoard(rank, file):
				if board[rank][file] == piece:
					return { 'file': file, 'rank': rank }
				elif board[rank][file] != ' ': 
					# stop exploring in a direction if there is an obstructing piece
					return None
				file += deltaFile
				rank += deltaRank
		else:
			file += deltaFile
			rank += deltaRank
			if inBoard(rank, file) and board[rank][file] == piece:
				return { 'file': file, 'rank': rank }

		return None


	def castle(self, movement, board:[[str]]):
		rookPiece = 'R'
		kingPiece = 'K'
		rank = toRank(1)
		if movement.color == 'B':
			rank = toRank(8)
			rookPiece = rookPiece.lower()
			kingPiece = kingPiece.lower()

		if movement.castleShort:
			board[rank][toFile('g')] = kingPiece
			board[rank][toFile('f')] = rookPiece
			board[rank][toFile('h')] = ' '
			board[rank][toFile('e')] = ' '

		if movement.castleLong:
			board[rank][toFile('c')] = kingPiece
			board[rank][toFile('d')] = rookPiece
			board[rank][toFile('a')] = ' '
			board[rank][toFile('e')] = ' '

	def removeIllegalMoves(self, possibleFroms: [], movement: Movement, board: [[str]]) -> []:
		'''
		this function removes possible movements by taking in consideration which ones will generate a check.
		I.e: there might be 2 rooks in conditions to perform a movement, but one would uncover a check. So that should be
		discarded as illegal.
		Examples:
		* Classics GM, Gausdal NOR, 2002.04.17, round 8, Carlsen vs Bluvshtein, movement 42. ... Rg8
		* Montevideo sim, Montevideo, 1911.??.??, Capablanca vs Rivas Costa, movement 9. Ne2
		'''

		# Strategy: Clone the board. simulate one movement, if check is present then that's illegal.
		kingPiece = 'K'
		if movement.color == 'B':
			kingPiece = kingPiece.lower()


		filteredPossibleFroms = []
		# Strategy: Clone the board. One possible piece by one: remove it from its place.
		# If there is no check against itself, that's a legal piece to move.
		for possibleFrom in possibleFroms:
			b = copy.deepcopy(board)
			b[possibleFrom['rank']][possibleFrom['file']] = ' ' # remove piece
			if not self.thereIsCheckAgaist(movement.color, b):
				filteredPossibleFroms.append(possibleFrom)

		return filteredPossibleFroms
	
	def thereIsCheckAgaist(self, kingColor: str, board:[[str]]) -> bool:
		kingPiece = 'K'
		queenPiece = 'q'
		bishopPiece = 'b'
		rookPiece = 'r'
		if kingColor == 'B':
			kingPiece = kingPiece.lower()
			queenPiece = queenPiece.upper()
			bishopPiece = bishopPiece.upper()
			rookPiece = rookPiece.upper()

		# identify king position
		kingPos = (0,0)
		for i in range(8):
			for j in range(8):
				if board[i][j] == kingPiece:
					kingPos = (i,j)


		# definition of pieces to search in which direction
		# note: Knights are not present, since their impact doesn't change when the enemy moves
		dir_pieces = [ 
			{ 	'delta': (-1,-1), 
				'pieces': [bishopPiece, queenPiece] },
			{ 	'delta': (-1,+1), 
				'pieces': [bishopPiece, queenPiece] },
			{ 	'delta': (+1,-1), 
				'pieces': [bishopPiece, queenPiece] },
			{ 	'delta': (+1,+1), 
				'pieces': [bishopPiece, queenPiece] },
			{ 	'delta': (-1, 0), 
				'pieces': [rookPiece, queenPiece] },
			{ 	'delta': (1, 0), 
				'pieces': [rookPiece, queenPiece] },
			{ 	'delta': (0, 1), 
				'pieces': [rookPiece, queenPiece] },
			{ 	'delta': (0, -1), 
				'pieces': [rookPiece, queenPiece] }
			]

		for dir_piece in dir_pieces:
			for p in dir_piece['pieces']:
				if self.getPieceInDirection( board, p, kingPos, dir_piece['delta'], True):
					return True
		return False

	# debug
	# ---------------------------------------------
	def printLastBoard(self):
		self.printGivenBoard(self.boards[-1])

	def printGivenBoard(self, board: [[str]]):
		for file in range(8):
			print("| ---- ", end = '')
		print('| ')
		for rank in range(7,-1, -1):
			for file in range(8):
				print("| %3s  " % (board[rank][file]), end = '')
			print('| ')
			for file in range(8):
				print("| ---- ", end = '')
			print('| ')
