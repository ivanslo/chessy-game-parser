'''
The next lines are there to deal with python files importing each other inside `src`
'''
import os.path
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


from src import  Board
import pytest

class TestGameController:
    def setup_class(self):
        self.board = Board.Board()


    '''
    tests taken from what Wikipedia says in 'examples' section
    https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
    '''

    def test_initialFen(self):
        initialFen = self.board.toFENposition()
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
        boardFen = self.board.toFENposition()
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
        boardFen = self.board.toFENposition()
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
        boardFen = self.board.toFENposition()
        assert( boardFen == 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R')