'''
The next lines are there to deal with python files importing each other inside `src`
alternatively, I need to set `PYTHONPATH=../src` before running pytest
'''
import os.path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/splitter")))

from pytest_mock import mocker
from unittest.mock import patch
import pytest



# Test Data
_bucket='aBucket'
_filename='aFilename'
_from='0'
_to='20'
_time='01-01-01 10:00:02'
lambdaEvent = { 'Records': [ {'s3': {
        'bucket':{'name': _bucket},
        'object':{'key' : _filename}
        }}]}
_sqs_url = 'http://fake-sqs-url/'


with patch.dict(os.environ, {'LOG_LEVEL': '3', 'SQS_URL': _sqs_url}):
    import lambda_ChessyPGNSplitter as L




def getMocks(mocker):
    mockS3 = mocker.Mock()
    mockSQS = mocker.Mock()
    mockPGNFile = mocker.Mock()
    mockContext = mocker.Mock()

    mockS3.get_object.return_value = { 'Body': mocker.Mock() }
    mockContext.get_remaining_time_in_millis.return_value = 10000

    return (mockS3, mockSQS, mockContext, mockPGNFile)


class TestLambdaChessyPGNSplitter:
    def setup_class(self):
        pass
    
    def test_cannotReadS3Object(self, mocker):
        (mockS3, mockSQS, mockContext, _) = getMocks(mocker)
        mocker.patch.object(L, 's3', mockS3)

        mockS3.get_object.side_effect = mocker.Mock(side_effect=Exception('impossible to read'))
        with pytest.raises(Exception) as e_info:
            L.lambda_handler(lambdaEvent, mockContext)

    def test_canReadS3ObjectAndSendSQSMessage(self, mocker):
        (mockS3, mockSQS, mockContext, mockPGNFile) = getMocks(mocker)
        mocker.patch.object(L, 's3', mockS3)
        mocker.patch.object(L, 'sqs', mockSQS)
        mocker.patch.object(L, 'PGNFile', mockPGNFile )

        # chunks #1
        mockPGNFile.groupBoundaries.return_value = [(0,10),(11,25)]

        L.lambda_handler(lambdaEvent, mockContext)

        mockSQS.send_message_batch.assert_called_once_with(Entries=[
            { 'Id':'id_0', 'MessageBody': 'bucket:aBucket\nfilename:aFilename\nfrom:0\nto:10'},
            { 'Id':'id_1', 'MessageBody': 'bucket:aBucket\nfilename:aFilename\nfrom:11\nto:25'}
            ],
            QueueUrl=_sqs_url)

        mockSQS.reset_mock()
        
        # chunks #2
        mockPGNFile.groupBoundaries.return_value = [(0,1),(2,3),(4,5),(10000,20000)]

        L.lambda_handler(lambdaEvent, mockContext)

        mockSQS.send_message_batch.assert_called_once_with(Entries=[
            { 'Id':'id_0', 'MessageBody': 'bucket:aBucket\nfilename:aFilename\nfrom:0\nto:1'},
            { 'Id':'id_1', 'MessageBody': 'bucket:aBucket\nfilename:aFilename\nfrom:2\nto:3'},
            { 'Id':'id_2', 'MessageBody': 'bucket:aBucket\nfilename:aFilename\nfrom:4\nto:5'},
            { 'Id':'id_3', 'MessageBody': 'bucket:aBucket\nfilename:aFilename\nfrom:10000\nto:20000'}
            ],
            QueueUrl=_sqs_url)

