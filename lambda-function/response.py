
"""Lex response functions to build responses which match the structure
of the necessary dialog actions.
"""


def elicit_slot(session_attributes, intent_name, slots,
                slot_to_elicit, message):
    """Elicit further data from the user. For example, if the user does not
    provide the correct slots, this will be used to re-elicit their slot
    values
    """

    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    """Sends dialog action close, which informs lex not to expect a
    response from the user"""

    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
