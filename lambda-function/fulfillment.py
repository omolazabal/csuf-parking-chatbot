
"""Controls behavior of the bot."""

import json
import response
import helper
import lambda_function as lamfunc


def optimal_parking(intent_request):
    """Fulfillment for finding the optimal parking lot to park at."""

    # Find optimal parking lot
    parking_lot = "best parking lot"

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
                'content': 'best parking location: {}'.format(parking_lot)
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

        # Obtain data and format into message
        lot_list = helper.get_available_lots()

        if not lot_list['ClosedLots']:
            available_lots = lot_list['AvailableLots'][0]
            del lot_list['AvailableLots'][0]
            for lot in lot_list['AvailableLots']:
                available_lots += (', ' + lot)
            message = 'All parking locations are open today! You can park' \
                      ' at {}.'.format(available_lots)
        else:
            available_lots = lot_list['AvailableLots'][0]
            del lot_list['AvailableLots'][0]
            for lot in lot_list['AvailableLots']:
                available_lots += (', ' + lot)

            closed_lots = lot_list['ClosedLots'][0]
            del lot_list['ClosedLots'][0]
            for lot in lot_list['ClosedLots']:
                closed_lots += (', ' + lot)

            message = 'Today you can park at: {}. You cannot park at: ' \
                      '{}.'.format(available_lots, closed_lots)

        return response.close(
            intent_request['sessionAttributes'],
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': message
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

        # Obtain and format data into message
        parking_data = helper.scrape_data()
        lot_name = parking_lot.replace(' ', '')

        if lot_name == 'all':
            message = 'Here are the available spaces for all locations: ' \
                  'Nutwood Structure ({}), State College Structure({}), ' \
                  'Eastside Structure ({}), Lot A & G ({}), ' \
                  'EvFree Church ({}), Brea Mall ({})'.format(
                      parking_data['NutwoodStructure']['AvailableSpaces'],
                      parking_data['StateCollegeStructure']['AvailableSpaces'],
                      parking_data['EastsideStructure']['AvailableSpaces'],
                      parking_data['LotA&G']['AvailableSpaces'],
                      parking_data['EvFreeChurch']['AvailableSpaces'],
                      parking_data['BreaMall']['AvailableSpaces']
                  )
        elif parking_data[lot_name]['AvailableSpaces'] == 'Closed':
            message = '{} is currently close. It is open on {}.'.format(
                parking_lot,
                parking_data[lot_name]['Date']
            )
        else:
            message = "{} currently has {} available parking spaces.".format(
                parking_lot,
                parking_data[lot_name]['AvailableSpaces']
            )

        # End the intent.
        return response.close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': message
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
                    'content': 'return directions to {}'.format(
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

        # Obtain and format data into message
        parking_data = helper.scrape_data()
        lot_name = parking_lot.replace(' ', '')

        if lot_name == 'all':
            message = 'Here are the directions for all locations: ' \
                  'Nutwood Structure ({}), State College Structure({}), ' \
                  'Eastside Structure ({}), Lot A & G ({}), ' \
                  'EvFree Church ({}), Brea Mall ({})'.format(
                      parking_data['NutwoodStructure']['Directions'],
                      parking_data['StateCollegeStructure']['Directions'],
                      parking_data['EastsideStructure']['Directions'],
                      parking_data['LotA&G']['Directions'],
                      parking_data['EvFreeChurch']['Directions'],
                      parking_data['BreaMall']['Directions']
                  )

        else:
            message = 'Here are the directions to {}: {}'.format(
                  parking_lot,
                  parking_data[lot_name]['Directions']
            )

        # End the intent.
        return response.close(
            session_attributes,
            'Fulfilled',
            {
                'contentType': 'PlainText',
                'content': message
            }
        )

    raise Exception('Error fulfilling SpecificParking intent')
