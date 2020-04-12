from sly import Lexer, Parser
import sys


# -----------------------------------
# Lexer
# -----------------------------------
class ChessLexer(Lexer):
	tokens = { JUGADA_NRO, GAME_INFO, SPACE, PIECE, RANK, FILE, CASTLE1, CASTLE2, CHECK, TAKE, RESULT, PROMOTION }

	
	RESULT = r'[012/]+-[012/]+'
	GAME_INFO = r'\[.+\]\n'
	JUGADA_NRO = r'\d+\.'
	PIECE = r'[QKNRB]'
	FILE = r'[abcdefgh]'
	RANK= r'[12345678]'
	CASTLE1 = r'O-O'
	CASTLE2 = r'O-O-O'
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
	def empty(self,p):
		pass

	@_('SPACE', 'empty')
	def whatever(self,p):
		...

	@_('JUGADA_NRO SPACE PIECE FILE RANK SPACE PIECE FILE RANK whatever')
	def movement(self, p):
		return ('movement', p.JUGADA_NRO, p.PIECE0, p.FILE0, p.RANK0, p.PIECE1, p.FILE1, p.RANK1)


# -----------------------------------
# Usage
# -----------------------------------

if __name__ == "__main__":
	lexer = ChessLexer()
	parser = ChessParser()
	parser.parse(lexer.tokenize(sys.stdin.read()))
