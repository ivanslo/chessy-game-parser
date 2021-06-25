import sys
import Movement, GameMetadata
import copy

def fromFile(file:int)-> str:
	if file == 0:
		return 'a'
	if file == 1:
		return 'b'
	if file == 2:
		return 'c'
	if file == 3:
		return 'd'
	if file == 4:
		return 'e'
	if file == 5:
		return 'f'
	if file == 6:
		return 'g'
	if file == 7:
		return 'h'
	raise Exception(('File is not valid: {0}').format(file))

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

def fromRank(rank: int)->str:
	return '{}'.format(rank+1)

def toRank(rank: str)-> int:
	try: 
		r = int(rank)
		return r-1
	except:
		raise Exception(('rank is not valid: {0}').format(rank))

def fromFileRank(file: int, rank: int) -> str:
	return '{}{}'.format(fromFile(file), fromRank(rank))

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

	InitialArrangement = {
		'r1': { 'pos': "a8"}, # 'taken': False, 'face': "r" },
		'n1': { 'pos': "b8"}, # 'taken': False, 'face': "n" },
		'b1': { 'pos': "c8"}, # 'taken': False, 'face': "b" },
		'q1': { 'pos': "d8"}, # 'taken': False, 'face': "q" },
		'k1': { 'pos': "e8"}, # 'taken': False, 'face': "k" },
		'b2': { 'pos': "f8"}, # 'taken': False, 'face': "b" },
		'n2': { 'pos': "g8"}, # 'taken': False, 'face': "n" },
		'r2': { 'pos': "h8"}, # 'taken': False, 'face': "r" },
		'p1': { 'pos': "a7"}, # 'taken': False, 'face': "p" },
		'p2': { 'pos': "b7"}, # 'taken': False, 'face': "p" },
		'p3': { 'pos': "c7"}, # 'taken': False, 'face': "p" },
		'p4': { 'pos': "d7"}, # 'taken': False, 'face': "p" },
		'p5': { 'pos': "e7"}, # 'taken': False, 'face': "p" },
		'p6': { 'pos': "f7"}, # 'taken': False, 'face': "p" },
		'p7': { 'pos': "g7"}, # 'taken': False, 'face': "p" },
		'p8': { 'pos': "h7"}, # 'taken': False, 'face': "p" },
		'R1': { 'pos': "a1"}, # 'taken': False, 'face': "R" },
		'N1': { 'pos': "b1"}, # 'taken': False, 'face': "N" },
		'B1': { 'pos': "c1"}, # 'taken': False, 'face': "B" },
		'Q1': { 'pos': "d1"}, # 'taken': False, 'face': "Q" },
		'K1': { 'pos': "e1"}, # 'taken': False, 'face': "K" },
		'B2': { 'pos': "f1"}, # 'taken': False, 'face': "B" },
		'N2': { 'pos': "g1"}, # 'taken': False, 'face': "N" },
		'R2': { 'pos': "h1"}, # 'taken': False, 'face': "R" },
		'P1': { 'pos': "a2"}, # 'taken': False, 'face': "P" },
		'P2': { 'pos': "b2"}, # 'taken': False, 'face': "P" },
		'P3': { 'pos': "c2"}, # 'taken': False, 'face': "P" },
		'P4': { 'pos': "d2"}, # 'taken': False, 'face': "P" },
		'P5': { 'pos': "e2"}, # 'taken': False, 'face': "P" },
		'P6': { 'pos': "f2"}, # 'taken': False, 'face': "P" },
		'P7': { 'pos': "g2"}, # 'taken': False, 'face': "P" },
		'P8': { 'pos': "h2"}, # 'taken': False, 'face': "P" },
	}

	def __init__(self):
		self.boards = [ self.IdentityBoard ] 
		self.gameInfo = GameMetadata.GameMetadata()
		self.boardsDict = [self.InitialArrangement]

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


	def getLastStep(self) -> dict:
		return {
			'board': self.getLastBoardInFEN() ,
			'boardDict': self.boardsDict[-1]
			}

	def getLastBoard(self) -> [[str]]:
		if len(self.boards) < 1:
			raise Exception('There are no boards')
		return self.boards[-1]


	def setupBoardInFEN(self, boardFEN: str ):
		spacedBoard = ""
		for i in range(len(boardFEN)):
			if boardFEN[i].isdigit():
				spacedBoard += " "*int(boardFEN[i])
			else:
				spacedBoard +=boardFEN[i]
		files = spacedBoard.split('/')

		assert len(files)== 8 , "bad input"
		board = [list(file) for file in files]

		board.reverse() # so white is UP
		self.boards.append(board)

		# setup boardDict
		boardDict = {}

		for i, row in enumerate(boardFEN.split("/")):
			j = 0
			for element in row:
				if element.isdigit():
					j += int(element)
				else:
					k = 1
					while boardDict.get('{}{}'.format(element, k)) != None:
						k += 1
					boardDict['{}{}'.format(element,k)] = { 'pos': fromFileRank(j, 7-i) }
					j += 1
		self.boardsDict.append(boardDict)


	def getPieceIdInPosition(self, rank:int, file:int) -> str:
		boardDict = self.getLastBoardDict()
		position = fromFileRank(file, rank)

		for key in boardDict:
			if boardDict[key]['pos'] == position:
				return key
		return None


	def getLastBoardDict(self) -> dict:
		if len(self.boardsDict) < 1:
			raise Exception('There are not `boardsDict`')
		return self.boardsDict[-1]

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
		#TODO: remove `newBoard` - generate the `board` out of `boardDict`
		newBoard = copy.deepcopy(self.boards[-1])
		newBoardDict = copy.deepcopy(self.boardsDict[-1])

		# TODO: store the movement in a extended format (Reversible Algebraic, or similar)

		if movement.piece == 'p':
			self.movePawn(movement, newBoard, newBoardDict)
		if movement.piece == 'B':
			self.moveBishop(movement, newBoard, newBoardDict)
		if movement.piece == 'N':
			self.moveKnight(movement, newBoard, newBoardDict)
		if movement.piece == 'R':
			self.moveRook(movement, newBoard, newBoardDict)
		if movement.piece == 'Q':
			self.moveQueen(movement, newBoard, newBoardDict)
		if movement.piece == 'K':
			if movement.castleShort or movement.castleLong:
				self.castle(movement, newBoard, newBoardDict)
			else:
				self.moveKing(movement, newBoard, newBoardDict)

		self.boardsDict.append(newBoardDict)
		self.boards.append(newBoard)


	def movePawn(self, movement: Movement, board: [[str]], boardDict: dict):
		file, rank, piece = self.getFileRankPiece(movement)
		pieceId = None

		side = 1
		if movement.color == 'B':
			side = -1

		if movement.take == False:
			if board[rank-(1 * side)][file] == piece:
				pieceId = self.getPieceIdInPosition(rank-(1 * side), file)
				board[rank-(1*side)][file] = ' '
			elif board[rank-(2*side)][file] == piece:
				pieceId = self.getPieceIdInPosition(rank-(2 * side), file)
				board[rank-(2*side)][file] = ' '
			else:
				raise Exception('Movement invalid: {0}'.format(movement))
		if movement.take == True:
			fromFile = toFile(movement.disFile)
			if board[rank-(1*side)][fromFile] == piece:
				pieceId = self.getPieceIdInPosition(rank-(1 * side), fromFile)
				board[rank-(1*side)][fromFile] = ' '
			else:
				raise Exception("no way that's possible: {0}".format(movement))
			if board[rank][file] == ' ': # took the am'pasaund
				pieceId = self.getPieceIdInPosition(rank-(1 * side), file)
				board[rank-(1*side)][file] = ' '

		if movement.crown:
			piece = movement.crownTo
			if movement.color == 'W':
				# NOTE: this is the 'transformation'
				piece = piece.upper()
			if movement.color == 'B':
				piece = piece.lower()

		board[rank][file] = piece 
		boardDict[pieceId]['pos'] = fromFileRank(file, rank)



	def moveBishop(self, movement: Movement, board: [[str]], boardDict: dict):
		bishopMovement = PieceMovement(
			[(1,1), (1,-1), (-1,1), (-1, -1)],
			isRepeated=True
		)
		self.movePiece(board, movement, bishopMovement, boardDict)

	
	def moveRook(self, movement: Movement, board: [[str]], boardDict: dict):
		rookMovement = PieceMovement(
			[(0,1), (0,-1), (-1,0), (1, 0)],
			isRepeated=True
		)
		self.movePiece(board, movement,rookMovement, boardDict)


	def moveKnight(self, movement: Movement, board: [[str]], boardDict: dict):
		knightMovement = PieceMovement(
			[( 1, 2),( 1,-2),(-1, 2),(-1,-2),
			 ( 2, 1),( 2,-1),(-2, 1),(-2,-1)],
			isRepeated=False
		)
		self.movePiece(board, movement,knightMovement, boardDict)


	def moveQueen(self, movement: Movement, board:[[str]], boardDict: dict):
		queenMovement = PieceMovement(
			[ ( 0, 1), ( 0,-1), ( 1, 0), (-1, 0),
			  ( 1, 1), ( 1,-1), (-1,-1), (-1, 1) ],
			isRepeated=True
		)
		self.movePiece(board, movement, queenMovement, boardDict)


	def moveKing(self, movement: Movement, board:[[str]], boardDict: dict):
		kingMovement = PieceMovement(
			[ ( 0, 1), ( 0,-1), ( 1, 0), (-1, 0),
			  ( 1, 1), ( 1,-1), (-1,-1), (-1, 1) ],
			isRepeated=False
		)
		self.movePiece(board, movement, kingMovement, boardDict)


	def movePiece(self, board: [[str]], movement: Movement, pieceMovement: PieceMovement, boardDict: dict):
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

		pieceId = self.getPieceIdInPosition(pieceFrom['rank'], pieceFrom['file'])
		boardDict[pieceId]['pos'] = fromFileRank(file, rank)


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


	def castle(self, movement, board:[[str]], boardDict: dict):
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

			pieceIdRook = self.getPieceIdInPosition(rank, toFile('h'))
			pieceIdKing = self.getPieceIdInPosition(rank, toFile('e'))
			boardDict[pieceIdRook]['pos'] = fromFileRank(toFile('f'), rank)
			boardDict[pieceIdKing]['pos'] = fromFileRank(toFile('g'), rank)

		if movement.castleLong:
			board[rank][toFile('c')] = kingPiece
			board[rank][toFile('d')] = rookPiece
			board[rank][toFile('a')] = ' '
			board[rank][toFile('e')] = ' '

			pieceIdRook = self.getPieceIdInPosition(rank, toFile('a'))
			pieceIdKing = self.getPieceIdInPosition(rank, toFile('e'))
			boardDict[pieceIdRook]['pos'] = fromFileRank(toFile('c'), rank)
			boardDict[pieceIdKing]['pos'] = fromFileRank(toFile('d'), rank)

	def removeIllegalMoves(self, possibleFroms: [], movement: Movement, board: [[str]]) -> []:
		'''
		this function removes possible movements by taking in consideration which ones will generate a check.
		I.e: there might be 2 rooks in conditions to perform a movement, but one would uncover a check. So that should be
		discarded as illegal.
		Examples:
		* Classics GM, Gausdal NOR, 2002.04.17, round 8, Carlsen vs Bluvshtein, movement 42. ... Rg8
		* Montevideo sim, Montevideo, 1911.??.??, Capablanca vs Rivas Costa, movement 9. Ne2

		It also allow movements that will cover the check.
		Example:
		* FIDE World Rapid 2014, Dubai UAE, 2014.06.16, round 2.2, Carlsen vs Guseinov, movement 8 .. Ne7
		'''

		# Strategy: Clone the board. simulate one movement, if check is present then that's illegal.
		kingPiece = 'K'
		if movement.color == 'B':
			kingPiece = kingPiece.lower()

		movFile, movRank, movPiece = self.getFileRankPiece(movement)

		filteredPossibleFroms = []
		# Strategy: Clone the board. One possible movement, one by one:
		# 	- simulate the movement (put the piece there) 
		#   - check there's no check against itself: that's a legal movement
		# this will remove "possibleMoves" that uncover checks.
		for possibleFrom in possibleFroms:
			b = copy.deepcopy(board)
			# simulate movement
			b[movRank][movFile] = movPiece
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
