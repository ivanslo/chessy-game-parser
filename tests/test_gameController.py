'''
The next lines are there to deal with python files importing each other inside `src`
'''
import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))



from src import parser, Board
import pytest
from pytest_mock import mocker

class TestGameController:
	parser = ""
	lexer = ""


	def setup_class(self):
		self.parser = parser.ChessParser()
		self.lexer = parser.ChessLexer()

	
	def test_callback(self, mocker):
		callback = mocker.stub(name='callback fn')
		self.parser.setCallbackFunction( callback )
		self.parser.parse(self.lexer.tokenize('1. e4 e5 2. Nc3 B3a1 3. a3'))
		assert( 5 == callback.call_count )

	def test_callback_object(self, mocker):
		callback = mocker.stub(name='callback fn')
		self.parser.setCallbackFunction( callback )
		self.parser.parse(self.lexer.tokenize('1. e4'))
		assert( 1 == callback.call_count )
		
class TestBoardPositions:
	parser = ""
	lexer = ""
	board = None

	''' 
	All expected outputs have been verified with lychess.org/analysis
	'''
	def setup_class(self):
		self.parser = parser.ChessParser()
		self.lexer = parser.ChessLexer()
	
	def setup_method(self):
		'''
		for each test case, a new board (starting from scratch) should be set up
		'''
		self.board = Board.Board()
		self.parser.setCallbackFunction( lambda x: self.board.makeMovement(x) )

	def test_pawn(self):
		self.parser.parse(self.lexer.tokenize('1. e4 e5 2. d4 d5 3. dxe5'))
		assert(self.board.toFENposition() == 'rnbqkbnr/ppp2ppp/8/3pP3/4P3/8/PPP2PPP/RNBQKBNR')
		
	def test_pawn_en_passant(self):
		self.parser.parse(self.lexer.tokenize("1. e4 a6 2. e5 f5 3. exf6 "))
		assert(self.board.toFENposition() == 'rnbqkbnr/1pppp1pp/p4P2/8/8/8/PPPP1PPP/RNBQKBNR')

	def test_normal_bishop(self):
		self.parser.parse(self.lexer.tokenize("1. e4 e5 2. Bc4 d6 3. d3 Bf5"))
		assert(self.board.toFENposition() == "rn1qkbnr/ppp2ppp/3p4/4pb2/2B1P3/3P4/PPP2PPP/RNBQK1NR")

	def test_normal_knight(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 Nh6"))
		assert(self.board.toFENposition() == "rnbqkb1r/pppppppp/7n/8/8/5N2/PPPPPPPP/RNBQKB1R")

	def test_ambiguous_knight(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 Nf6 2. Nc3 Nc6 3. Nd4 Nd5 5. Ncb5 Ndb4 6. Nxc6 dxc6 7. Nd4"))
		assert(self.board.toFENposition() == "r1bqkb1r/ppp1pppp/2p5/8/1n1N4/8/PPPPPPPP/R1BQKB1R")

	def test_ambiguous_rook(self):
		self.parser.parse(self.lexer.tokenize("1. a4 a5 2. Ra3 Ra6 3. h4 h5 4. Rhh3 Rhh6 5. Rhe3"))
		assert(self.board.toFENposition() == "1nbqkbn1/1pppppp1/r6r/p6p/P6P/R3R3/1PPPPPP1/1NBQKBN1")

	def test_normal_queen(self):
		self.parser.parse(self.lexer.tokenize("1. d4 e5 2. Qd3 Qh4 3. Qb5 Qxd4"))
		assert(self.board.toFENposition() == "rnb1kbnr/pppp1ppp/8/1Q2p3/3q4/8/PPP1PPPP/RNB1KBNR")

	def test_normal_king(self):
		self.parser.parse(self.lexer.tokenize("1. e4 d5 2. Ke2 Kd7 3. Kd3 Kc6"))
		assert(self.board.toFENposition() == "rnbq1bnr/ppp1pppp/2k5/3p4/4P3/3K4/PPPP1PPP/RNBQ1BNR")
