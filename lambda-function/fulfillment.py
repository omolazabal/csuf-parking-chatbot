
"""Controls behavior of the bot."""

import json
import response
import helper
import lambda_function as lamfunc
from random import randint


def optimal_parking(intent_request):
    """Fulfillment for finding the optimal parking lot to park at."""

    # Find optimal parking lot
    sorted_lots = helper.get_optimal_lots()
    parking_lot = sorted_lots['First']['Name']

    # Use of sessionAttributes to store information that can be used to guide
    # conversation. Session attributes are pieces of information that the user
    # has provided to the chatbot either in a previous intent or the current
    # one.
    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
    else:
        session_attributes = {}

    # Load slot value history for parking lots
    parking_request = json.dumps({
        'ParkingRequest': 'OptimalLot',
        'ParkingLot': parking_lot
    })

    # Track current parking request.
    session_attributes['currentParkingRequest'] = parking_request

    source = intent_request['invocationSource']

    if source == 'FulfillmentCodeHook':
        # Called once the user has provided all information to fulfill the.
        # intent. In this case it is called immediately because there are no
        # slots for this intent.
        lamfunc.logger.debug(
            'request for optimal parking={}'.format(parking_request)
        )

        # Clear settings from sessionAttributes
        helper.try_ex(lambda: session_attributes.pop('currentParkingRequest'))

        # Keep track of what was the last parking lot the user requested
        # information for.
        session_attributes['lastParkingRequest'] = parking_request

        # End the intent.
        return response.close(
            intent_request['sessionAttributes'],
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': '{} is the best place to park right now. It has '
                           '{} available parking spaces.'.format(
                               parking_lot,
                               sorted_lots['First']['AvailableSpaces']
                            )
            }
        )

    raise Exception('Error fulfilling OptimalParking intent')


def list_parking(intent_request):
    """Fulfillment for listing all available parking lots."""

    # Clear session attributes to avoid confusion
    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
        helper.try_ex(lambda: session_attributes.pop('lastParkingRequest'))

    source = intent_request['invocationSource']

    if source == 'FulfillmentCodeHook':
        lamfunc.logger.debug('request for lot list')

        return response.close(
            intent_request['sessionAttributes'],
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': helper.build_list_lot_msg()
            }
        )

    raise Exception('Error fulfilling OptimalParking intent')


def specific_parking(intent_request):
    """Fulfillment for giving the user information regarding a specified lot"""

    # Check for any errors with the current slots
    parking_lot = helper.try_ex(
        lambda: intent_request['currentIntent']['slots']['ParkingLot']
    )

    # Use of sessionAttributes to store information that can be used to guide
    # conversation.
    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
    else:
        session_attributes = {}

    # Load slot value history for parking lots
    parking_request = json.dumps({
        'ParkingRequest': 'LotAvailability',
        'ParkingLot': parking_lot
    })

    # Track current parking request.
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

            return response.elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        intent_request['currentIntent']['slots']['ParkingLot'] \
            = validation_result['newLotName']

        # Redirect to Amazon Lex to obtain slot values.
        return response.delegate(
            session_attributes,
            intent_request['currentIntent']['slots']
        )

    if source == 'FulfillmentCodeHook':
        lamfunc.logger.debug(
            'request for specific parking={}'.format(parking_request)
        )

        # Clear settings from sessionAttributes
        helper.try_ex(lambda: session_attributes.pop('currentParkingRequest'))

        # Keep track of what was the last parking lot the user requested
        # information for.
        session_attributes['lastParkingRequest'] = parking_request

        # End the intent.
        return response.close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': helper.build_specific_parking_msg(parking_lot)
            }
        )

    raise Exception('Error fulfilling SpecificParking intent')


