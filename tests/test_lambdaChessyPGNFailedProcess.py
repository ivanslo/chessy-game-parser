'''
The next lines are there to deal with python files importing each other inside `src`
alternatively, I need to set `PYTHONPATH=../src` before running pytest
'''
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/failer")))

from pytest_mock import mocker
from unittest.mock import patch
import pytest

with patch.dict(os.environ, {'LOG_LEVEL': '3'}):
    import lambda_ChessyPGNFailedProcess as L

_bucket='aBucket'
_filename='aFilename'
_from='0'
_to='20'
_time='01-01-01 10:00:02'

lambdaEvent = { 'Records': [{'body': 'bucket:{}\nfilename:{}\nfrom:{}\nto:{}'.format(_bucket,_filename,_from,_to)}] }
lambdaEvent_bad = { 'Records': [{'body': 'bad_sqs_message'}] }

class TestLambdaChessyPGNFailedProcess:
    def setup_class(self):
        pass
    
    def test_callDynamoDB(self, mocker):
        dynamoMock = mocker.Mock()
        tableMock = mocker.Mock()
        mocker.patch.object(L, 'dynamodb',dynamoMock)
        dynamoMock.Table.return_value = tableMock

        L.lambda_handler(lambdaEvent, None)

        dynamoMock.Table.assert_called_once_with('pgn_files_failed')
        tableMock.put_item.assert_called_once()

    def test_callsDynamoDBCorrectly(self, mocker):
        dynamoMock = mocker.Mock()
        tableMock = mocker.Mock()
        timeMock = mocker.Mock()
        mocker.patch.object(L, 'dynamodb',dynamoMock)
        mocker.patch.object(L, 'getDatetime',timeMock)
        dynamoMock.Table.return_value = tableMock
        timeMock.return_value = _time 

        L.lambda_handler(lambdaEvent, None)

        dynamoMock.Table.assert_called_once_with('pgn_files_failed')
        tableMock.put_item.assert_called_once()

        tableMock.put_item.assert_called_with(Item={
            'id': '{}_{}_{}_{}_DLQ'.format(_bucket, _filename, _from, _to),
            'bucket': _bucket,
            'filename': _filename,
            'lineFrom': _from,
            'lineTo': _to,
            'reason': "Was in DLQ",
            'datetime': _time
        })

    def test_callsDynamoDBWithoutParsing(self, mocker):
        dynamoMock = mocker.Mock()
        tableMock = mocker.Mock()
        timeMock = mocker.Mock()
        mocker.patch.object(L, 'dynamodb',dynamoMock)
        mocker.patch.object(L, 'getDatetime',timeMock)
        dynamoMock.Table.return_value = tableMock
        timeMock.return_value = _time 

        L.lambda_handler(lambdaEvent_bad, None)

        dynamoMock.Table.assert_called_once_with('pgn_files_failed')

        ## FAIL TO PARSE MESSAGE VALUES
        _bucket = '_bucket_'
        _filename = '_filename_'
        _from = '_from_'
        _to = '_to_'

        tableMock.put_item.assert_called_with(Item={
            'id': '{}_{}_{}_{}_DLQ'.format(_bucket, _filename, _from, _to),
            'bucket': _bucket,
            'filename': _filename,
            'lineFrom': _from,
            'lineTo': _to,
            'reason': "Was in DLQ",
            'datetime': _time
        })
