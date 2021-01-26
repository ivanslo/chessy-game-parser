'''
The next lines are there to deal with python files importing each other inside `src`
alternatively, I need to set `PYTHONPATH=../src` before running pytest
'''
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/parser")))


import parser
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
	
	def parse(self,text):
		return self.parser.parse(self.lexer.tokenize(text))

	def test_basic_game(self):
		_ = self.parse("1. e3 e4 2.Ke3 exd5")

	def test_castle(self):
		_ = self.parse("23. O-O-O O-O")

	def test_promote(self):
		_ = self.parse("23. e8=Q e1 24. a8=N R3")

	def test_check(self):
		_ = self.parse("23. Ra3+ Be3+")

	def test_disamb_move(self):
		non_eat = self.parse("1. Ra3 Beh3 3.B2c3 Re4h8 ")
		eating  = self.parse("1. Rxa3 Bexh3 3.B2xc3 Re4xh8") 

	def test_gameinfo(self):
		result = self.parse("[Day 3]\n [Result 1-0]\n1. e4 ")
		print(result)
		assert( result != None )

	def test_result(self):
		result = self.parse("1. e4 1-0")
		assert( result != None )

	def test_no_result(self):
		result = self.parse("1. e4")
		assert( result != None )
		
	def test_gameinfo_2(self):
		result = self.parse("[Day 3]\n 1. e4 ")
		print(result)
		assert( result != None )

	def test_gameinfo_3(self):
		result = self.parse("1. e4 ")
		print(result)
		assert( result != None )
