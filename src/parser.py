from sly import Lexer
import sys

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

if __name__ == "__main__":
	lexer = ChessLexer()
	tokens = lexer.tokenize(sys.stdin.read())

	for token in tokens:
		print(token)

