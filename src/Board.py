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
	IdentityBoard: [[str]] = [ 
			['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR'],
			['Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp', 'Wp'],
			[ ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  ' '],
			[ ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  ' '],
			[ ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  ' '],
			[ ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  ' ',  ' '],
			['Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp', 'Bp'],
			['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR']
	]

	def __init__(self):
		self.boards = [ self.IdentityBoard ] 


	def movePawn(self, movement: Movement, board: [[str]]):
		file = toFile(movement.destFile)
		rank = toRank(movement.destRank)
		piece = movement.color + movement.piece

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
		file = toFile(movement.destFile)
		rank = toRank(movement.destRank)
		piece = movement.color + movement.piece

		# where is it moved from?
		whereFrom = self.findPieceWithDelta(board, piece, rank, file, -1, -1)
		if whereFrom:
			board[whereFrom['rank']][whereFrom['file']] = ' '
			board[rank][file] = piece
			return

		whereFrom = self.findPieceWithDelta(board, piece, rank, file, -1, 1)
		if whereFrom:
			board[whereFrom['rank']][whereFrom['file']] = ' '
			board[rank][file] = piece
			return
		whereFrom = self.findPieceWithDelta(board, piece, rank, file, 1, -1)
		if whereFrom:
			board[whereFrom['rank']][whereFrom['file']] = ' '
			board[rank][file] = piece
			return
		whereFrom = self.findPieceWithDelta(board, piece, rank, file, 1, 1)
		if whereFrom:
			board[whereFrom['rank']][whereFrom['file']] = ' '
			board[rank][file] = piece
			return
		raise Exception('not possible to move bishop like that {0}'.format(movement))
	
	def moveRook(self, movement: Movement, board: [[str]]):
		file = toFile(movement.destFile)
		rank = toRank(movement.destRank)
		piece = movement.color + movement.piece

		# where is it moved from?
		possibleRooks = []

		for delta in [(0,1), (0,-1), (-1,0), (1, 0)]:
			whereFrom = self.findPieceWithDelta(board, piece, rank, file, delta[0], delta[1])
			if whereFrom:
				possibleRooks.append(whereFrom)


		# TODO: do the same with the Knights!!!!
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
		# TODO: write a 'getFRP' that return the three
		file = toFile(movement.destFile)
		rank = toRank(movement.destRank)
		piece = movement.color + movement.piece


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
				possibleKnights.append( { 'rank':testRank, 'file':testFile} )

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


	def findPieceWithDelta(self, board: [[str]], piece: str, rank: int, file: int, deltaRank: int, deltaFile: int): 
		
		if board[rank][file] == 'piece':
			return { 'file': file, 'rank': rank }

		while file >= 0 and rank >= 0 and file < 8 and rank < 8:
			if board[rank][file] == piece:
				return { 'file': file, 'rank': rank }
			file += deltaFile
			rank += deltaRank
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


	def getAllBoards(self):
		return self.boards

