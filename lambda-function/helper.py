
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


def build_validation_result(is_valid, violated_slot, message_content):
    """Creates the results for whether a parking lot is valid or not"""
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def validate_parking_lot(parking_lot):
    """Checks whether the user's requested lot is valid"""
    parking_lots = ['evfree church', 'state college', 'a and g', 'g',
                    'a', 'eastside', 'nutwood', 'brea mall', 'all']

    if parking_lot is not None and parking_lot.lower() not in parking_lots:
        return build_validation_result(False,
                                       'ParkingLot',
                                       'I do not know of any information'
                                       'regarfing {}, would you '
                                       'like to try a different parking '
                                       'lot?'.format(parking_lot))

    return build_validation_result(True, None, None)
