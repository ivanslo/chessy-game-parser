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


	## Pawns

	def test_pawn(self):
		self.parser.parse(self.lexer.tokenize('1. e4 e5 2. d4 d5 3. dxe5'))
		assert(self.board.toFENposition() == 'rnbqkbnr/ppp2ppp/8/3pP3/4P3/8/PPP2PPP/RNBQKBNR')
		
	def test_pawn_en_passant(self):
		self.parser.parse(self.lexer.tokenize("1. e4 a6 2. e5 f5 3. exf6 "))
		assert(self.board.toFENposition() == 'rnbqkbnr/1pppp1pp/p4P2/8/8/8/PPPP1PPP/RNBQKBNR')

	## Bishop

	def test_normal_bishop(self):
		self.parser.parse(self.lexer.tokenize("1. e4 e5 2. Bc4 d6 3. d3 Bf5"))
		assert(self.board.toFENposition() == "rn1qkbnr/ppp2ppp/3p4/4pb2/2B1P3/3P4/PPP2PPP/RNBQK1NR")

	def test_ambiguous_bishop(self):
		# 4 bishops per side
		self.board.addBoardInFEN("2bk1b2/8/1b1b4/1B6/5B2/8/8/2B1KB2")
		self.parser.parse(self.lexer.tokenize("1. Bfd3 Bdc5 2. Bce3 Bfd6 3. Ba4 Bxf4"))
		assert(self.board.toFENposition() == "2bk4/8/1b6/2b5/B4b2/3BB3/8/4K3")

	## Knight

	def test_normal_knight(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 Nh6"))
		assert(self.board.toFENposition() == "rnbqkb1r/pppppppp/7n/8/8/5N2/PPPPPPPP/RNBQKB1R")

	def test_ambiguous_knight(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 Nf6 2. Nc3 Nc6 3. Nd4 Nd5 5. Ncb5 Ndb4 6. Nxc6 dxc6 7. Nd4"))
		assert(self.board.toFENposition() == "r1bqkb1r/ppp1pppp/2p5/8/1n1N4/8/PPPPPPPP/R1BQKB1R")

	## Rook

	def test_ambiguous_rook(self):
		self.parser.parse(self.lexer.tokenize("1. a4 a5 2. Ra3 Ra6 3. h4 h5 4. Rhh3 Rhh6 5. Rhe3"))
		assert(self.board.toFENposition() == "1nbqkbn1/1pppppp1/r6r/p6p/P6P/R3R3/1PPPPPP1/1NBQKBN1")

	def test_ambiguous_rooks(self):
		# three rooks
		self.board.addBoardInFEN("2k5/8/5R2/3R4/5R2/8/2K5/8")
		self.parser.parse(self.lexer.tokenize("1. Rf8+ Kc7"))
		assert(self.board.toFENposition() == "5R2/2k5/8/3R4/5R2/8/2K5/8")
		self.parser.parse(self.lexer.tokenize("2. Rdf5 Kc6"))
		assert(self.board.toFENposition() == "5R2/8/2k5/5R2/5R2/8/2K5/8")
		self.parser.parse(self.lexer.tokenize("3. R8f6"))
		assert(self.board.toFENposition() == "8/8/2k2R2/5R2/5R2/8/2K5/8")

	## Queen

	def test_normal_queen(self):
		self.parser.parse(self.lexer.tokenize("1. d4 e5 2. Qd3 Qh4 3. Qb5 Qxd4"))
		assert(self.board.toFENposition() == "rnb1kbnr/pppp1ppp/8/1Q2p3/3q4/8/PPP1PPPP/RNB1KBNR")

	def test_ambiguous_queen(self):
		initial_three_queen = "6Q1/6QQ/8/2k5/8/8/2K5/8"
		self.board.addBoardInFEN(initial_three_queen)
		self.parser.parse(self.lexer.tokenize("1. Qhh8")) #disambiguation with file
		assert(self.board.toFENposition() == "6QQ/6Q1/8/2k5/8/8/2K5/8")
		
		self.board.addBoardInFEN(initial_three_queen)
		self.parser.parse(self.lexer.tokenize("1. Q8h8")) #disambiguation with rank
		assert(self.board.toFENposition() == "7Q/6QQ/8/2k5/8/8/2K5/8")

		self.board.addBoardInFEN(initial_three_queen)
		self.parser.parse(self.lexer.tokenize("1. Qg7h8")) #disambiguation with file and rank
		assert(self.board.toFENposition() == "6QQ/7Q/8/2k5/8/8/2K5/8")

	## King

	def test_normal_king(self):
		self.parser.parse(self.lexer.tokenize("1. e4 d5 2. Ke2 Kd7 3. Kd3 Kc6"))
		assert(self.board.toFENposition() == "rnbq1bnr/ppp1pppp/2k5/3p4/4P3/3K4/PPPP1PPP/RNBQ1BNR")

	## Castling

	def test_castle_short_white(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 d5 2.e3 Bf5 3.Bb5+ Nd7 4.O-O"))
		assert(self.board.toFENposition() == "r2qkbnr/pppnpppp/8/1B1p1b2/8/4PN2/PPPP1PPP/RNBQ1RK1")

	def test_castle_short_black(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 Nf6 2. e3 e6 3. Bc4 Bc5 4. d4 O-O"))
		assert(self.board.toFENposition() == "rnbq1rk1/pppp1ppp/4pn2/2b5/2BP4/4PN2/PPP2PPP/RNBQK2R")

	def test_castle_long_white(self):
		self.parser.parse(self.lexer.tokenize("1. d4 d5 2. Nc3 e6 3. Bf4 Nf6 4. Qd2 Na6 5. O-O-O"))
		assert(self.board.toFENposition() == "r1bqkb1r/ppp2ppp/n3pn2/3p4/3P1B2/2N5/PPPQPPPP/2KR1BNR")

	def test_castle_long_black(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 d5 2. e3 Bf5 3. Bb5+ Nd7 4. d3 c6 5. Bc4 Qc7 6. h3 O-O-O"))
		assert(self.board.toFENposition() == "2kr1bnr/ppqnpppp/2p5/3p1b2/2B5/3PPN1P/PPP2PP1/RNBQK2R")
	
	def test_castle_both(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 d5 2.e3 Bf5 3.Bb5+ Nd7 4.O-O c6 5.Ba4 Qc7 6.d4 O-O-O"))
		assert(self.board.toFENposition() == "2kr1bnr/ppqnpppp/2p5/3p1b2/B2P4/4PN2/PPP2PPP/RNBQ1RK1")