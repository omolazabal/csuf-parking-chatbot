
"""Contains the handler and dispatch functions. Routes incoming
request based on the intent and dispatches bot's intent handlers
"""

import logging
import fulfillment

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def dispatch(intent_request):
    """Deals with the intent the user specifies"""

    logger.debug('dispatch userId={}, intentName={}'
                 .format(intent_request['userId'],
                         intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    if intent_name == 'OptimalParking':
        return fulfillment.optimal_parking(intent_request)

    if intent_name == 'ListParkingLots':
        return fulfillment.list_parking(intent_request)

    if intent_name == 'SpecificParking':
        return fulfillment.specific_parking(intent_request)

    if intent_name == 'GetDirections':
        return fulfillment.get_directions(intent_request)

    raise Exception('Intent with name {} not supported'.format(intent_name))


def lambda_handler(event, context):
    """Main handler
    Event is used to pass in event data. Seems to be stored as nested.
    dictionaries. context is used to provide runtime information.
    """

    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
