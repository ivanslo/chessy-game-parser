import json
import logging
import urllib.parse
import boto3
import os
import signal
from datetime import datetime

import  GameController

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# logger set to the environment variable level
logger = logging.getLogger()
level = os.environ['LOG_LEVEL']
logger.setLevel(int(level))

processingFile = ""

def lambda_handler(event, context):
    global processingFile
    # Setup alarm for when I'm close (1 second) to timeout
    signal.alarm(int(context.get_remaining_time_in_millis() / 1000) - 1)
    
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    logger.debug('Handling bucket/key: {}/{}.'.format(bucket, key))

    processingFile = key
    response = {}
    body = ""
    parsedGames = []

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        body = response['Body'].read().decode('utf-8').replace('\r\n','\n')
    except Exception as e:
        logger.error('Exception getting oject from S3: {}'.format(e))
        save_failed_game(key, "reading")
        raise e

    try:
        parsedGames = GameController.processPGNText(body)
    except Exception as e:
        logger.error('Exception Parsing: {}'.format(e))
        save_failed_game(key, "parsing")
        raise e
    
    try:
        table = dynamodb.Table('chess_games')
        with table.batch_writer() as batch:
            for game in parsedGames:
                item_db = {}
                item_db['id'] = str(game.id)
                for k in game.info.keys():
                    item_db[k] = str(game.info[k])
                item_db['jsonFile'] = game.toJSON()
                batch.put_item(Item=item_db)

    except Exception as e:
        logger.error('Exception Writing to DB: {}'.format(e))
        save_failed_game(key, "writing")
        raise e
    
    # disconnect signal alarm
    signal.alarm(0)
    save_succeeded_game(key)
    logger.info('PGN handled and written successfully')

def save_failed_game(filename: str, reason: str):
    signal.alarm(0)
    table = dynamodb.Table('chess_games_failed')
    when = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table.put_item(Item={'filename': filename, 'reason': reason, 'datetime': when})

def save_succeeded_game(filename: str):
    signal.alarm(0)
    table = dynamodb.Table('chess_games_succeeded')
    when = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    table.put_item(Item={'filename': filename, 'datetime': when})
    
def timeout_handler(_signal, _frame):
    global processingFile
    '''Handle SIGALARM'''
    save_failed_game(processingFile, 'not enough time')
    raise Exception('Not enough Time')

signal.signal(signal.SIGALRM, timeout_handler)