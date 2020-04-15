from sly import Lexer, Parser
import sys


# -----------------------------------
# Lexer
# -----------------------------------
class ChessLexer(Lexer):
	tokens = { JUGADA_NRO, GAME_INFO, SPACE, PIECE, RANK, FILE, CASTLE_SHORT, CASTLE_LONG, CHECK, TAKE, RESULT, PROMOTION, NEWLINE }

	
	RESULT = r'[012/]+-[012/]+'
	GAME_INFO = r'\[.+\]\n'
	JUGADA_NRO = r'\d+\.'
	PIECE = r'[QKNRB]'
	FILE = r'[abcdefgh]'
	RANK= r'[12345678]'
	CASTLE_LONG = r'O-O-O'
	CASTLE_SHORT = r'O-O'
	CHECK = r'\+'
	TAKE = r'x'
	PROMOTION = r'='
	SPACE = r' '
	NEWLINE = r'\n'

	# parse int
	def JUGADA_NRO(self, t):
		t.value = int(t.value[:-1])
		return t
	
	# remove newline
	def GAME_INFO(self, t):
		t.value = t.value[:-1]
		return t
	
	def error(self, t):
		print("Illegal character '%s'" % t.value[0])
		self.index += 1

# -----------------------------------
# Parser
# -----------------------------------


class ChessParser(Parser):
	tokens = ChessLexer.tokens
	# debugfile = 'parser.out'

	@_('info movements RESULT __')
	def game(self, p):
		return p
	
	@_('info __ GAME_INFO __', 'empty')
	def info(self, p):
		try:
			return p.info + [p.GAME_INFO]
		except:
			return ()

	@_('GAME_INFO')
	def info(self, p):
		return [p.GAME_INFO]

	@_('movements movement')
	def movements(self, p):
		# print(p.movement)
		return p.movements + [ p.movement ]

	@_('movement')
	def movements(self, p):
		return [ p.movement ]

	@_('')
	def empty(self, p):
		pass

	@_('SPACE', 'NEWLINE', 'empty')
	def __(self, p):
		...
	
	@_('PIECE', 'empty')
	def who(self, p):
		try:
			return ( p.PIECE)
		except:
			return ('pawn')
	
	@_(		'FILE RANK', 
			'TAKE FILE RANK',
			'FILE FILE RANK',
			'FILE TAKE FILE RANK',
			'RANK FILE RANK',
			'RANK TAKE FILE RANK',
			'FILE RANK FILE RANK',
			'FILE RANK TAKE FILE RANK'
		)
	def where(self, p):
		extra = ""
		try:
			to = p.FILE
		except:
			to = ""
		try:
			to += p.RANK
		except:
			...
		disamb = ""

		if hasattr(p, 'TAKE'):
			extra = 'TAKE'
		if hasattr(p, 'FILE0'):
			disamb = p.FILE0
			to = p.FILE1
		if hasattr(p, 'RANK0'):
			disamb += p.RANK0
			to += p.RANK1

		if disamb != "":
			return ('to '+extra, disamb, to)

		return ('to' + extra, to)

		

	@_('PROMOTION PIECE', 'empty')
	def promotion(self, p):
		try:
			return ('promoted to', p.PIECE)
		except:
			return None

	@_('who where promotion')
	def move(self, p):
		return ( p.who, p.where, p.promotion)
	
	@_('castle')
	def move(self, p):
		return ('castle', p.castle)

	@_('TAKE', 'empty')
	def take(self, p):
		return p[0]

	@_('CASTLE_SHORT')
	def castle(self, p):
		return p.CASTLE_SHORT

	@_('CASTLE_LONG')
	def castle(self, p):
		return p.CASTLE_LONG

	@_('CHECK')
	def modif(self, p):
		return p.CHECK

	@_('empty')
	def modif(self, p):
		return ''

	@_('JUGADA_NRO __ move modif __ move modif __')
	def movement(self, p):
		return (
				(p.JUGADA_NRO, 'white', p.move0, p.modif0),
				(p.JUGADA_NRO, 'black', p.move1, p.modif1)
				)

	@_('JUGADA_NRO __ move modif __')
	def movement(self, p):
		return (p.JUGADA_NRO, 'white', p.move, p.modif)

# -----------------------------------
# Usage
# -----------------------------------

if __name__ == "__main__":
	lexer = ChessLexer()
	parser = ChessParser()
	cosas = parser.parse(lexer.tokenize(sys.stdin.read()))
	# print(cosas)
