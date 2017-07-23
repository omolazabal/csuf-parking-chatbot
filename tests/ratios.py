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

    valid_lots = [
        'EvFree Church', 'State College Structure', 'Lot A & G',
        'Eastside Structure', 'Nutwood Structure', 'Brea Mall', 'all',
        'everywhere'
    ]

    max_ratio = 0
    is_valid = False
    lot = None
    limit = 0.7

    for valid_lot in valid_lots:
        # Go through each lot and compare the ratios. If the ratio is high
        # enough then save that lot
        ratio = difflib.SequenceMatcher(None, valid_lot.lower(),
                                        parking_lot).ratio()
        if valid_lot == 'Nutwood Structure':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'nutwood',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif valid_lot == 'State College Structure':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'state college',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif valid_lot == 'Eastside Structure':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'eastside',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif valid_lot == 'EvFree Church':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'evfree',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'church',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif valid_lot == 'Brea Mall':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'brea',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'mall',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif valid_lot == 'Lot A & G':
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'lot g & a',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'lot a', parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'a', parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'g', parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'a and g',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

            ratio = difflib.SequenceMatcher(None, 'g and a',
                                            parking_lot).ratio()
            if ratio >= limit and ratio >= max_ratio:
                is_valid = True
                lot = valid_lot
                max_ratio = ratio

        elif ratio >= limit and ratio >= max_ratio:
            is_valid = True
            lot = valid_lot
            max_ratio = ratio

    return {'isValid': is_valid, 'newLotName': lot, 'ratio': max_ratio}


print(is_valid_lot('sratw colege stuctur'))
