from sly import Lexer, Parser
import sys


# -----------------------------------
# Lexer
# -----------------------------------
class ChessLexer(Lexer):
	tokens = { JUGADA_NRO, GAME_INFO, SPACE, PIECE, 
			RANK, FILE, CASTLE_SHORT, CASTLE_LONG, 
			CHECK, TAKE, RESULT, PROMOTION, NEWLINE }

	
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
		raise Exception("Illegal token '%s'" % t.value[0])

# -----------------------------------
# Parser
# -----------------------------------


class ChessParser(Parser):
	tokens = ChessLexer.tokens
	# debugfile = 'parser.out'
	start = 'game'

	@_('info __ movements result __')
	def game(self, p):
		return p
	
	@_('RESULT')
	def result(self, p):
		return p.RESULT

	@_('empty')
	def result(self, p):
		return "<no-result>"

	@_('empty')
	def info(self, p):
		return ()

	@_('info __ GAME_INFO __')
	def info(self, p):
		return p.info + [p.GAME_INFO]

	@_('GAME_INFO')
	def info(self, p):
		return [p.GAME_INFO]

	@_('movements movement')
	def movements(self, p):
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
	
	@_('PIECE')
	def who(self, p):
		return (p.PIECE)

	@_('empty')
	def who(self, p):
		return ('pawn')
	
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
		to = ""
		dis= ""
		if hasattr(p, 'FILE1'):
			to += p.FILE1
			dis += p.FILE0
		else:
			to += p.FILE

		if hasattr(p, 'RANK1'):
			to += p.RANK1
			dis += p.RANK0
		else:
			to += p.RANK

		if hasattr(p, 'TAKE'):
			return ('to (taking)', dis, to)

		return ('to ', dis, to)

	@_( 'empty')
	def promotion(self, p):
		...

	@_('PROMOTION PIECE')
	def promotion(self, p):
		return ('promoted to', p.PIECE)

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
	# print(cosas)
