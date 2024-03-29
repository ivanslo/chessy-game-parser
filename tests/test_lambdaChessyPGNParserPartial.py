'''
The next lines are there to deal with python files importing each other inside `src`
alternatively, I need to set `PYTHONPATH=../src` before running pytest
'''
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/parser")))

from pytest_mock import mocker
from unittest.mock import patch
import pytest



# Test Data
_bucket='aBucket'
_filename='aFilename'
_from='0'
_to='20'
_time='01-01-01 10:00:02'
_msgBody = 'bucket:{0}\nfilename:{1}\nfrom:{2}\nto:{3}'.format(_bucket,_filename,_from,_to)
class ParsedGame:
    def __init__(self, id):
        self.id = id
    info = {
        'key1': 'value1',
        'key2': 'value2'
    }
    def toJSON(self):
        return "jsonified"

    def toDict(self):
        return {"dictified":""}


lambdaEvent = { 'Records': [ {'body': _msgBody }]}


def mockFailedDbItem(reason: str) -> dict :
    _dbItem = {
            'id': '{}_{}_{}_{}'.format(_bucket, _filename, _from, _to),
            'bucket': _bucket,
            'filename': _filename,
            'lineFrom': int(_from),
            'lineTo': int(_to),
            'reason': reason,
            'datetime': _time
            }
    return _dbItem

def mockAddedDbItem(gamesQuantity: int) -> dict :
    _dbItem = {
            'id': '{}_{}_{}_{}'.format(_bucket, _filename, _from, _to),
            'bucket': _bucket,
            'datetime': _time,
            'filename': _filename,
            'lineFrom': int(_from),
            'lineTo': int(_to),
            'gamesQuantity': gamesQuantity
            }
    return _dbItem

def mockSuccessDbItem(pg: ParsedGame) -> dict :
    _dbItem = {
            'id': str(pg.id),
            'addedDate': _time,
            'jsonFile': pg.toDict()
            }
    for k in pg.info:
        _dbItem[k] = pg.info[k]
    return _dbItem

mock_tableChessGamesFailed = 'games_failed'
mock_tablePgnFailed = 'pgn_failed'
mock_tablePgnSucceeded = 'pgn_succeeded'
mock_tableChessGames = 'chess_games'


with patch.dict(os.environ, {'LOG_LEVEL': '3', 
    'TABLE_CHESS_GAMES_FAILED':mock_tableChessGamesFailed,
    'TABLE_PGN_FILES_SUCCEEDED':mock_tablePgnSucceeded,
    'TABLE_PGN_FILES_FAILED': mock_tablePgnFailed,
    'TABLE_CHESS_GAMES':mock_tableChessGames
    }):
    import lambda_ChessyPGNParserPartial as L




def getMocks(mocker):
    mockS3 = mocker.Mock()
    mockSQS = mocker.Mock()
    mockDynamo = mocker.Mock()
    mockGameController = mocker.Mock()
    mockContext = mocker.Mock()
    mockTable = mocker.Mock()

    mockTime = mocker.Mock()
    mockTime.return_value = _time

    mockBody = mocker.Mock()
    mockBody.read.return_value.decode.return_value.replace.return_value.split.return_value = []

    mockS3.get_object.return_value = { 'Body': mockBody }
    mockContext.get_remaining_time_in_millis.return_value = 10000
    mockDynamo.Table.return_value = mockTable

    return (mockS3, mockSQS, mockDynamo, mockContext, mockGameController, mockTime)


