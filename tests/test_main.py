'''
The next lines are there to deal with python files importing each other inside `src`
alternatively, I need to set `PYTHONPATH=../src` before running pytest
'''
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/parser")))

import unittest
import GameController

class TestGameControllerReal:
	def test_processPGNText_1(self):
		result = GameController.processPGNText("""
[Event "Havana"]
[Site "Havana CUB"]
[Date "1965.08.26"]
[EventDate "1965.08.25"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 
""")
		movements = 8
		assert( len(result) == 1 )
		assert( result[0].id == "Havana_HavanaCUB_19650826" )
		assert( result[0].info["Event"] == "Havana" )
		assert( len(result[0].steps) == movements+1 )

	def test_processPGNText_2(self):
		result = GameController.processPGNText(
"""
[Event "Anand-Carlsen World Championship"]
[Site "Chennai IND"]
[Date "2013.11.21"]
[EventDate "2013.11.07"]
[Round "9"]

1.d4 Nf6 2.c4 e6 3.Nc3 Bb4  1-1

[Event "Gashimov Memorial"]
[Site "Shamkir AZE"]
[Date "2015.04.21"]
[EventDate "2015.04.17"]
[Round "5"]

1.Nf3 Nf6 2.g3 b5 3.Bg2 Bb7 1-0
""")
		movements = 6
		assert( len(result) == 2 )
		assert( result[0].id == "AnandCarlsenWorldChampionship_ChennaiIND_20131121_9" )
		assert( len(result[0].steps) == movements+1 )

		assert( result[1].id == "GashimovMemorial_ShamkirAZE_20150421_5" )
		assert( len(result[1].steps) == movements+1 )
	
	def test_processPGNText_3(self):
		result = GameController.processPGNText(
"""
[Event "Anand-Carlsen World Championship"]
[Site "Chennai IND"]
[Date "2013.11.21"]
[EventDate "2013.11.07"]
[Round "9"]

1.d4 Nf6 2.c4 e6 3.Nc3 Bb4  1-1
""")
		movements = 6
		assert( result[0].id == "AnandCarlsenWorldChampionship_ChennaiIND_20131121_9" )
		assert( len(result[0].steps) == movements+1 )
		assert( result[0].steps[0]['board'] == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" )
		assert( result[0].steps[1]['board'] == "rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR")

	def test_processPGNText_format(self):
		result = GameController.processPGNText("""
[Event "Havana"]
[Site "Havana CUB"]
[Date "1965.08.26"]
[EventDate "1965.08.25"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 
""")
		movements = 8
		assert( len(result) == 1 )
		assert( result[0].id == "Havana_HavanaCUB_19650826" )
		assert( result[0].info["Event"] == "Havana" )
		assert( len(result[0].steps) == movements+1 )
		assert( result[0].steps[0] == {
			'board':"rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR",
			'boardDict': {
				'r1': { 'pos': "a8" , 'face': "r" , 'taken': False },
				'n1': { 'pos': "b8" , 'face': "n" , 'taken': False },
				'b1': { 'pos': "c8" , 'face': "b" , 'taken': False },
				'q1': { 'pos': "d8" , 'face': "q" , 'taken': False },
				'k1': { 'pos': "e8" , 'face': "k" , 'taken': False },
				'b2': { 'pos': "f8" , 'face': "b" , 'taken': False },
				'n2': { 'pos': "g8" , 'face': "n" , 'taken': False },
				'r2': { 'pos': "h8" , 'face': "r" , 'taken': False },
				'p1': { 'pos': "a7" , 'face': "p" , 'taken': False },
				'p2': { 'pos': "b7" , 'face': "p" , 'taken': False },
				'p3': { 'pos': "c7" , 'face': "p" , 'taken': False },
				'p4': { 'pos': "d7" , 'face': "p" , 'taken': False },
				'p5': { 'pos': "e7" , 'face': "p" , 'taken': False },
				'p6': { 'pos': "f7" , 'face': "p" , 'taken': False },
				'p7': { 'pos': "g7" , 'face': "p" , 'taken': False },
				'p8': { 'pos': "h7" , 'face': "p" , 'taken': False },
				'R1': { 'pos': "a1" , 'face': "R" , 'taken': False },
				'N1': { 'pos': "b1" , 'face': "N" , 'taken': False },
				'B1': { 'pos': "c1" , 'face': "B" , 'taken': False },
				'Q1': { 'pos': "d1" , 'face': "Q" , 'taken': False },
				'K1': { 'pos': "e1" , 'face': "K" , 'taken': False },
				'B2': { 'pos': "f1" , 'face': "B" , 'taken': False },
				'N2': { 'pos': "g1" , 'face': "N" , 'taken': False },
				'R2': { 'pos': "h1" , 'face': "R" , 'taken': False },
				'P1': { 'pos': "a2" , 'face': "P" , 'taken': False },
				'P2': { 'pos': "b2" , 'face': "P" , 'taken': False },
				'P3': { 'pos': "c2" , 'face': "P" , 'taken': False },
				'P4': { 'pos': "d2" , 'face': "P" , 'taken': False },
				'P5': { 'pos': "e2" , 'face': "P" , 'taken': False },
				'P6': { 'pos': "f2" , 'face': "P" , 'taken': False },
				'P7': { 'pos': "g2" , 'face': "P" , 'taken': False },
				'P8': { 'pos': "h2" , 'face': "P" , 'taken': False },
			},
			'boardDictDiff': {
				'r1': { 'pos': "a8" , 'face': "r" , 'taken': False },
				'n1': { 'pos': "b8" , 'face': "n" , 'taken': False },
				'b1': { 'pos': "c8" , 'face': "b" , 'taken': False },
				'q1': { 'pos': "d8" , 'face': "q" , 'taken': False },
				'k1': { 'pos': "e8" , 'face': "k" , 'taken': False },
				'b2': { 'pos': "f8" , 'face': "b" , 'taken': False },
				'n2': { 'pos': "g8" , 'face': "n" , 'taken': False },
				'r2': { 'pos': "h8" , 'face': "r" , 'taken': False },
				'p1': { 'pos': "a7" , 'face': "p" , 'taken': False },
				'p2': { 'pos': "b7" , 'face': "p" , 'taken': False },
				'p3': { 'pos': "c7" , 'face': "p" , 'taken': False },
				'p4': { 'pos': "d7" , 'face': "p" , 'taken': False },
				'p5': { 'pos': "e7" , 'face': "p" , 'taken': False },
				'p6': { 'pos': "f7" , 'face': "p" , 'taken': False },
				'p7': { 'pos': "g7" , 'face': "p" , 'taken': False },
				'p8': { 'pos': "h7" , 'face': "p" , 'taken': False },
				'R1': { 'pos': "a1" , 'face': "R" , 'taken': False },
				'N1': { 'pos': "b1" , 'face': "N" , 'taken': False },
				'B1': { 'pos': "c1" , 'face': "B" , 'taken': False },
				'Q1': { 'pos': "d1" , 'face': "Q" , 'taken': False },
				'K1': { 'pos': "e1" , 'face': "K" , 'taken': False },
				'B2': { 'pos': "f1" , 'face': "B" , 'taken': False },
				'N2': { 'pos': "g1" , 'face': "N" , 'taken': False },
				'R2': { 'pos': "h1" , 'face': "R" , 'taken': False },
				'P1': { 'pos': "a2" , 'face': "P" , 'taken': False },
				'P2': { 'pos': "b2" , 'face': "P" , 'taken': False },
				'P3': { 'pos': "c2" , 'face': "P" , 'taken': False },
				'P4': { 'pos': "d2" , 'face': "P" , 'taken': False },
				'P5': { 'pos': "e2" , 'face': "P" , 'taken': False },
				'P6': { 'pos': "f2" , 'face': "P" , 'taken': False },
				'P7': { 'pos': "g2" , 'face': "P" , 'taken': False },
				'P8': { 'pos': "h2" , 'face': "P" , 'taken': False },
			}
		 } )
		assert( result[0].steps[1] == {
			'board':"rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR",
			'boardDict': {
				'r1': { 'pos': "a8" , 'face': "r" , 'taken': False },
				'n1': { 'pos': "b8" , 'face': "n" , 'taken': False },
				'b1': { 'pos': "c8" , 'face': "b" , 'taken': False },
				'q1': { 'pos': "d8" , 'face': "q" , 'taken': False },
				'k1': { 'pos': "e8" , 'face': "k" , 'taken': False },
				'b2': { 'pos': "f8" , 'face': "b" , 'taken': False },
				'n2': { 'pos': "g8" , 'face': "n" , 'taken': False },
				'r2': { 'pos': "h8" , 'face': "r" , 'taken': False },
				'p1': { 'pos': "a7" , 'face': "p" , 'taken': False },
				'p2': { 'pos': "b7" , 'face': "p" , 'taken': False },
				'p3': { 'pos': "c7" , 'face': "p" , 'taken': False },
				'p4': { 'pos': "d7" , 'face': "p" , 'taken': False },
				'p5': { 'pos': "e7" , 'face': "p" , 'taken': False },
				'p6': { 'pos': "f7" , 'face': "p" , 'taken': False },
				'p7': { 'pos': "g7" , 'face': "p" , 'taken': False },
				'p8': { 'pos': "h7" , 'face': "p" , 'taken': False },
				'R1': { 'pos': "a1" , 'face': "R" , 'taken': False },
				'N1': { 'pos': "b1" , 'face': "N" , 'taken': False },
				'B1': { 'pos': "c1" , 'face': "B" , 'taken': False },
				'Q1': { 'pos': "d1" , 'face': "Q" , 'taken': False },
				'K1': { 'pos': "e1" , 'face': "K" , 'taken': False },
				'B2': { 'pos': "f1" , 'face': "B" , 'taken': False },
				'N2': { 'pos': "g1" , 'face': "N" , 'taken': False },
				'R2': { 'pos': "h1" , 'face': "R" , 'taken': False },
				'P1': { 'pos': "a2" , 'face': "P" , 'taken': False },
				'P2': { 'pos': "b2" , 'face': "P" , 'taken': False },
				'P3': { 'pos': "c2" , 'face': "P" , 'taken': False },
				'P4': { 'pos': "d2" , 'face': "P" , 'taken': False },
				'P5': { 'pos': "e4" , 'face': "P" , 'taken': False },
				'P6': { 'pos': "f2" , 'face': "P" , 'taken': False },
				'P7': { 'pos': "g2" , 'face': "P" , 'taken': False },
				'P8': { 'pos': "h2" , 'face': "P" , 'taken': False },
			},
			'boardDictDiff': {
				'P5': { 'pos': "e4" , 'face': "P" , 'taken': False },
			}

		 } )