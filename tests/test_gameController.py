'''
The next lines are there to deal with python files importing each other inside `src`
alternatively, I need to set `PYTHONPATH=../src` before running pytest
'''
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/parser")))



import parser, Board
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
		self.parser.setMovementDetectedCallback( callback )
		self.parser.parse(self.lexer.tokenize('1. e4 e5 2. Nc3 B3a1 3. a3'))
		assert( 5 == callback.call_count )

	def test_callback_object(self, mocker):
		callback = mocker.stub(name='callback fn')
		self.parser.setMovementDetectedCallback( callback )
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
		self.parser.setMovementDetectedCallback( lambda x: self.board.makeMovement(x) )


	## Pawns
	def test_pawn_basic(self):
		self.parser.parse(self.lexer.tokenize('1. e4 e5'))
		assert(self.board.getLastBoardInFEN() == 'rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR')
		boardDict = self.board.getLastBoardDict()
		assert(boardDict['r1'] == {'pos': 'a8', 'taken': False, 'face': 'r'})
		assert(boardDict['P5'] == {'pos': 'e4', 'taken': False, 'face': 'P'})
		assert(boardDict['p5'] == {'pos': 'e5', 'taken': False, 'face': 'p'})

	def test_pawn(self):
		self.parser.parse(self.lexer.tokenize('1. e4 e5 2. d4 d5 3. dxe5'))
		assert(self.board.getLastBoardInFEN() == 'rnbqkbnr/ppp2ppp/8/3pP3/4P3/8/PPP2PPP/RNBQKBNR')
		
	def test_pawn_en_passant(self):
		self.parser.parse(self.lexer.tokenize("1. e4 a6 2. e5 f5 3. exf6 "))
		assert(self.board.getLastBoardInFEN() == 'rnbqkbnr/1pppp1pp/p4P2/8/8/8/PPPP1PPP/RNBQKBNR')


	## Bishop

	def test_normal_bishop(self):
		self.parser.parse(self.lexer.tokenize("1. e4 e5 2. Bc4 d6 3. d3 Bf5"))
		assert(self.board.getLastBoardInFEN() == "rn1qkbnr/ppp2ppp/3p4/4pb2/2B1P3/3P4/PPP2PPP/RNBQK1NR")

	def test_ambiguous_bishop(self):
		# 4 bishops per side
		self.board.setupBoardInFEN("2bk1b2/8/1b1b4/1B6/5B2/8/8/2B1KB2")
		self.parser.parse(self.lexer.tokenize("1. Bfd3 Bdc5 2. Bce3 Bfd6 3. Ba4 Bxf4"))
		assert(self.board.getLastBoardInFEN() == "2bk4/8/1b6/2b5/B4b2/3BB3/8/4K3")


	## Knight

	def test_normal_knight(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 Nh6"))
		assert(self.board.getLastBoardInFEN() == "rnbqkb1r/pppppppp/7n/8/8/5N2/PPPPPPPP/RNBQKB1R")

	def test_ambiguous_knight(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 Nf6 2. Nc3 Nc6 3. Nd4 Nd5 5. Ncb5 Ndb4 6. Nxc6 dxc6 7. Nd4"))
		assert(self.board.getLastBoardInFEN() == "r1bqkb1r/ppp1pppp/2p5/8/1n1N4/8/PPPPPPPP/R1BQKB1R")


	## Rook

	def test_ambiguous_rook(self):
		self.parser.parse(self.lexer.tokenize("1. a4 a5 2. Ra3 Ra6 3. h4 h5 4. Rhh3 Rhh6 5. Rhe3"))
		assert(self.board.getLastBoardInFEN() == "1nbqkbn1/1pppppp1/r6r/p6p/P6P/R3R3/1PPPPPP1/1NBQKBN1")

	def test_ambiguous_rooks(self):
		# three rooks
		self.board.setupBoardInFEN("2k5/8/5R2/3R4/5R2/8/2K5/8")
		self.parser.parse(self.lexer.tokenize("1. Rf8+ Kc7"))
		assert(self.board.getLastBoardInFEN() == "5R2/2k5/8/3R4/5R2/8/2K5/8")
		self.parser.parse(self.lexer.tokenize("2. Rdf5 Kc6"))
		assert(self.board.getLastBoardInFEN() == "5R2/8/2k5/5R2/5R2/8/2K5/8")
		self.parser.parse(self.lexer.tokenize("3. R8f6"))
		assert(self.board.getLastBoardInFEN() == "8/8/2k2R2/5R2/5R2/8/2K5/8")


	## Queen

	def test_normal_queen(self):
		self.parser.parse(self.lexer.tokenize("1. d4 e5 2. Qd3 Qh4 3. Qb5 Qxd4"))
		assert(self.board.getLastBoardInFEN() == "rnb1kbnr/pppp1ppp/8/1Q2p3/3q4/8/PPP1PPPP/RNB1KBNR")

	def test_ambiguous_queen(self):
		initial_three_queen = "6Q1/6QQ/8/2k5/8/8/2K5/8"
		self.board.setupBoardInFEN(initial_three_queen)
		self.parser.parse(self.lexer.tokenize("1. Qhh8")) #disambiguation with file
		assert(self.board.getLastBoardInFEN() == "6QQ/6Q1/8/2k5/8/8/2K5/8")
		
		self.board.setupBoardInFEN(initial_three_queen)
		self.parser.parse(self.lexer.tokenize("1. Q8h8")) #disambiguation with rank
		assert(self.board.getLastBoardInFEN() == "7Q/6QQ/8/2k5/8/8/2K5/8")

		self.board.setupBoardInFEN(initial_three_queen)
		self.parser.parse(self.lexer.tokenize("1. Qg7h8")) #disambiguation with file and rank
		assert(self.board.getLastBoardInFEN() == "6QQ/7Q/8/2k5/8/8/2K5/8")


	## King

	def test_normal_king(self):
		self.parser.parse(self.lexer.tokenize("1. e4 d5 2. Ke2 Kd7 3. Kd3 Kc6"))
		assert(self.board.getLastBoardInFEN() == "rnbq1bnr/ppp1pppp/2k5/3p4/4P3/3K4/PPPP1PPP/RNBQ1BNR")


	## Castling

	def test_castle_short_white(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 d5 2.e3 Bf5 3.Bb5+ Nd7 4.O-O"))
		assert(self.board.getLastBoardInFEN() == "r2qkbnr/pppnpppp/8/1B1p1b2/8/4PN2/PPPP1PPP/RNBQ1RK1")

	def test_castle_short_black(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 Nf6 2. e3 e6 3. Bc4 Bc5 4. d4 O-O"))
		assert(self.board.getLastBoardInFEN() == "rnbq1rk1/pppp1ppp/4pn2/2b5/2BP4/4PN2/PPP2PPP/RNBQK2R")

	def test_castle_long_white(self):
		self.parser.parse(self.lexer.tokenize("1. d4 d5 2. Nc3 e6 3. Bf4 Nf6 4. Qd2 Na6 5. O-O-O"))
		assert(self.board.getLastBoardInFEN() == "r1bqkb1r/ppp2ppp/n3pn2/3p4/3P1B2/2N5/PPPQPPPP/2KR1BNR")

	def test_castle_long_black(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 d5 2. e3 Bf5 3. Bb5+ Nd7 4. d3 c6 5. Bc4 Qc7 6. h3 O-O-O"))
		assert(self.board.getLastBoardInFEN() == "2kr1bnr/ppqnpppp/2p5/3p1b2/2B5/3PPN1P/PPP2PP1/RNBQK2R")
	
	def test_castle_both(self):
		self.parser.parse(self.lexer.tokenize("1. Nf3 d5 2.e3 Bf5 3.Bb5+ Nd7 4.O-O c6 5.Ba4 Qc7 6.d4 O-O-O"))
		assert(self.board.getLastBoardInFEN() == "2kr1bnr/ppqnpppp/2p5/3p1b2/B2P4/4PN2/PPP2PPP/RNBQ1RK1")

class TestBoardGames:
	parser = ""
	lexer = ""
	board = None

	def setup_class(self):
		self.parser = parser.ChessParser()
		self.lexer = parser.ChessLexer()

	def setup_method(self):
		self.board = Board.Board()
		self.parser.setMovementDetectedCallback( lambda x: self.board.makeMovement(x) )

	def test_wc2013_round6(self):
		self.parser.parse(self.lexer.tokenize("""
[Event "WCh 2013"]
[Site "Chennai IND"]
[Date "2013.11.16"]
[Round "6"]
[White "Anand, Viswanathan"]
[Black "Carlsen, Magnus"]
[Result "0-1"]
[WhiteTitle "GM"]
[BlackTitle "GM"]
[WhiteElo "2775"]
[BlackElo "2870"]
[ECO "C65"]
[Opening "Ruy Lopez"]
[Variation "Berlin defence"]
[WhiteFideId "5000017"]
[BlackFideId "1503014"]
[EventDate "2013.11.09"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 Nf6 4. d3 Bc5 5. c3 O-O 6. O-O Re8 7. Re1 a6 8. Ba4
b5 9. Bb3 d6 10. Bg5 Be6 11. Nbd2 h6 12. Bh4 Bxb3 13. axb3 Nb8 14. h3 Nbd7 15.
Nh2 Qe7 16. Ndf1 Bb6 17. Ne3 Qe6 18. b4 a5 19. bxa5 Bxa5 20. Nhg4 Bb6 21. Bxf6
Nxf6 22. Nxf6+ Qxf6 23. Qg4 Bxe3 24. fxe3 Qe7 25. Rf1 c5 26. Kh2 c4 27. d4 Rxa1
28. Rxa1 Qb7 29. Rd1 Qc6 30. Qf5 exd4 31. Rxd4 Re5 32. Qf3 Qc7 33. Kh1 Qe7 34.
Qg4 Kh7 35. Qf4 g6 36. Kh2 Kg7 37. Qf3 Re6 38. Qg3 Rxe4 39. Qxd6 Rxe3 40. Qxe7
Rxe7 41. Rd5 Rb7 42. Rd6 f6 43. h4 Kf7 44. h5 gxh5 45. Rd5 Kg6 46. Kg3 Rb6 47.
Rc5 f5 48. Kh4 Re6 49. Rxb5 Re4+ 50. Kh3 Kg5 51. Rb8 h4 52. Rg8+ Kh5 53. Rf8 Rf4
54. Rc8 Rg4 55. Rf8 Rg3+ 56. Kh2 Kg5 57. Rg8+ Kf4 58. Rc8 Ke3 59. Rxc4 f4 60.
Ra4 h3 61. gxh3 Rg6 62. c4 f3 63. Ra3+ Ke2 64. b4 f2 65. Ra2+ Kf3 66. Ra3+ Kf4
67. Ra8 Rg1 0-11
"""))
		assert(self.board.getLastBoardInFEN() == "R7/8/7p/8/1PP2k2/7P/5p1K/6r1")

	def test_wc2013_round9(self):
		self.parser.parse(self.lexer.tokenize("""
[Event "WCh 2013"]
[Site "Chennai IND"]
[Date "2013.11.21"]
[Round "9"]
[White "Anand, Viswanathan"]
[Black "Carlsen, Magnus"]
[Result "0-1"]
[WhiteTitle "GM"]
[BlackTitle "GM"]
[WhiteElo "2775"]
[BlackElo "2870"]
[ECO "E25"]
[Opening "Nimzo-Indian"]
[Variation "Saemisch variation"]
[WhiteFideId "5000017"]
[BlackFideId "1503014"]
[EventDate "2013.11.09"]

1. d4 Nf6 2. c4 e6 3. Nc3 Bb4 4. f3 d5 5. a3 Bxc3+ 6. bxc3 c5 7. cxd5 exd5 8. e3
c4 9. Ne2 Nc6 10. g4 O-O 11. Bg2 Na5 12. O-O Nb3 13. Ra2 b5 14. Ng3 a5 15. g5
Ne8 16. e4 Nxc1 17. Qxc1 Ra6 18. e5 Nc7 19. f4 b4 20. axb4 axb4 21. Rxa6 Nxa6
22. f5 b3 23. Qf4 Nc7 24. f6 g6 25. Qh4 Ne8 26. Qh6 b2 27. Rf4 b1=Q+ 28. Nf1 Qe1 0-1
"""))
		assert(self.board.getLastBoardInFEN() == "2bqnrk1/5p1p/5PpQ/3pP1P1/2pP1R2/2P5/6BP/4qNK1")
	def test_fideWorldRapid2014_2_2(self):
		self.parser.parse(self.lexer.tokenize("""
[Event "FIDE World Rapid 2014"]
[Site "Dubai UAE"]
[Date "2014.06.16"]
[Round "2.2"]
[White "Guseinov,G"]
[Black "Carlsen,M"]
[Result "1/2-1/2"]
[WhiteElo "2613"]
[BlackElo "2881"]
[ECO "C08"]

1.e4 e6 2.d4 d5 3.Nd2 c5 4.exd5 exd5 5.Bb5+ Nc6 6.Ngf3 cxd4 7.O-O Bd6 8.Re1+ Ne7
9.Nxd4 O-O 10.N2b3 Qc7 11.h3 a6 12.Bd3 Ne5 13.Bf4 N7g6 14.Bxg6 fxg6 15.Bxe5 Bxe5
16.c3 Qd6 17.Qd3 Bd7 18.Re2 Rae8 19.Rae1 g5 20.Nd2 g4 21.hxg4 Bh2+ 22.Kf1 Rxe2
23.Kxe2 Bxg4+ 24.f3 Bd7 25.Kd1 Bf4 26.Kc2 Qf6 27.N2b3 Be8 28.Nf5 Kh8 29.Nbd4 Bg6
30.g4 Be5 31.Kd1 h6 32.Qe3 Re8 33.Qd2 Kh7 34.a3 a5 35.Re2 Qa6 36.Re1 Bf4
37.Qc2 Rxe1+ 38.Kxe1 Qf6 39.Qe2 Bf7 40.Kd1 g6 41.Ne3 h5 42.gxh5 gxh5 43.Ng2 Bh6
44.Qd3+ Bg6 45.Qb5 h4 46.Qd7+ Kg8 47.Qc8+ Kh7 48.Qd7+ Kg8 49.Qc8+ Kh7 50.Qd7+ Kh8
51.Qc8+ Kh7  1/2-1/2
"""))
		assert(self.board.getLastBoardInFEN() == "2Q5/1p5k/5qbb/p2p4/3N3p/P1P2P2/1P4N1/3K4")


class TestMultipleGames:
	parser = ""
	lexer = ""

	def setup_class(self):
		self.parser = parser.ChessParser()
		self.lexer = parser.ChessLexer()

	def test_wc2013_all(self, mocker):
		callback = mocker.stub(name='game detected fn')
		self.parser.setGameFinishedCallback(callback)
		self.parser.parse(self.lexer.tokenize("""
[Event "WCh 2013"]
[Round "1"]

1. d4 Nf6 2. c4 e6 1/2-1/2

[Event "WCh 2013"]
[Round "2"]

1. d4 Nf6 2. c4 e6 1/2-1/2
"""))
		assert( 2 == callback.call_count )
