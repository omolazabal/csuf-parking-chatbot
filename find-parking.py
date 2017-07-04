import math
import os
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def dispatch(intent_request):
    # Deals with the intent the user specifies

def lambda_handler(event, context):
    '''Main handler
    event is used to pass in event data.
    context is used to provide runtime information.
    '''

    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)