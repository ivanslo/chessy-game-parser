# Lambda Function: ChessyPGNFailedProcess

import logging
import boto3
import os
import re
from datetime import datetime

import sys

dynamodb = boto3.resource('dynamodb')

# logger set to the environment variable level
logger = logging.getLogger()
level = os.environ['LOG_LEVEL']
logger.setLevel(int(level))


def lambda_handler(event, context):
    # Get the object from the event
    sqsBody = event['Records'][0]['body']
    match = re.match(r'bucket:(.+)\nfilename:(.+)\nfrom:(\d+)\nto:(\d+)', sqsBody)

    b  = "_bucket_"
    fk = "_filename_"
    f  = "_from_"
    t  = "_to_"
    if match == None:
        # does-not throw
        logger.error("Malformed SQS Message received: {} ".format(sqsBody))
    else:
        (b,fk,f,t) = match.groups()
        logger.debug('Handling bucket/key/from/to: {}/{}/{}/{}'.format(b,fk,f,t))

    table = dynamodb.Table('pgn_files_failed')
    table.put_item(Item={
        'id': '{}_{}_{}_{}_DLQ'.format(b, fk, f, t),
        'bucket': b,
        'filename': fk,
        'lineFrom': f,
        'lineTo': t,
        'reason': "Was in DLQ",
        'datetime': getDatetime()
        })
    
    return {
        'statusCode': 200,
        'body': 'stored'
    }
    
def getDatetime()-> str :
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
