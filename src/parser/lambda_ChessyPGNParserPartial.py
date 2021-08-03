# Lambda Function: ChessyPGNParserPartial

import json
import logging
import urllib.parse
import boto3
import os
import signal
from datetime import datetime
import re

import GameController

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

# logger set to the environment variable level
logger = logging.getLogger()
level = os.environ['LOG_LEVEL']
logger.setLevel(int(level))

table_chess_games_failed = os.environ['TABLE_CHESS_GAMES_FAILED']
table_pgn_files_succeeded =os.environ['TABLE_PGN_FILES_SUCCEEDED']
table_pgn_files_failed= os.environ['TABLE_PGN_FILES_FAILED']
table_chess_games = os.environ['TABLE_CHESS_GAMES']



toProcess_FileKey = ""
toProcess_Bucket = ""
toProcess_LineFrom = -1
toProcess_LineTo = -1


def lambda_handler(event, context):
    global toProcess_Bucket, toProcess_FileKey, toProcess_LineFrom, toProcess_LineTo

    # Setup alarm for when I'm close (1 second) to timeout
    signal.alarm(int(context.get_remaining_time_in_millis() / 1000) - 1)
    
    # Get the object from the event and show its content type
    sqsBody = event['Records'][0]['body']

    match = re.match(r'bucket:(.+)\nfilename:(.+)\nfrom:(\d+)\nto:(\d+)', sqsBody)

    if match == None:
        raise Exception("Malformed SQS Message received: {} ".format(sqsBody))

    (b,fk,f,t) = match.groups()
    logger.debug('Handling bucket/key/from/to: {}/{}/{}/{}'.format(b,fk,f,t))

    toProcess_Bucket = b
    toProcess_FileKey = fk
    toProcess_LineFrom = int(f)
    toProcess_LineTo = int(t)

    
    response = {}
    body = ""
    parsedGames = []

    try:
        response = s3.get_object(Bucket=toProcess_Bucket, Key=toProcess_FileKey)
        body = response['Body'].read().decode('utf-8').replace('\r\n','\n')
    except Exception as e:
        logger.error('Exception getting oject from S3: {}'.format(e))
        save_failed_gamefile("reading")
        raise e

    bodyLines = body.split('\n')
    partialBody = '\n'.join(bodyLines[toProcess_LineFrom:toProcess_LineTo])


    try:
        parsedGames = GameController.processPGNText(partialBody)
    except Exception as e:
        logger.error('Exception Parsing: {}'.format(e))
        save_failed_gamefile("parsing")
        raise e
    
    duplicatedKeysErrors = []
    try:
        table = dynamodb.Table(table_chess_games)
        with table.batch_writer() as batch:
            batchedIds= set([])
            for game in parsedGames:
                item_db = {}
                # avoid batching multiple items w same key
                if game.id in batchedIds:
                    duplicatedKeysErrors.append(game.id)
                    continue
                batchedIds.add(game.id)

                item_db['id'] = str(game.id)
                for k in game.info.keys():
                    item_db[k] = str(game.info[k])
                item_db['jsonFile'] = game.toDict()
                item_db['addedDate'] = getDatetime()
                batch.put_item(Item=item_db)
    except Exception as e:
        logger.error('Exception Writing to DB: {}'.format(e))
        save_failed_gamefile("writing")
        raise e
    
    if len(duplicatedKeysErrors) > 0:
        for duplicatedKey in duplicatedKeysErrors:
            save_failed_game('Duplicated Key: {}'.format(duplicatedKey))

    # disconnect signal alarm
    signal.alarm(0)
    save_succeeded_game( len(parsedGames) - len(duplicatedKeysErrors) )
    logger.info('Partial PGN handled and written successfully')

def getDatetime()-> str :
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getProcessingId() -> str:
    return '{}_{}_{}_{}'.format(toProcess_Bucket, toProcess_FileKey, toProcess_LineFrom, toProcess_LineTo)

def save_failed_game(reason: str):
    signal.alarm(0)
    table = dynamodb.Table(table_chess_games_failed)
    when = getDatetime()
    table.put_item(Item={
        'id': getProcessingId(),
        'bucket': toProcess_Bucket,
        'filename': toProcess_FileKey,
        'lineFrom': toProcess_LineFrom,
        'lineTo':toProcess_LineTo,
        'reason': reason,
        'datetime': when
        })

def save_failed_gamefile(reason: str):
    signal.alarm(0)
    table = dynamodb.Table(table_pgn_files_failed)
    when = getDatetime()
    table.put_item(Item={
        'id': getProcessingId(),
        'bucket': toProcess_Bucket,
        'filename': toProcess_FileKey,
        'lineFrom': toProcess_LineFrom,
        'lineTo':toProcess_LineTo,
        'reason': reason,
        'datetime': when
        })

def save_succeeded_game(gamesQuantity: int):
    signal.alarm(0)
    table = dynamodb.Table(table_pgn_files_succeeded)
    when = getDatetime()
    table.put_item(Item={
        'id': getProcessingId(),
        'bucket': toProcess_Bucket,
        'filename': toProcess_FileKey,
        'lineFrom': toProcess_LineFrom,
        'lineTo':toProcess_LineTo,
        'gamesQuantity': gamesQuantity,
        'datetime': when
        })
    
def timeout_handler(_signal, _frame):
    global toProcess_FileKey
    '''Handle SIGALARM'''
    save_failed_gamefile('not enough time')
    raise Exception('Not enough Time')

signal.signal(signal.SIGALRM, timeout_handler)