class TestLambdaChessyPGNParserPartial:
    def setup_class(self):
        pass
    
    def test_cannotReadS3Object(self, mocker):
        (mockS3, mockSQS, mockDynamo, mockContext, _, mockTime) = getMocks(mocker)
        mocker.patch.object(L, 's3', mockS3)
        mocker.patch.object(L, 'dynamodb', mockDynamo)
        mocker.patch.object(L, 'getDatetime', mockTime)

        mockS3.get_object.side_effect = mocker.Mock(side_effect=Exception('impossible to read'))

        with pytest.raises(Exception) as e_info:
            L.lambda_handler(lambdaEvent, mockContext)
    
        item = mockFailedDbItem('reading')
        mockDynamo.Table.assert_called_once_with(mock_tablePgnFailed)
        mockDynamo.Table.return_value.put_item.assert_called_once()
        mockDynamo.Table.return_value.put_item.assert_called_once_with(Item=item)

    def test_processGame_andFail(self, mocker):
        (mockS3, mockSQS, mockDynamo, mockContext, mockGameController, mockTime) = getMocks(mocker)
        mocker.patch.object(L, 's3', mockS3)
        mocker.patch.object(L, 'dynamodb', mockDynamo)
        mocker.patch.object(L, 'GameController',mockGameController)
        mocker.patch.object(L, 'getDatetime', mockTime)

        mockGameController.processPGNText.side_effect = mocker.Mock(side_effect=Exception('parsing fail'))

        with pytest.raises(Exception) as e_info:
            L.lambda_handler(lambdaEvent, mockContext)

        mockGameController.processPGNText.assert_called_once()
        item = mockFailedDbItem('parsing')
        mockDynamo.Table.assert_called_once_with(mock_tablePgnFailed)
        mockDynamo.Table.return_value.put_item.assert_called_once()
        mockDynamo.Table.return_value.put_item.assert_called_once_with(Item=item)

    def test_processGame_writes_andFail(self, mocker):
        (mockS3, mockSQS, mockDynamo, mockContext, mockGameController, mockTime) = getMocks(mocker)
        mocker.patch.object(L, 's3', mockS3)
        mocker.patch.object(L, 'dynamodb', mockDynamo)
        mocker.patch.object(L, 'GameController',mockGameController)
        mocker.patch.object(L, 'getDatetime', mockTime)

        mockBatch = mocker.Mock()
        mockTable = mocker.MagicMock()
        mockDynamo.Table.return_value = mockTable
        mockTable.batch_writer.return_value.__enter__.return_value = mockBatch
        mockBatch.put_item.side_effect = mocker.Mock(side_effect=Exception('put item failed'))

        pg = ParsedGame(1)
        mockGameController.processPGNText.return_value = [pg]

        with pytest.raises(Exception) as e_info:
            L.lambda_handler(lambdaEvent, mockContext)

        item = mockSuccessDbItem(pg)
        mockBatch.put_item.assert_called_once()
        mockBatch.put_item.assert_called_once_with(Item=item)
        assert( mockDynamo.Table.call_count == 2 )

        mockDynamo.Table.assert_any_call('chess_games')
        mockDynamo.Table.assert_any_call(mock_tablePgnFailed)

        failedItem = mockFailedDbItem('writing')
        mockTable.put_item.assert_called_once()
        mockTable.put_item.assert_called_once_with(Item=failedItem)

    def test_processGame_writes_1(self, mocker):
        (mockS3, mockSQS, mockDynamo, mockContext, mockGameController, mockTime) = getMocks(mocker)
        mocker.patch.object(L, 's3', mockS3)
        mocker.patch.object(L, 'dynamodb', mockDynamo)
        mocker.patch.object(L, 'GameController',mockGameController)
        mocker.patch.object(L, 'getDatetime', mockTime)
        mockBatch = mocker.Mock()
        mockTable = mocker.MagicMock()
        mockTable.batch_writer.return_value.__enter__.return_value = mockBatch
        mockDynamo.Table.return_value = mockTable

        pg = ParsedGame(1)
        mockGameController.processPGNText.return_value = [pg]

        L.lambda_handler(lambdaEvent, mockContext)

        mockBatch.put_item.assert_called_once()
        mockBatch.put_item.assert_called_once_with(Item=mockSuccessDbItem(pg))

        assert( mockDynamo.Table.call_count == 2 )
        mockDynamo.Table.assert_any_call('chess_games')
        mockDynamo.Table.assert_any_call(mock_tablePgnSucceeded)

        mockTable.put_item.assert_called_once()
        mockTable.put_item.assert_called_once_with(Item=mockAddedDbItem(1))

    def test_processGame_writes_2(self, mocker):
        (mockS3, mockSQS, mockDynamo, mockContext, mockGameController, mockTime) = getMocks(mocker)
        mocker.patch.object(L, 's3', mockS3)
        mocker.patch.object(L, 'dynamodb', mockDynamo)
        mocker.patch.object(L, 'GameController',mockGameController)
        mocker.patch.object(L, 'getDatetime', mockTime)
        mockBatch = mocker.Mock()
        mockTable = mocker.MagicMock()
        mockTable.batch_writer.return_value.__enter__.return_value = mockBatch
        mockDynamo.Table.return_value = mockTable

        pg1 = ParsedGame(1)
        pg2 = ParsedGame(2)
        mockGameController.processPGNText.return_value = [pg1, pg2]

        L.lambda_handler(lambdaEvent, mockContext)

        assert( mockBatch.put_item.call_count == 2 )
        mockBatch.put_item.assert_any_call(Item=mockSuccessDbItem(pg1))
        mockBatch.put_item.assert_any_call(Item=mockSuccessDbItem(pg2))

        mockDynamo.Table.assert_any_call('chess_games')
        mockDynamo.Table.assert_any_call(mock_tablePgnSucceeded)

        mockTable.put_item.assert_called_once()
        mockTable.put_item.assert_called_once_with(Item=mockAddedDbItem(2))

    def test_processGame_writes_duplicated_id(self, mocker):
        (mockS3, mockSQS, mockDynamo, mockContext, mockGameController, mockTime) = getMocks(mocker)
        mocker.patch.object(L, 's3', mockS3)
        mocker.patch.object(L, 'dynamodb', mockDynamo)
        mocker.patch.object(L, 'GameController',mockGameController)
        mocker.patch.object(L, 'getDatetime', mockTime)
        mockBatch = mocker.Mock()
        mockTable = mocker.MagicMock()
        mockTable.batch_writer.return_value.__enter__.return_value = mockBatch
        mockDynamo.Table.return_value = mockTable

        pg1 = ParsedGame(1)
        pg2 = ParsedGame(1)
        mockGameController.processPGNText.return_value = [pg1, pg2]

        L.lambda_handler(lambdaEvent, mockContext)

        mockDynamo.Table.assert_any_call('chess_games')
        mockDynamo.Table.assert_any_call(mock_tablePgnSucceeded)
        mockDynamo.Table.assert_any_call(mock_tableChessGamesFailed)

        # good game
        assert( mockBatch.put_item.call_count == 1 )
        mockBatch.put_item.assert_any_call(Item=mockSuccessDbItem(pg1))
        # file things
        assert( mockTable.put_item.call_count == 2 )
        mockTable.put_item.assert_any_call(Item=mockAddedDbItem(1))
        mockTable.put_item.assert_any_call(Item=mockFailedDbItem('Duplicated Key: 1'))

    def test_processGame_writes_duplicated_id_2(self, mocker):
        (mockS3, mockSQS, mockDynamo, mockContext, mockGameController, mockTime) = getMocks(mocker)
        mocker.patch.object(L, 's3', mockS3)
        mocker.patch.object(L, 'dynamodb', mockDynamo)
        mocker.patch.object(L, 'GameController',mockGameController)
        mocker.patch.object(L, 'getDatetime', mockTime)
        mockBatch = mocker.Mock()
        mockTable = mocker.MagicMock()
        mockTable.batch_writer.return_value.__enter__.return_value = mockBatch
        mockDynamo.Table.return_value = mockTable

        pg1 = ParsedGame(1)
        pg2 = ParsedGame(2)
        pg3 = ParsedGame(3)
        pg4 = ParsedGame(3) # duplicated
        mockGameController.processPGNText.return_value = [pg1, pg2, pg3, pg4]

        L.lambda_handler(lambdaEvent, mockContext)

        mockDynamo.Table.assert_any_call('chess_games')
        mockDynamo.Table.assert_any_call(mock_tablePgnSucceeded)
        mockDynamo.Table.assert_any_call(mock_tableChessGamesFailed)

        # good game
        assert( mockBatch.put_item.call_count == 3 )
        mockBatch.put_item.assert_any_call(Item=mockSuccessDbItem(pg1))
        mockBatch.put_item.assert_any_call(Item=mockSuccessDbItem(pg2))
        mockBatch.put_item.assert_any_call(Item=mockSuccessDbItem(pg3))

        assert( mockTable.put_item.call_count == 2 )
        # file things
        mockTable.put_item.assert_any_call(Item=mockAddedDbItem(3))
        # duplicated key
        mockTable.put_item.assert_any_call(Item=mockFailedDbItem('Duplicated Key: 3'))