def get_directions(intent_request):
    """Fulfillment for giving the user information regarding a specified lot"""

    # Check for any errors with the current slots
    parking_lot = helper.try_ex(
        lambda: intent_request['currentIntent']['slots']['ParkingLot']
    )

    # Use of sessionAttributes to retrieve information that can be used to
    # guide conversation.
    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
    else:
        session_attributes = {}

    # Check for a previous parking request the user had made.
    last_parking_req = helper.try_ex(
        lambda: session_attributes['lastParkingRequest']
    )
    if last_parking_req:
        last_parking_req = json.loads(last_parking_req)

    # Load slot value history for parking lots
    parking_request = json.dumps({
        'ParkingRequest': 'Directions',
        'ParkingLot': parking_lot
    })

    # Track current parking request.
    session_attributes['currentParkingRequest'] = parking_request

    source = intent_request['invocationSource']

    if source == 'DialogCodeHook':
        # Check and validate the slots that have been specified.
        validation_result = helper.validate_parking_lot(
                                intent_request['currentIntent']['slots']
                            )
        if not validation_result['isValid']:
            # If invalid, re-elicit for the slot values.
            slots = intent_request['currentIntent']['slots']
            slots[validation_result['violatedSlot']] = None

            return response.elicit_slot(
                session_attributes,
                intent_request['currentIntent']['name'],
                slots,
                validation_result['violatedSlot'],
                validation_result['message']
            )

        intent_request['currentIntent']['slots']['ParkingLot'] \
            = validation_result['newLotName']

        if parking_lot is None and last_parking_req:
            # If the slot empty and there is a parking lot already stored
            # from a previous conversation, then use that parking value
            lamfunc.logger.debug(
                'request for lot directions={}'.format(parking_request)
            )

            # Clear settings from sessionsAttributes.
            helper.try_ex(
                lambda: session_attributes.pop('currentParkingRequest')
            )
            helper.try_ex(
                lambda: session_attributes.pop('lastParkingRequest')
            )

            # End the intent.
            return response.close(
                session_attributes,
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': helper.build_directions_msg(
                        last_parking_req['ParkingLot']
                    )
                }
            )

        # Otherwise, redirect to Amazon Lex to obtain slot values.
        return response.delegate(
            session_attributes,
            intent_request['currentIntent']['slots']
        )

    if source == 'FulfillmentCodeHook':
        lamfunc.logger.debug(
            'request for lot directions={}'.format(parking_request)
        )

        # Clear settings from sessionAttributes
        helper.try_ex(lambda: session_attributes.pop('currentParkingRequest'))
        helper.try_ex(lambda: session_attributes.pop('lastParkingRequest'))

        # End the intent.
        return response.close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': helper.build_directions_msg(parking_lot)
            }
        )

    raise Exception('Error fulfilling SpecificParking intent')


def greeting(intent_request):
    """Fulfillment for greeting the user."""

    # Clear session attributes to avoid confusion
    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
        helper.try_ex(lambda: session_attributes.pop('lastParkingRequest'))

    source = intent_request['invocationSource']

    if source == 'FulfillmentCodeHook':
        lamfunc.logger.debug('greet the user')

        message = [
            'Hey there! I can assist you with parking. Try asking me "Where '
            'should I park today?" or "Give me directions to State College '
            'Structure."',
            'Hello there! Need help parking? I can help you with that.',
            'How\'s it going?'
        ]

        index = randint(0, 2)  # Choose random message.

        return response.close(
            intent_request['sessionAttributes'],
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': message[index]
            }
        )

    raise Exception('Error fulfilling OptimalParking intent')


def closing(intent_request):
    """Fulfillment for closing the conversation with the user."""

    # Clear session attributes to avoid confusion
    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
        helper.try_ex(lambda: session_attributes.pop('lastParkingRequest'))

    source = intent_request['invocationSource']

    if source == 'FulfillmentCodeHook':
        lamfunc.logger.debug('greet the user')

        message = [
            'Bye!',
            'Adios!',
            'See you later!'
        ]

        index = randint(0, 2)  # Choose random message.

        return response.close(
            intent_request['sessionAttributes'],
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': message[index]
            }
        )

    raise Exception('Error fulfilling OptimalParking intent')


def joke(intent_request):
    """Fulfillment for telling the user a joke."""

    # Clear session attributes to avoid confusion
    if intent_request['sessionAttributes'] is not None:
        session_attributes = intent_request['sessionAttributes']
        helper.try_ex(lambda: session_attributes.pop('lastParkingRequest'))

    source = intent_request['invocationSource']

    if source == 'FulfillmentCodeHook':
        lamfunc.logger.debug('greet the user')

        message = [
            "When is a car not a car? When it turns into a driveway.",
            "I couldn't figure out how to fasten my seatbelt. Then it "
            "clicked.",
            "What do you do when you see a spaceman? Park in it, man.",
            "I got complimented on my parking today. Someone left a note that "
            "said PARKING FINE."
        ]

        index = randint(0, 3)  # Choose random message.

        return response.close(
            intent_request['sessionAttributes'],
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': message[index]
            }
        )

    raise Exception('Error fulfilling OptimalParking intent')