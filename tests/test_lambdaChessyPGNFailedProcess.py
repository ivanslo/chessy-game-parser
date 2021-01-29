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

class TestLambdaChessyPGNFailedProcess:
    def setup_class(self):
        pass
    
    def test_callDynamoDB(self, mocker):
        dynamoMock = mocker.Mock()
        tableMock = mocker.Mock()
        mocker.patch.object(L, 'dynamodb',dynamoMock)
        dynamoMock.Table.return_value = tableMock

        event = { 'Records': [{'body': 'bucket:chess-private-content\nfilename:Carlsen.pgn\nfrom:0\nto:15'}] }

        L.lambda_handler(event, None)
    
        dynamoMock.Table.assert_called_once_with('pgn_files_failed')
        tableMock.put_item.assert_called_once()

    def test_callsDynamoDBCorrectly(self, mocker):
        dynamoMock = mocker.Mock()
        tableMock = mocker.Mock()
        mocker.patch.object(L, 'dynamodb',dynamoMock)
        dynamoMock.Table.return_value = tableMock
        # mock datetime

        event = { 'Records': [{'body': 'bucket:chess-private-content\nfilename:Carlsen.pgn\nfrom:0\nto:15'}] }

        L.lambda_handler(event, None)
    
        dynamoMock.Table.assert_called_once_with('pgn_files_failed')
        tableMock.put_item.assert_called_once()




		