
"""Lex response functions to build responses which match the structure
of the necessary dialog actions.
"""

def close(session_attributes, fulfillment_state, message):
    """Sends dialog action close, which informs lex not to expect a
    response from the user"""

    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response
