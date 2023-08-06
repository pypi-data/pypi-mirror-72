import base64
import logging
import os
from simplejson import loads


def process_sns_event(func):
    def wrapper(event, _context):
        logging.debug('Received event : {}'.format(event))
        for record in event['Records']:
            event = loads(record['Sns']['Message'])
            func(event)

    return wrapper


def process_kinesis_event(func):
    def wrapper(event, _context):
        logging.debug('Received event : {}'.format(event))

        for record in event['Records']:
            event = loads(base64.b64decode(record['kinesis']['data']).decode('UTF-8'))
            try:
                func(event)
            except Exception as e:
                logging.getLogger().error("An unknown error occurred when trying to process kinesis event")
                logging.getLogger().exception(e)
                if os.environ.get('SILENT_FAILURE', 'false').lower() != 'true':
                    raise e

    return wrapper


def process_sqs_event(func):
    def wrapper(event, _context):
        for record in event['Records']:
            command = loads(record['body'])
            func(command)

    return wrapper
