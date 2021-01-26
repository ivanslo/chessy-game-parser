'''
The next lines are there to deal with python files importing each other inside `src`
alternatively, I need to set `PYTHONPATH=../src` before running pytest
'''
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/parser")))



import  Board
import Movement
import pytest

class TestGameController:
    def setup_class(self):
        self.board = Board.Board()


    '''
    tests taken from what Wikipedia says in 'examples' section
    https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    '''

    def test_initialFen(self):
        initialFen = self.board.getLastBoardInFEN()
        assert( initialFen == 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')

    def test_afterOneMoveFen(self):
        board_e4 = [ 
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', ' ', 'P', 'P', 'P'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'P', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]
        self.board.addBoard(board_e4)
        boardFen = self.board.getLastBoardInFEN()
        assert( boardFen == 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR')
    
    def test_afterTwoMovesFen(self):
        board_e4_c5 = [ 
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', ' ', 'P', 'P', 'P'],
            [ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [ ' ', ' ', ' ', ' ', 'P', ' ', ' ', ' '],
            [ ' ', ' ', 'p', ' ', ' ', ' ', ' ', ' '],
            [ ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', 'p', ' ', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]
        self.board.addBoard(board_e4_c5)
        boardFen = self.board.getLastBoardInFEN()
        assert( boardFen == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR')


    def test_afterThreeMovesFen(self):
        board_e4_c5_Nf3 = [ 
            ['R', 'N', 'B', 'Q', 'K', 'B', ' ', 'R'],
            ['P', 'P', 'P', 'P', ' ', 'P', 'P', 'P'],
            [' ', ' ', ' ', ' ', ' ', 'N', ' ', ' '],
            [' ', ' ', ' ', ' ', 'P', ' ', ' ', ' '],
            [' ', ' ', 'p', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', 'p', ' ', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]
        self.board.addBoard(board_e4_c5_Nf3)
        boardFen = self.board.getLastBoardInFEN()
        assert( boardFen == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R')

    def test_fenToBoard_OneMove(self):
        fen_e4 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR"
        self.board.addBoardInFEN(fen_e4)
        board = self.board.getLastBoard()
        assert( board == [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', ' ', 'P', 'P', 'P'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', 'P', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']])

    def test_fenToBoard_ThreeMoves(self):
        fen_e4_c5_Nf3 = 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R'
        self.board.addBoardInFEN(fen_e4_c5_Nf3)
        board = self.board.getLastBoard()
        assert( board == [
            ['R', 'N', 'B', 'Q', 'K', 'B', ' ', 'R'],
            ['P', 'P', 'P', 'P', ' ', 'P', 'P', 'P'],
            [' ', ' ', ' ', ' ', ' ', 'N', ' ', ' '],
            [' ', ' ', ' ', ' ', 'P', ' ', ' ', ' '],
            [' ', ' ', 'p', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', 'p', ' ', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'] ])

    def test_randomBoard(self):
        fen_board = '8/4k3/3b1q2/2ppn3/2B3bP/2N1B1K1/P3N3/R2Q3R'
        # corroborate in lichess that the output board is correct
        self.board.addBoardInFEN(fen_board)
        board = self.board.getLastBoard()
        assert( board == [
            ['R', ' ', ' ', 'Q', ' ', ' ', ' ', 'R'],
            ['P', ' ', ' ', ' ', 'N', ' ', ' ', ' '],
            [' ', ' ', 'N', ' ', 'B', ' ', 'K', ' '],
            [' ', ' ', 'B', ' ', ' ', ' ', 'b', 'P'],
            [' ', ' ', 'p', 'p', 'n', ' ', ' ', ' '],
            [' ', ' ', ' ', 'b', ' ', 'q', ' ', ' '],
            [' ', ' ', ' ', ' ', 'k', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '] ])

    '''
    right choice of piece-to-move
    '''
    def  test_filterOutPossibleMovement_1(self):
        '''
        Example: Classics GM, Gausdal NOR, 2002.04.17, round 8, Carlsen vs Bluvshtein, movement 42. ... Rg8
        '''
        board_initial_in_FEN = '5r2/p4p1k/6rb/8/4Q1R1/2P1p2P/PP5P/7K'
        self.board.addBoardInFEN(board_initial_in_FEN)
        # Note: the movement doesn't say which of the two rooks to move.s
        # The board discard the one in g6 -because its illegal- and use the one in f8
        movement = Movement.Movement()
        movement.piece= 'R'
        movement.destFile = 'g'
        movement.destRank = '8'
        movement.color = 'B'
        self.board.makeMovement(movement)

        boardFEN = self.board.getLastBoardInFEN()
        assert( boardFEN == '6r1/p4p1k/6rb/8/4Q1R1/2P1p2P/PP5P/7K')

    def  test_filterOutPossibleMovement_2(self):
        '''
        Example: Montevideo sim, Montevideo, 1911.??.??, Capablanca vs Rivas Costa, movement 9. Ne2
        '''
        board_initial_in_FEN = 'rnbqk2r/pp4pp/4pn2/2pp2B1/1b1P4/2NBQP2/PPP3PP/R3K1NR'
        self.board.addBoardInFEN(board_initial_in_FEN)
        # Note: the movement doesn't say which of the two Knigths to move
        # The board discard the one in c3 -because its illegal- and use the one in g1
        movement = Movement.Movement()
        movement.piece= 'N'
        movement.destFile = 'e'
        movement.destRank = '2'
        movement.color = 'W'
        self.board.makeMovement(movement)

        boardFEN = self.board.getLastBoardInFEN()
        assert( boardFEN == 'rnbqk2r/pp4pp/4pn2/2pp2B1/1b1P4/2NBQP2/PPP1N1PP/R3K2R')