import json
import logging
import urllib.parse
import boto3
import os

import  GameController


'''
Simulates what the lambda function will do: open the file from S3 and call our internals.
Its purpose is to troubleshoot file opening, decoding, etc
'''

def main():
    s3 = boto3.client('s3', aws_access_key_id='<NONE>', aws_secret_access_key='<NONE>')
    # Get the object from the event and show its content type
    bucket = 'chess-private-content'
    # key = 'Capablanca.pgn'
    key = 'WorldChamp2016.pgn'

    response = s3.get_object(Bucket=bucket, Key=key)
    body = response['Body'].read().decode('utf-8').replace('\r\n','\n')

    parsedGames = GameController.processPGNText(body)

    print(len(parsedGames))

main()