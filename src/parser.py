from sly import Lexer, Parser
import sys

import Movement


# -----------------------------------
# Lexer
# -----------------------------------
class ChessLexer(Lexer):
	tokens = { MOVE_NUMBER, GAME_INFO, SPACE, PIECE, 
			RANK, FILE, CASTLE_SHORT, CASTLE_LONG, 
			CHECK, TAKE, RESULT, PROMOTION, NEWLINE }

	
	RESULT = r'[012/]+-[012/]+'
	GAME_INFO = r'\[.+\]\n'
	MOVE_NUMBER = r'\d+\.'
	PIECE = r'[QKNRB]'
	FILE = r'[abcdefgh]'
	RANK= r'[12345678]'
	CASTLE_LONG = r'O-O-O'
	CASTLE_SHORT = r'O-O'
	CHECK = r'\+'
	TAKE = r'x'
	PROMOTION = r'='
	SPACE = r' '
	NEWLINE = r'\n+'

	# parse int
	def MOVE_NUMBER(self, t):
		t.value = int(t.value[:-1])
		return t
	
	# remove newline
	def GAME_INFO(self, t):
		t.value = t.value[:-1]
		return t
	
	def error(self, t):
		raise Exception("Illegal token '%s' line '%d'" % (t.value[0], t.lineno))

# -----------------------------------
# Parser
# -----------------------------------


class ChessParser(Parser):
	gameFinishedCb = None
	gameInfoDetectedCb = None
	movementDetectedCb = None
	tokens = ChessLexer.tokens
	# debugfile = 'parser.out'
	
	start = 'entry'

	currentMove = Movement.Movement()

	def newMovement(self):
		self.currentMove = Movement.Movement()

	def setGameInfoDetectedCallback(self, cb):
		self.gameInfoDetectedCb = cb

	def setMovementDetectedCallback(self, cb):
		self.movementDetectedCb = cb

	def setGameFinishedCallback(self, cb):
		self.gameFinishedCb = cb

	#    Rules
	# ----------

	@_('games', 'game')
	def entry(self, p):
		return p

	@_('games game')
	def games(self, p):
		return p.games + [ p.game ]

	@_('game')
	def games(self, p):
		return [ p.game ]

	@_('info __ movements __ result __')
	def game(self, p):
		if self.gameFinishedCb:
			self.gameFinishedCb(p)
		return p
	
	@_('RESULT')
	def result(self, p):
		return p.RESULT

	@_('empty')
	def result(self, p):
		return "<no-result>"

	@_('empty')
	def info(self, p):
		return []

	@_('info __ GAME_INFO __')
	def info(self, p):
		if self.gameInfoDetectedCb:
			self.gameInfoDetectedCb( p.GAME_INFO )
		return p.info + [p.GAME_INFO]

	@_('GAME_INFO')
	def info(self, p):
		if self.gameInfoDetectedCb:
			self.gameInfoDetectedCb( p.GAME_INFO )
		return [p.GAME_INFO]

	@_('movements movement')
	def movements(self, p):
		return p.movements + [ p.movement ]

	@_('movement')
	def movements(self, p):
		return [ p.movement ]

	@_('')
	def empty(self, p):
		...

	@_('SPACE', 'NEWLINE', 'empty')
	def __(self, p):
		...
	
	@_('PIECE')
	def who(self, p):
		self.currentMove.piece = p.PIECE

	@_('empty')
	def who(self, p):
		self.currentMove.piece = 'p'
	
	@_(		
		'FILE RANK',		# not taking
		'FILE FILE RANK',
		'RANK FILE RANK',
		'FILE RANK FILE RANK',
		'TAKE FILE RANK',	# taking
		'FILE TAKE FILE RANK',
		'RANK TAKE FILE RANK',
		'FILE RANK TAKE FILE RANK'
	)
	def where(self, p):
		if hasattr(p, 'FILE1'):
			self.currentMove.destFile = p.FILE1
			self.currentMove.disFile = p.FILE0
		else:
			self.currentMove.destFile = p.FILE

		if hasattr(p, 'RANK1'):
			self.currentMove.destRank = p.RANK1
			self.currentMove.disRank = p.RANK0
		else:
			self.currentMove.destRank = p.RANK

		if hasattr(p, 'TAKE'):
			self.currentMove.take = True
		return ()

	@_( 'empty')
	def promotion(self, p):
		...

	@_('PROMOTION PIECE')
	def promotion(self, p):
		self.currentMove.crown = True
		self.currentMove.crownTo = p.PIECE

	@_('who where promotion')
	def move(self, p):
		...
	
	@_('castle')
	def move(self, p):
		...

	@_('TAKE', 'empty')
	def take(self, p):
		self.currentMove.take = True

	@_('CASTLE_SHORT')
	def castle(self, p):
		self.currentMove.piece = 'K'
		self.currentMove.castleShort = True

	@_('CASTLE_LONG')
	def castle(self, p):
		self.currentMove.piece = 'K'
		self.currentMove.castleLong = True

	@_('CHECK')
	def modif(self, p):
		self.currentMove.check = True

	@_('empty')
	def modif(self, p):
		return ''

	@_('MOVE_NUMBER __ whiteMovement __ blackMovement __')
	def movement(self, p):
		...

	@_('MOVE_NUMBER __ whiteMovement __')
	def movement(self, p):
		...

	@_('move modif')
	def whiteMovement(self, p):
		self.currentMove.color = 'W'
		if self.movementDetectedCb:
			self.movementDetectedCb(self.currentMove)
			self.newMovement()
			
	@_('move modif')
	def blackMovement(self, p):
		self.currentMove.color = 'B'
		if self.movementDetectedCb:
			self.movementDetectedCb(self.currentMove)
			self.newMovement()

	def error(self, p):
		if p != None:
			raise Exception('Parse Error: "%s"' % p)
# -----------------------------------
# Usage
# -----------------------------------

if __name__ == "__main__":
	lexer = ChessLexer()
	parser = ChessParser()
	cosas = parser.parse(lexer.tokenize(sys.stdin.read()))
	print(cosas)
