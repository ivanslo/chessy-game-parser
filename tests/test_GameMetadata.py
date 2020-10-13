'''
The next lines are there to deal with python files importing each other inside `src`
alternatively, I need to set `PYTHONPATH=../src` before running pytest
'''
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


import GameMetadata
import pytest


class TestGameMetadata:
    gameMeta = None

    def setup_class(self):
        self.gameMeta= GameMetadata.GameMetadata()

    def test_metadataIsParsed(self):
        
        # Correct format doesn't raise Exceptions
        self.gameMeta.add('[Event "Event1"]')

        # these should all raise Exceptions
        with pytest.raises(Exception) as e:
            self.gameMeta.add('WEKJW')
        with pytest.raises(Exception) as e:
            self.gameMeta.add('[Event ]')
        with pytest.raises(Exception) as e:
            self.gameMeta.add('(Event )')
        with pytest.raises(Exception) as e:
            self.gameMeta.add('(Event )')

    def test_idIsMadeOutOfMandatoryFields(self):
        strings = [ '[Event "Event1"]', '[Site "Site1"]', '[Whatever "yes"]']
        
        self.gameMeta.add(strings[0])
        self.gameMeta.add(strings[1])
        self.gameMeta.add(strings[2])

        gameId = self.gameMeta.getId()

        assert(gameId.find('Event1') >= 0)
        assert(gameId.find('Site1') >= 0)
        assert(gameId.find('yes') == -1)
    
    def test_idRemovesUnwantedChars(self):
        strings = [ '[Event "Event-1"]', '[Site "many spaces     here"]']
        
        self.gameMeta.add(strings[0])
        self.gameMeta.add(strings[1])

        gameId = self.gameMeta.getId()

        assert(gameId == "Event1_manyspaceshere")

