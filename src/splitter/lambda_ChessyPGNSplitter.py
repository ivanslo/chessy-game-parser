# Lambda Function: ChessyPGNSplitter

import json
import logging
import urllib.parse
import boto3
import os
import signal
from datetime import datetime

import sys
import PGNFile

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')

# logger set to the environment variable level
logger = logging.getLogger()
level = os.environ['LOG_LEVEL']
sqsUrl = os.environ['SQS_URL']
logger.setLevel(int(level))

processingFile = ""
processingBucket = ""

def lambda_handler(event, context):
    global processingFile
    global processingBucket
    # Setup alarm for when I'm close (1 second) to timeout
    signal.alarm(int(context.get_remaining_time_in_millis() / 1000) - 1)
    
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    logger.debug('Handling bucket/key: {}/{}.'.format(bucket, key))

    processingBucket = bucket
    processingFile = key
    
    response = {}
    fileBody = ""

    ## Reading
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        fileBody = response['Body'].read().decode('utf-8').split('\n')
    except Exception as e:
        logger.error('Exception getting oject from S3: {}'.format(e))
        raise e


    ## Processing
    gameDelimiters = PGNFile.getGameBoundaryLines(fileBody)
    chunks = PGNFile.groupBoundaries(gameDelimiters, 100)

    ## Sending
    try: 
        sendToSQS(chunks)
    except Exception as e:
        logger.error('Exception publishing to SQS: {}'.format(e))
    
    return {
        'statusCode': 200,
        'body': 'all good'
    }
    signal.alarm(0)
    
'''
send the `chunks` to SQS as messages
'''
def sendToSQS(chunks):
    global processingFile
    global processingBucket

    def makeMessageFor(b: str, fn: str, f: int, t: int, n: int) :
        return {
            'Id': 'id_{0}'.format(n),
            'MessageBody': 'bucket:{0}\nfilename:{1}\nfrom:{2}\nto:{3}'.format(b, fn,f,t)
        }

    messages = []
    for i, (f,t) in enumerate(chunks):
        messages.append(makeMessageFor(processingBucket, processingFile, f, t, i))
    
    maxMessages = 10 # 10 per batch
    i = 0
    while i < len(messages):
        j = i + maxMessages
        sqs.send_message_batch(Entries=messages[i:j], QueueUrl=sqsUrl)
        i = j


def timeout_handler(_signal, _frame):
    global processingFile
    '''Handle SIGALARM'''
    raise Exception('Not enough Time')

signal.signal(signal.SIGALRM, timeout_handler)
