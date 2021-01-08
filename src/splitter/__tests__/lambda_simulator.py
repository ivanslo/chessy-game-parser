import json
import logging
import urllib.parse
import boto3
import os

import sys
import os.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import PGNFile


'''
Simulates what the lambda function will see.
'''

def main():
    s3 = boto3.client('s3', aws_access_key_id='NONE', aws_secret_access_key='NONE')
    bucket = 'chess-private-content'
    key = 'Carlsen.pgn'

    response = s3.get_object(Bucket=bucket, Key=key)
    fileBody = response['Body'].read().decode('utf-8').split('\n')
    
    gameDelimiters = PGNFile.getGameBoundaryLines(fileBody)
    chunks = PGNFile.groupBoundaries(gameDelimiters, 100)

    print(len(gameDelimiters))
    print(gameDelimiters[-10:])
    print(len(chunks))

main()