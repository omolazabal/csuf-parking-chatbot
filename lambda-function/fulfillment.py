
"""Controls behavior of the bot."""

import response

def optimal_parking(intent_request):
    """Fulfillment for finding the optimal parking lot to park at."""

    source = intent_request['invocationSource']

    if source == 'FulfillmentCodeHook':
        # Called once the user has provided all information to fulfill the intent.
        # In this case it is called immediately because there are no slots for
        # this intent.
        return response.close(intent_request['sessionAttributes'], 'Fulfilled',
                              {'contentType': 'PlainText',
                               'content': 'return best parking location(s)'})

    raise Exception('Error fulfilling OptimalParking intent')

def list_parking(intent_request):
    """Fulfillment for listing all available parking lots."""

    source = intent_request['invocationSource']

    if source == 'FulfillmentCodeHook':
        return response.close(intent_request['sessionAttributes'], 'Fulfilled',
                              {'contentType': 'PlainText',
                               'content': 'return list of available parking lots'})

    raise Exception('Error fulfilling OptimalParking intent')
