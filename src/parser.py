from sly import Lexer, Parser
import sys


# -----------------------------------
# Lexer
# -----------------------------------
class ChessLexer(Lexer):
	tokens = { JUGADA_NRO, GAME_INFO, SPACE, PIECE, RANK, FILE, CASTLE_SHORT, CASTLE_LONG, CHECK, TAKE, RESULT, PROMOTION }

	
	RESULT = r'[012/]+-[012/]+'
	GAME_INFO = r'\[.+\]\n'
	JUGADA_NRO = r'\d+\.'
	PIECE = r'[QKNRB]'
	FILE = r'[abcdefgh]'
	RANK= r'[12345678]'
	CASTLE_SHORT = r'O-O'
	CASTLE_LONG = r'O-O-O'
	CHECK = r'\+'
	TAKE = r'x'
	PROMOTION = r'='
	SPACE = r' '

	ignore_newline = r'\n'

	def error(self, t):
		print("Illegal character '%s'" % t.value[0])
		self.index += 1

# -----------------------------------
# Parser
# -----------------------------------
class ChessParser(Parser):
	tokens = ChessLexer.tokens
	debugfile = 'parser.out'


	@_('movements')
	def game(self, p):
		...
	
	@_('movements movement')
	def movements(self, p):
		print( p[1] )

	@_('empty')
	def movements(self, p):
		...

	@_('')
	def empty(self, p):
		pass

	@_('SPACE', 'empty')
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

		

	@_('who where', 'castle')
	def move(self, p):
		try:
			return ( p.who, p.where)
		except:
			return ('castle', p[0])

	@_('TAKE', 'empty')
	def take(self, p):
		return p[0]

	@_('CASTLE_SHORT', 'CASTLE_LONG')
	def castle(self, p):
		try:
			return p.CASTLE_SHORT
		except:
			return p.CASTLE_LONG

	@_('CHECK', 'empty')
	def modif(self, p):
		try:
			if p.CHECK:
				return 'CHECK'
		except:
			return ''

	@_('JUGADA_NRO __ move modif __ move modif __')
	def movement(self, p):
		return (
				(p.JUGADA_NRO, 'white', p.move0, p.modif0),
				(p.JUGADA_NRO, 'black', p.move1, p.modif1)
				)

# -----------------------------------
# Usage
# -----------------------------------

if __name__ == "__main__":
	lexer = ChessLexer()
	parser = ChessParser()
	parser.parse(lexer.tokenize(sys.stdin.read()))
