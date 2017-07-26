import difflib


def is_valid_lot(parking_lot):
    """Check if passed parking lot is valid. Uses difflib to check the ratio.
    if the raito of the checked word vs the actual word is equal to or above
    the limit, then the checked word is converted to the actual word.

    Returns a dictionary containing whether the checked lot is valid and the
    corrected spelling of the word."""

    if parking_lot is None:
        # If no parking lot is given, return
        return {'isValid': True, 'newLotName': None}

    parking_lot = parking_lot.lower()

    # Appropriate names of the parking lots
    valid_lots = [
        'Nutwood Structure', 'State College Structure', 'Eastside Structure',
        'Lot A & G', 'EvFree Church', 'Brea Mall', 'all', 'everywhere'
        ]

    # Alternative names for the parking lots
    lot_alts = {
        'Nutwood Structure': [
            'nutwood structure',
            'nutwood'
            ],
        'State College Structure': [
            'state college structure',
            'state college'
            ],
        'Eastside Structure': [
            'eastside structure', 'eastside'
            ],
        'Lot A & G': [
            'lot a & g', 'lot g & a', 'lot a',
            'a', 'g', 'a and g', 'g and a'
            ],
        'EvFree Church': [
            'evfree church',
            'evfree',
            'church'
            ],
        'Brea Mall': [
            'brea',
            'mall'
            ],
        'all': ['all'],
        'everywhere': ['everywhere']
    }

    max_ratio = 0
    is_valid = False
    lot = None  # Holds the corrected name of the lot

    # The threshold that the checked lot vs the actual lot ratio
    # has to surpass for the checked lot to be corrected to the
    # actual lot.
    limit = 0.75

    for valid_lot in valid_lots:
        # Go through each lot and compare the ratios. If the ratio is high
        # enough then save that lot

        for alt in lot_alts[valid_lot]:
            # Check the ratio for the current parking lot and the alt names.
            ratio = difflib.SequenceMatcher(None, alt, parking_lot).ratio()

            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

    return {'isValid': is_valid, 'newLotName': lot, 'ratio': max_ratio}


print(is_valid_lot('stastcolegs'))
