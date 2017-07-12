
"""Helper functions to assist in checking for errors and for specific cases"""


def try_ex(func):
    """Call passed in function in try block. If KeyError is encountered return
    None. This function is intended to be used to safely access dictionary.
    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None


def is_valid_lot(parking_lot):
    """Check if passed parking lot is valid"""

    valid_lots = [
        'evfree church', 'state college', 'a and g', 'g',
        'a', 'eastside', 'nutwood', 'brea mall', 'all'
    ]

    return parking_lot.lower() in valid_lots


def build_validation_result(is_valid, violated_slot, message_content):
    """Creates the results for whether a parking lot is valid or not"""

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {
            'contentType': 'PlainText',
            'content': message_content
        }
    }


def validate_parking_lot(slots):
    """Checks whether the user's requested lot is valid"""

    parking_lot = try_ex(lambda: slots['ParkingLot'])

    if parking_lot and not is_valid_lot(parking_lot):
        return build_validation_result(
            False,
            'ParkingLot',
            'I do not know of any information regarding {}, try a different'
            'parking lot.'.format(parking_lot)
        )

    return {'isValid': True}
