
"""Controls behavior of the bot."""

import json
import response
import helper
import lambda_function as lamfunc


def optimal_parking(intent_request):
    """Fulfillment for finding the optimal parking lot to park at."""

    source = intent_request['invocationSource']

    if source == 'FulfillmentCodeHook':
        # Called once the user has provided all information to fulfill the.
        # intent. In this case it is called immediately because there are no
        # slots for this intent.
        return response.close(
            intent_request['sessionAttributes'],
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': 'return best parking location(s)'
            }
        )

    raise Exception('Error fulfilling OptimalParking intent')


def list_parking(intent_request):
    """Fulfillment for listing all available parking lots."""

    source = intent_request['invocationSource']

    if source == 'FulfillmentCodeHook':
        return response.close(
            intent_request['sessionAttributes'],
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': 'return list of available parking lots'
            }
        )

    raise Exception('Error fulfilling OptimalParking intent')


def specific_parking(intent_request):
    """Fulfillment for giving the user information regarding a specified lot"""

    # Check for any errors with the current slots
    parking_lot = helper.try_ex(lambda: intent_request['currentIntent']
                                                      ['slots']
                                                      ["ParkingLot"])

    # Use of sessionAttributes to pass information that can be used to
    # guide conversation. Session attributes are pieces of information
    # that the user has provided to the chatbot either in a previous
    # intent or the current one.
    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
    else:
        session_attributes = {}

    # Load slot value history for parking lots and track current parking
    # request.
    parking_request = json.dumps({
        'ParkingRequest': 'Availability',
        'ParkingLot': parking_lot
    })

    session_attributes['currentParkingRequest'] = parking_request

    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Called on each user input until intent has been fulfilled.

        # Check and validate the slots that have been specified.
        validation_result = helper.validate_parking_lot(
                                intent_request['currentIntent']['slots']
                            )
        if not validation_result['isValid']:
            # If invalid, re-elicit for the slot values.
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return helper.elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        session_attributes['currentParkingRequest'] = parking_request
        return response.delegate(
            session_attributes,
            intent_request['currenIntent']['slots']
        )

    if source == 'FulfillmentHookCode':
        lamfunc.logger.debug('specificParking={}'.format(parking_request))

        helper.try_ex(lambda: session_attributes.pop('currentParkingRequest'))

        # Keep track of what was the last parking lot the user requested
        # information for.
        session_attributes['lastConfirmedParkingRequest'] = parking_request

        return response.close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': 'return parking information about {}'
                           .format(parking_lot)
            }
        )

    raise Exception('Error fulfilling SpecificParking intent')
