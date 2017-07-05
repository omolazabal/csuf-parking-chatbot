import math
import os
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def dispatch(intent_request):
    '''Deals with the intent the user specifies
    '''

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'],
                                                            intent_request['currentIntent']['name']))
    intent_name = intent_request['currentIntent']['name']

    if intent_name == 'OptimalParking':
        return optimal_parking(intent_request)
    elif intent_name == 'SpecificParking':
        return SpecificParking(intent_request)
    elif intent_name == 'ListParkingLots':
        return ListParkingLots(intent_request)
    elif intent_name == 'GetDirections':
        return GetDirections(intent_request)
    else:
        raise Exception('Intent with name {} not supported'.format(intent_name))
    


def lambda_handler(event, context):
    '''Main handler
    Event is used to pass in event data. Seems to be stored as nested dictionaries.
    Context is used to provide runtime information.
    '''

    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)