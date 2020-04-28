from src import parser
import pytest

def count(generator):
	return sum(1 for x in generator)

''' Lexer Tests '''
class TestLexer:
	lexer = ""

	def setup_class(self):
		self.lexer = parser.ChessLexer()

	def test_basic_tokens_1(self):
		tokens = self.lexer.tokenize("e3 e4")
		assert( count(tokens) == 5 )

	def test_basic_tokens_2(self):
		tokens = self.lexer.tokenize("e3")
		assert( count(tokens) == 2 )

	''' these tests pass if no exception is thrown '''
	def test_play_1(self):
		tokens = self.lexer.tokenize("1. e3 e4 2.Ke3 R3e2 3.Bd8=K")
		count(tokens)

	def test_play_2(self):
		tokens = self.lexer.tokenize("1. Ra3e7+")
		count(tokens)
		
	def test_play_3(self):
		tokens = self.lexer.tokenize("22. a3 O-O 23.O-O-O K3xe3 ")
		count(tokens)

	def test_error_token(self):
		with pytest.raises(Exception) as e_info:
			self.lexer.tokenize("&")
			count(tokens)



''' Parser Tests '''
class TestParser:
	parser = ""
	lexer = ""

	def setup_class(self):
		self.parser = parser.ChessParser()
		self.lexer = parser.ChessLexer()
	
	def test_basic_game(self):
		_ = self.parser.parse(self.lexer.tokenize("1. e3 e4 2.Ke3 exd5"))

	def test_castle(self):
		_ = self.parser.parse(self.lexer.tokenize("23. O-O-O O-O"))

	def test_promote(self):
		_ = self.parser.parse(self.lexer.tokenize("23. e8=Q"))

	def test_check(self):
		_ = self.parser.parse(self.lexer.tokenize("23. Ra3+ Be3+"))

	def test_disamb(self):
		_ = self.parser.parse(self.lexer.tokenize("2. R2a3 Beh3 3.Ba2c3 Rh8"))
