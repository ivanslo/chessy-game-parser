'''
The next lines are there to deal with python files importing each other inside `src`
alternatively, I need to set `PYTHONPATH=../src` before running pytest
'''
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

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

	def test_processPGNText_1(self):
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